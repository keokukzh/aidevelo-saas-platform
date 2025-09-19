# SaaS Setup PowerShell Script
Write-Host "🚀 Erstelle SaaS Deployment" -ForegroundColor Green

# Navigate to Desktop
cd $env:USERPROFILE\Desktop
if (!(Test-Path "saas")) { mkdir saas }
cd saas

Write-Host "📁 Arbeite in: $(Get-Location)" -ForegroundColor Yellow

# .env Datei
@"
STRIPE_SECRET_KEY=sk_test_51S8tiw6bysxOOlngnay4pVwXkRYO00OOnnQSeCO8etZth9yeMbQ2dNGKCsXX8FCdXhyV1NA2WSMo3Tcl1Ln33cy300nhN9ej2o
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
DATABASE_URL=sqlite:///saas_app.db
SECRET_KEY=change_this_secret_key_12345
DOMAIN=http://localhost:8501
DEBUG=True
"@ | Out-File -FilePath ".env" -Encoding UTF8

# requirements.txt
@"
streamlit>=1.28.0
stripe>=5.5.0
python-dotenv>=1.0.0
pandas>=2.0.0
plotly>=5.15.0
requests>=2.31.0
bcrypt>=4.0.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "✅ Dateien erstellt!" -ForegroundColor Green
Write-Host "📋 Nächste Schritte:" -ForegroundColor Cyan
Write-Host "1. pip install -r requirements.txt" -ForegroundColor White
Write-Host "2. streamlit run main.py" -ForegroundColor White

# Installation starten
$install = Read-Host "Dependencies jetzt installieren? (j/n)"
if ($install -eq "j" -or $install -eq "y") {
    pip install -r requirements.txt
    Write-Host "🚀 Starte Streamlit..." -ForegroundColor Green
    streamlit run main.py
}
