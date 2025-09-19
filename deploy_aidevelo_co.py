#!/usr/bin/env python3
"""
AiDevelo.co - Complete Deployment Script
Deploys AI SaaS Platform to aidevelo.co domain
"""

import subprocess
import os
import json
from pathlib import Path

class AiDeveloCoDeployer:
    def __init__(self):
        self.domain = "aidevelo.co"
        self.subdomains = {
            "app": "app.aidevelo.co",      # Main SaaS App
            "dashboard": "dashboard.aidevelo.co",  # Enterprise Dashboard
            "api": "api.aidevelo.co"       # API Services
        }
        
    def log(self, message):
        print(f"🚀 [DEPLOY] {message}")
        
    def create_streamlit_configs(self):
        """Create Streamlit configs for all subdomains"""
        config_dir = Path(".streamlit")
        config_dir.mkdir(exist_ok=True)
        
        configs = {
            "app": {"port": 8501, "file": "main.py"},
            "dashboard": {"port": 8502, "file": "enterprise_aidevelo.py"},
            "api": {"port": 8503, "file": "api_server.py"}
        }
        
        for subdomain, config in configs.items():
            config_content = f"""
[server]
port = {config['port']}
address = "0.0.0.0"
headless = true
baseUrlPath = "/"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
"""
            
            config_file = config_dir / f"config_{subdomain}.toml"
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(config_content.strip())
            self.log(f"✅ Streamlit config created for {subdomain}")
            
    def create_api_server(self):
        """Create API server for api.aidevelo.co"""
        api_content = '''#!/usr/bin/env python3
"""
API Server for aidevelo.co
Provides REST API endpoints for the SaaS platform
"""

from flask import Flask, request, jsonify
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "AiDevelo.co API Server",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "pricing": "/api/pricing",
            "webhook": "/api/webhook/stripe"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"})

@app.route('/api/pricing')
def pricing():
    return jsonify({
        "plans": {
            "free": {"price": 0, "features": ["10 AI queries/month"]},
            "basic": {"price": 9.99, "features": ["100 AI queries/month", "Basic analytics"]},
            "pro": {"price": 29.99, "features": ["1000 AI queries/month", "Advanced analytics"]},
            "enterprise": {"price": 99.99, "features": ["Unlimited queries", "Custom features"]}
        }
    })

@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
        
        if event['type'] == 'checkout.session.completed':
            # Handle successful payment
            session = event['data']['object']
            # Update user subscription in database
            pass
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8503, debug=False)
'''
        
        with open("api_server.py", "w", encoding="utf-8") as f:
            f.write(api_content.strip())
        self.log("✅ API server created")
        
    def create_dockerfiles(self):
        """Create Dockerfiles for all services"""
        services = {
            "app": {"port": 8501, "file": "main.py"},
            "dashboard": {"port": 8502, "file": "enterprise_aidevelo.py"},
            "api": {"port": 8503, "file": "api_server.py"}
        }
        
        for service, config in services.items():
            dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for API server
RUN pip install flask

# Copy application files
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \\
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{config['port']}/health || exit 1

EXPOSE {config['port']}

CMD ["python", "{config['file']}"]
"""
            
            dockerfile_name = f"Dockerfile_{service}"
            with open(dockerfile_name, "w", encoding="utf-8") as f:
                f.write(dockerfile_content.strip())
            self.log(f"✅ Dockerfile created for {service}")
            
    def create_docker_compose(self):
        """Create docker-compose for aidevelo.co"""
        compose_content = """
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile_app
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - DOMAIN=https://aidevelo.co
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  dashboard:
    build:
      context: .
      dockerfile: Dockerfile_dashboard
    ports:
      - "8502:8502"
    environment:
      - STREAMLIT_SERVER_PORT=8502
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - DOMAIN=https://aidevelo.co
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8502/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build:
      context: .
      dockerfile: Dockerfile_api
    ports:
      - "8503:8503"
    environment:
      - FLASK_ENV=production
      - DOMAIN=https://aidevelo.co
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8503/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx_aidevelo_co.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
      - dashboard
      - api
    restart: unless-stopped
