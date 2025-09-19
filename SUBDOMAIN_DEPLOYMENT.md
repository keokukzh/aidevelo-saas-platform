# 🚀 AiDevelo.ai - Subdomain Deployment Guide

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