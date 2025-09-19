#!/usr/bin/env python3
"""
AiDevelo.ai - Cloudflare Deployment Script
Deploys the Enterprise SaaS to aidevelo.ai domain
"""

import os
import subprocess
import json
from pathlib import Path

class AiDeveloDeployer:
    def __init__(self):
        self.domain = "aidevelo.ai"
        self.project_name = "aidevelo-enterprise"
        
    def log(self, message):
        print(f"🚀 [DEPLOY] {message}")
        
    def create_requirements(self):
        """Create requirements.txt for deployment"""
        requirements = """
streamlit==1.28.1
pandas==2.1.3
plotly==5.17.0
requests==2.31.0
python-dotenv==1.0.0
"""
        with open("requirements.txt", "w") as f:
            f.write(requirements.strip())
        self.log("✅ Requirements.txt created")
        
    def create_streamlit_config(self):
        """Create Streamlit configuration"""
        config_dir = Path(".streamlit")
        config_dir.mkdir(exist_ok=True)
        
        config_content = """
[server]
port = 8501
address = "0.0.0.0"
headless = true

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
"""
        
        with open(config_dir / "config.toml", "w") as f:
            f.write(config_content.strip())
        self.log("✅ Streamlit config created")
        
    def create_dockerfile(self):
        """Create production Dockerfile"""
        dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

CMD ["streamlit", "run", "enterprise_aidevelo.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content.strip())
        self.log("✅ Dockerfile created")
        
    def create_docker_compose(self):
        """Create docker-compose for local testing"""
        compose_content = """
version: '3.8'

services:
  aidevelo:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - aidevelo
    restart: unless-stopped
"""
        
        with open("docker-compose.yml", "w") as f:
            f.write(compose_content.strip())
        self.log("✅ Docker Compose created")
        
    def create_nginx_config(self):
        """Create Nginx reverse proxy config"""
        nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server aidevelo:8501;
    }
    
    server {
        listen 80;
        server_name aidevelo.ai www.aidevelo.ai;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
        # Streamlit specific
        location / {
            proxy_pass http://streamlit;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
            proxy_buffering off;
        }
        
        # Streamlit WebSocket support
        location /_stcore/stream {
            proxy_pass http://streamlit/_stcore/stream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
"""
        
        with open("nginx.conf", "w") as f:
            f.write(nginx_config.strip())
        self.log("✅ Nginx config created")
        
    def create_cloudflare_worker(self):
        """Create Cloudflare Worker for additional functionality"""
        worker_code = """
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Add security headers
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    
    newResponse.headers.set('X-Frame-Options', 'DENY');
    newResponse.headers.set('X-Content-Type-Options', 'nosniff');
    newResponse.headers.set('X-XSS-Protection', '1; mode=block');
    newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000');
    
    // Analytics tracking
    if (url.pathname.includes('/contact') || url.pathname.includes('/demo')) {
      // Log enterprise inquiries
      console.log(`Enterprise inquiry: ${url.pathname} from ${request.headers.get('CF-Connecting-IP')}`);
    }
    
    return newResponse;
  },
};
"""
        
        with open("worker.js", "w") as f:
            f.write(worker_code.strip())
        self.log("✅ Cloudflare Worker created")
        
    def create_deployment_guide(self):
        """Create deployment documentation"""
        guide_content = """# AiDevelo.ai Deployment Guide

## 🚀 Quick Deploy to Cloudflare

### Option 1: Cloudflare Pages (Recommended)
```bash
# 1. Build and deploy
npm install -g wrangler
wrangler pages project create aidevelo-ai
wrangler pages publish . --project-name aidevelo-ai

# 2. Set custom domain
wrangler pages deployment tail --project-name aidevelo-ai
```

### Option 2: Docker Deployment  
```bash
# 1. Build image
docker build -t aidevelo:latest .

# 2. Run locally
docker-compose up -d

# 3. Deploy to production
docker push your-registry/aidevelo:latest
```

