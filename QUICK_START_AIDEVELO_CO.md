# 🚀 AiDevelo.co - Quick Start Guide

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