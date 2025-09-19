@echo off
echo 🚀 SaaS Platform Starter
echo ========================
echo.

REM Set UTF-8 encoding
chcp 65001 > nul

echo Prüfe Python Installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python nicht gefunden. Bitte installieren Sie Python.
    pause
    exit /b 1
)

echo ✅ Python gefunden
echo.

echo Installiere Abhängigkeiten...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Installation fehlgeschlagen
    pause
    exit /b 1
)

echo ✅ Abhängigkeiten installiert
echo.

echo 🚀 Starte SaaS Anwendung...
echo Öffnen Sie http://localhost:8501 in Ihrem Browser
echo.

streamlit run main.py

pause