"""
        
        with open("docker-compose-aidevelo-co.yml", "w", encoding="utf-8") as f:
            f.write(compose_content.strip())
        self.log("✅ Docker Compose created for aidevelo.co")
        
    def create_nginx_config(self):
        """Create Nginx config for aidevelo.co subdomains"""
        nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream app_backend {
        server app:8501;
    }
    
    upstream dashboard_backend {
        server dashboard:8502;
    }
    
    upstream api_backend {
        server api:8503;
    }
    
    # Main SaaS App - app.aidevelo.co
    server {
        listen 80;
        server_name app.aidevelo.co;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
        
        location / {
            proxy_pass http://app_backend;
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
        
        location /_stcore/stream {
            proxy_pass http://app_backend/_stcore/stream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
    
    # Enterprise Dashboard - dashboard.aidevelo.co
    server {
        listen 80;
        server_name dashboard.aidevelo.co;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
        
        location / {
            proxy_pass http://dashboard_backend;
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
        
        location /_stcore/stream {
            proxy_pass http://dashboard_backend/_stcore/stream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
    
    # API Services - api.aidevelo.co
    server {
        listen 80;
        server_name api.aidevelo.co;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
        
        location / {
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
        
        with open("nginx_aidevelo_co.conf", "w", encoding="utf-8") as f:
            f.write(nginx_config.strip())
        self.log("✅ Nginx config created for aidevelo.co")
        
    def create_dns_instructions(self):
        """Create DNS configuration instructions"""
        dns_content = """# 🌐 DNS-Konfiguration für aidevelo.co

## 📋 Cloudflare DNS-Einträge hinzufügen

### Gehen Sie zu Cloudflare DNS Management für aidevelo.co und fügen Sie folgende CNAME-Einträge hinzu:

```
Type: CNAME
Name: app
Content: [Ihr Server IP oder Cloudflare Pages URL]
Proxy status: Proxied (orange Wolke)
TTL: Auto

Type: CNAME
Name: dashboard  
Content: [Ihr Server IP oder Cloudflare Pages URL]
Proxy status: Proxied (orange Wolke)
TTL: Auto

Type: CNAME
Name: api
Content: [Ihr Server IP oder Cloudflare Pages URL]
Proxy status: Proxied (orange Wolke)
TTL: Auto
```

## 🎯 URLs nach DNS-Konfiguration:

- **B2B SaaS**: https://app.aidevelo.co
- **Enterprise Dashboard**: https://dashboard.aidevelo.co  
- **API Services**: https://api.aidevelo.co
- **Hauptseite**: https://aidevelo.co (bereits konfiguriert)

## 💰 Verkaufsstrategie:

### B2B SaaS (app.aidevelo.co)
- Preise: 9,99€ - 99,99€/Monat
- Zielgruppe: KMU, Startups
- Features: Benutzerauthentifizierung, Zahlungen, KI-Tools

### Enterprise (dashboard.aidevelo.co)
- Preise: 25K€ - 150K€/Monat
- Zielgruppe: Fortune 500
- Features: ROI-Rechner, Enterprise Analytics, Custom Development

## 🚀 Deployment-Optionen:

### Option 1: Docker (Empfohlen)
```bash
docker-compose -f docker-compose-aidevelo-co.yml up -d
```

### Option 2: Cloudflare Pages
```bash
# App deployen
wrangler pages publish . --project-name aidevelo-app
wrangler pages domain add aidevelo-app app.aidevelo.co

# Dashboard deployen
wrangler pages publish . --project-name aidevelo-dashboard
wrangler pages domain add aidevelo-dashboard dashboard.aidevelo.co
```

### Option 3: Lokaler Start (Testing)
```bash
# Terminal 1 - App
streamlit run main.py --server.port=8501

# Terminal 2 - Dashboard
streamlit run enterprise_aidevelo.py --server.port=8502

# Terminal 3 - API
python api_server.py
```

