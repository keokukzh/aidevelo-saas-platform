#!/usr/bin/env python3
"""
SaaS Deployment Script
Automatisiert das Setup und Deployment Ihrer SaaS App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("📦 Installiere Python Abhängigkeiten...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Abhängigkeiten installiert")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei Installation: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env Datei nicht gefunden")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'STRIPE_SECRET_KEY' in content:
            print("✅ .env Datei konfiguriert")
            return True
    
    print("❌ .env Datei unvollständig")
    return False

def run_app():
    """Run the Streamlit app"""
    print("🚀 Starte SaaS Anwendung...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port=8501"])
    except KeyboardInterrupt:
        print("\n👋 Anwendung beendet")

def main():
    print("🎯 SaaS Deployment Script")
    print("=" * 30)
    
    # Check environment
    if not check_env_file():
        print("❌ Bitte .env Datei konfigurieren")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Installation fehlgeschlagen")
        return
    
    print("\n✅ Setup abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. Öffnen Sie http://localhost:8501 in Ihrem Browser")
    print("2. Registrieren Sie einen neuen Account")
    print("3. Testen Sie die Zahlungsintegration")
    print("4. Für Produktion: Domain konfigurieren und deployen")
    
    # Run app
    input("\nDrücken Sie Enter um die App zu starten...")
    run_app()

if __name__ == "__main__":
    main()
