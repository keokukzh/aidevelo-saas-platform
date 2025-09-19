# 🌐 DNS-Konfiguration für aidevelo.co

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