---
**🎯 aidevelo.co ist bereit für den Verkauf!**
"""
        
        with open("DNS_CONFIGURATION.md", "w", encoding="utf-8") as f:
            f.write(dns_content.strip())
        self.log("✅ DNS configuration guide created")
        
    def create_quick_start(self):
        """Create quick start guide"""
        quick_start = """# 🚀 AiDevelo.co - Quick Start Guide

## ⚡ In 10 Minuten live!

### Schritt 1: DNS konfigurieren (5 Min)
1. Gehen Sie zu Cloudflare DNS Management
2. Fügen Sie CNAME-Einträge hinzu:
   - `app` → [Ihr Server]
   - `dashboard` → [Ihr Server]
   - `api` → [Ihr Server]

### Schritt 2: Apps starten (5 Min)
```bash
# Docker (empfohlen)
docker-compose -f docker-compose-aidevelo-co.yml up -d

# Oder lokal
streamlit run main.py --server.port=8501 &
streamlit run enterprise_aidevelo.py --server.port=8502 &
python api_server.py &
```

### Schritt 3: URLs testen
- https://app.aidevelo.co
- https://dashboard.aidevelo.co
- https://api.aidevelo.co

## 💰 Sofortiger Verkauf:

### B2B SaaS: app.aidevelo.co
- Free: 0€ (10 Abfragen/Monat)
- Basic: 9,99€/Monat
- Pro: 29,99€/Monat
- Enterprise: 99,99€/Monat

### Enterprise: dashboard.aidevelo.co
- Starter: 25.000€/Monat
- Professional: 75.000€/Monat
- Elite: 150.000€/Monat

## 🎯 Marketing-URLs:
- Hauptseite: https://aidevelo.co
- Demo: https://app.aidevelo.co/demo
- ROI-Rechner: https://dashboard.aidevelo.co/roi
- API-Docs: https://api.aidevelo.co

---
**🚀 Starten Sie jetzt mit dem Verkauf!**
"""
        
        with open("QUICK_START_AIDEVELO_CO.md", "w", encoding="utf-8") as f:
            f.write(quick_start.strip())
        self.log("✅ Quick start guide created")
        
    def deploy(self):
        """Execute complete deployment setup for aidevelo.co"""
        self.log("🎯 Starting AiDevelo.co Complete Deployment Setup")
        
        # Create all configurations
        self.create_streamlit_configs()
        self.create_api_server()
        self.create_dockerfiles()
        self.create_docker_compose()
        self.create_nginx_config()
        self.create_dns_instructions()
        self.create_quick_start()
        
        self.log("✅ All aidevelo.co deployment files created!")
        
        print(f"""
🎉 AIDEVELO.CO DEPLOYMENT READY!

📁 Files created:
  ✅ Dockerfile_app - B2B SaaS App
  ✅ Dockerfile_dashboard - Enterprise Dashboard
  ✅ Dockerfile_api - API Services
  ✅ docker-compose-aidevelo-co.yml - Complete Setup
  ✅ nginx_aidevelo_co.conf - Subdomain Routing
  ✅ api_server.py - REST API Server
  ✅ DNS_CONFIGURATION.md - DNS Setup Guide
  ✅ QUICK_START_AIDEVELO_CO.md - Quick Start

🌐 Subdomains to configure:
  ✅ app.aidevelo.co - B2B SaaS (9,99€ - 99,99€/Monat)
  ✅ dashboard.aidevelo.co - Enterprise (25K€ - 150K€/Monat)
  ✅ api.aidevelo.co - API Services

🎯 Next steps:
  1. Add DNS CNAME records in Cloudflare:
     - app.aidevelo.co
     - dashboard.aidevelo.co
     - api.aidevelo.co
  2. Run: docker-compose -f docker-compose-aidevelo-co.yml up -d
  3. Test URLs and start selling!

💰 Ready for immediate sales:
  ✅ Professional .co domain
  ✅ Clean subdomain structure
  ✅ B2B and Enterprise versions
  ✅ API services included
  ✅ No conflicts with existing apps

🚀 Start selling on aidevelo.co now!
""")

if __name__ == "__main__":
    deployer = AiDeveloCoDeployer()
    deployer.deploy()
