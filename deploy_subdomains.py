#!/usr/bin/env python3
"""
AiDevelo.ai - Subdomain Deployment Script
Deploys AI SaaS Platform to new subdomains
"""

import subprocess
import os
import json
from pathlib import Path

class SubdomainDeployer:
    def __init__(self):
        self.domain = "aidevelo.ai"
        self.subdomains = {
            "saas": "saas.aidevelo.ai",
            "dashboard": "dashboard.aidevelo.ai"
        }
        
    def log(self, message):
        print(f"🚀 [DEPLOY] {message}")
        
    def create_streamlit_config(self, subdomain):
        """Create Streamlit config for subdomain"""
        config_dir = Path(".streamlit")
        config_dir.mkdir(exist_ok=True)
        
        port = 8501 if subdomain == "saas" else 8502
        
        config_content = f"""
[server]
port = {port}
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
        with open(config_file, "w") as f:
            f.write(config_content.strip())
        self.log(f"✅ Streamlit config created for {subdomain}")
        
    def create_dockerfile(self, subdomain):
        """Create Dockerfile for subdomain"""
        app_file = "main.py" if subdomain == "saas" else "enterprise_aidevelo.py"
        port = 8501 if subdomain == "saas" else 8502
        
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

# Copy application files
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \\
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{port}/_stcore/health || exit 1

EXPOSE {port}

CMD ["streamlit", "run", "{app_file}", "--server.port={port}", "--server.address=0.0.0.0"]
"""
        
        dockerfile_name = f"Dockerfile_{subdomain}"
        with open(dockerfile_name, "w") as f:
            f.write(dockerfile_content.strip())
        self.log(f"✅ Dockerfile created for {subdomain}")
        
    def create_docker_compose(self):
        """Create docker-compose for subdomains"""
        compose_content = """
version: '3.8'

services:
  saas:
    build:
      context: .
      dockerfile: Dockerfile_saas
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

  dashboard:
    build:
      context: .
      dockerfile: Dockerfile_dashboard
    ports:
      - "8502:8502"
    environment:
      - STREAMLIT_SERVER_PORT=8502
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8502/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx_subdomains.conf:/etc/nginx/nginx.conf
    depends_on:
      - saas
      - dashboard
    restart: unless-stopped
"""
        
        with open("docker-compose-subdomains.yml", "w") as f:
            f.write(compose_content.strip())
        self.log("✅ Docker Compose created for subdomains")
        
    def create_nginx_config(self):
        """Create Nginx config for subdomains"""
        nginx_config = """
events {
    worker_connections 1024;
}

http {
    upstream saas_backend {
        server saas:8501;
    }
    
    upstream dashboard_backend {
        server dashboard:8502;
    }
    
    # SaaS Subdomain
    server {
        listen 80;
        server_name saas.aidevelo.ai;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
        location / {
            proxy_pass http://saas_backend;
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
            proxy_pass http://saas_backend/_stcore/stream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
    
    # Dashboard Subdomain
    server {
        listen 80;
        server_name dashboard.aidevelo.ai;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
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
}
"""
        
        with open("nginx_subdomains.conf", "w") as f:
            f.write(nginx_config.strip())
        self.log("✅ Nginx config created for subdomains")
        
    def create_deployment_guide(self):
        """Create deployment guide for subdomains"""
        guide_content = """# 🚀 AiDevelo.ai - Subdomain Deployment Guide

## 📋 DNS-Konfiguration (Cloudflare)

### Neue CNAME-Einträge hinzufügen:

1. **Gehen Sie zu Cloudflare DNS Management**
2. **Klicken Sie auf "Add record"**
3. **Fügen Sie folgende Einträge hinzu:**

```
Type: CNAME
Name: saas
Content: [Ihr Server IP oder Cloudflare Pages URL]
Proxy status: Proxied (orange Wolke)
TTL: Auto

Type: CNAME  
Name: dashboard
Content: [Ihr Server IP oder Cloudflare Pages URL]
Proxy status: Proxied (orange Wolke)
TTL: Auto
```

## 🚀 Deployment-Optionen

### Option 1: Docker (Empfohlen für Produktion)

```bash
# 1. Docker Compose starten
docker-compose -f docker-compose-subdomains.yml up -d

# 2. URLs testen
curl http://saas.aidevelo.ai
curl http://dashboard.aidevelo.ai
```

### Option 2: Lokaler Start (Für Testing)

```bash
# Terminal 1 - SaaS App
streamlit run main.py --server.port=8501

# Terminal 2 - Dashboard App  
streamlit run enterprise_aidevelo.py --server.port=8502
```

### Option 3: Cloudflare Pages

```bash
# 1. Wrangler installieren
npm install -g wrangler

# 2. SaaS deployen
wrangler pages publish . --project-name aidevelo-saas
wrangler pages domain add aidevelo-saas saas.aidevelo.ai

# 3. Dashboard deployen
wrangler pages publish . --project-name aidevelo-dashboard
wrangler pages domain add aidevelo-dashboard dashboard.aidevelo.ai
```

## 🎯 URLs nach Deployment

- **Basis SaaS**: https://saas.aidevelo.ai
- **Enterprise Dashboard**: https://dashboard.aidevelo.ai
- **API Services**: https://api.aidevelo.ai (bestehend)

## 💰 Verkaufsstrategie

### B2B SaaS (saas.aidevelo.ai)
- Preise: 9,99€ - 99,99€/Monat
- Zielgruppe: KMU, Startups
- Features: Benutzerauthentifizierung, Zahlungen, KI-Tools

### Enterprise (dashboard.aidevelo.ai)
- Preise: 25K€ - 150K€/Monat
- Zielgruppe: Fortune 500
- Features: ROI-Rechner, Enterprise Analytics, Custom Development

## 🔧 Troubleshooting

### DNS-Propagation
- Warten Sie 5-15 Minuten nach DNS-Änderungen
- Testen Sie mit: `nslookup saas.aidevelo.ai`

### Port-Konflikte
- SaaS läuft auf Port 8501
- Dashboard läuft auf Port 8502
- Nginx läuft auf Port 80/443

### SSL-Zertifikate
- Cloudflare automatisches SSL
- Oder Let's Encrypt für eigene Server

---
**🚀 Bereit für den Verkauf mit professionellen Subdomains!**
"""
        
        with open("SUBDOMAIN_DEPLOYMENT.md", "w", encoding="utf-8") as f:
            f.write(guide_content.strip())
        self.log("✅ Subdomain deployment guide created")
        
    def deploy(self):
        """Execute subdomain deployment setup"""
        self.log("🎯 Starting Subdomain Deployment Setup")
        
        # Create configurations for both subdomains
        for subdomain in self.subdomains.keys():
            self.create_streamlit_config(subdomain)
            self.create_dockerfile(subdomain)
            
        self.create_docker_compose()
        self.create_nginx_config()
        self.create_deployment_guide()
        
        self.log("✅ All subdomain deployment files created!")
        
        print(f"""
🎉 SUBDOMAIN DEPLOYMENT READY!

📁 Files created:
  ✅ Dockerfile_saas - SaaS App Container
  ✅ Dockerfile_dashboard - Dashboard App Container
  ✅ docker-compose-subdomains.yml - Multi-app Setup
  ✅ nginx_subdomains.conf - Subdomain Routing
  ✅ SUBDOMAIN_DEPLOYMENT.md - Complete Guide

🎯 Next steps:
  1. Add DNS CNAME records in Cloudflare:
     - saas.aidevelo.ai
     - dashboard.aidevelo.ai
  2. Run: docker-compose -f docker-compose-subdomains.yml up -d
  3. Test URLs:
     - https://saas.aidevelo.ai
     - https://dashboard.aidevelo.ai

💰 Ready for sales:
  ✅ B2B SaaS: saas.aidevelo.ai (9,99€ - 99,99€/Monat)
  ✅ Enterprise: dashboard.aidevelo.ai (25K€ - 150K€/Monat)
  ✅ Professional subdomain structure
  ✅ No conflicts with existing apps

🚀 Start selling immediately!
""")

if __name__ == "__main__":
    deployer = SubdomainDeployer()
    deployer.deploy()