## 🔧 Configuration

### Environment Variables
```env
STREAMLIT_SERVER_PORT=8501
OPENAI_API_KEY=your_openai_key
STRIPE_SECRET_KEY=your_stripe_key
ENTERPRISE_MODE=true
```

### DNS Settings (Cloudflare)
```
Type: A
Name: @
Value: Your server IP
Proxy: Enabled

Type: CNAME  
Name: www
Value: aidevelo.ai
Proxy: Enabled
```

## 🎯 Enterprise Features Active

✅ Multi-page navigation
✅ ROI Calculator  
✅ AI Demo sections
✅ Enterprise pricing
✅ Contact forms
✅ Analytics dashboard
✅ Security headers
✅ Performance optimization

## 📊 Monitoring

- Cloudflare Analytics
- Application performance monitoring
- Error tracking
- User journey analytics

## 💰 Revenue Tracking

- Enterprise lead capture
- Demo request tracking  
- Conversion analytics
- ROI calculations

---
**AiDevelo.ai - Ready for Enterprise Sales** 🚀
"""
        
        with open("DEPLOYMENT.md", "w") as f:
            f.write(guide_content.strip())
        self.log("✅ Deployment guide created")
        
    def create_sales_config(self):
        """Create sales and marketing configuration"""
        sales_config = {
            "enterprise": {
                "pricing": {
                    "starter": 25000,
                    "professional": 75000,
                    "elite": 150000
                },
                "contact": {
                    "email": "enterprise@aidevelo.ai",
                    "phone": "+1-555-123-ADEV",
                    "response_time": "< 2 hours"
                },
                "features": {
                    "compliance": ["SOC2", "HIPAA", "ISO27001", "GDPR"],
                    "deployment": ["Cloud", "On-premise", "Hybrid"],
                    "support": ["24/7", "Dedicated", "SLA 99.99%"]
                }
            },
            "marketing": {
                "target_industries": [
                    "Financial Services",
                    "Healthcare", 
                    "Manufacturing",
                    "Government"
                ],
                "value_props": [
                    "10x faster development",
                    "340% average ROI",
                    "99.97% uptime",
                    "Enterprise security"
                ]
            }
        }
        
        with open("sales_config.json", "w") as f:
            json.dump(sales_config, f, indent=2)
        self.log("✅ Sales configuration created")
        
    def deploy(self):
        """Execute full deployment"""
        self.log("🎯 Starting AiDevelo.ai Enterprise Deployment")
        
        # Create all deployment files
        self.create_requirements()
        self.create_streamlit_config()
        self.create_dockerfile()
        self.create_docker_compose()
        self.create_nginx_config()
        self.create_cloudflare_worker()
        self.create_deployment_guide()
        self.create_sales_config()
        
        self.log("✅ All deployment files created!")
        
        print(f"""
🎉 AIDEVELO.AI DEPLOYMENT READY!

📁 Files created:
  ✅ requirements.txt - Python dependencies
  ✅ Dockerfile - Production container
  ✅ docker-compose.yml - Local testing
  ✅ nginx.conf - Reverse proxy
  ✅ worker.js - Cloudflare Worker
  ✅ DEPLOYMENT.md - Full guide
  ✅ sales_config.json - Sales configuration

🚀 Next steps:
  1. Copy enterprise_aidevelo.py to your deployment folder
  2. Run: docker-compose up -d (for local testing)
  3. Deploy to Cloudflare Pages or your preferred host
  4. Point aidevelo.ai DNS to your server
  5. Configure SSL certificate

💰 Enterprise Features Ready:
  ✅ ROI Calculator ($25K-$150K/month pricing)
  ✅ AI Capabilities Demo
  ✅ Enterprise Analytics
  ✅ Security & Compliance 
  ✅ Contact/Sales Forms
  ✅ Professional Design

🎯 Ready to sell to Fortune 500 companies!
""")

if __name__ == "__main__":
    deployer = AiDeveloDeployer()
    deployer.deploy()
