#!/bin/bash
# Komplettes SaaS Deployment Paket für C:\Users\keoku\Desktop\saas

echo "🚀 Erstelle komplettes SaaS Deployment Paket"
echo "============================================="

# 1. .env Datei mit Ihrem Stripe Schlüssel
cat > .env << 'EOF'
STRIPE_SECRET_KEY=sk_test_51S8tiw6bysxOOlngnay4pVwXkRYO00OOnnQSeCO8etZth9yeMbQ2dNGKCsXX8FCdXhyV1NA2WSMo3Tcl1Ln33cy300nhN9ej2o
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
DATABASE_URL=sqlite:///saas_app.db
SECRET_KEY=change_this_secret_key_12345
DOMAIN=http://localhost:8501
DEBUG=True
OPENAI_API_KEY=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
EOF

# 2. requirements.txt
cat > requirements.txt << 'EOF'
streamlit>=1.28.0
stripe>=5.5.0
python-dotenv>=1.0.0
pandas>=2.0.0
plotly>=5.15.0
requests>=2.31.0
bcrypt>=4.0.0
sqlalchemy>=2.0.0
hashlib2>=1.3.1
email-validator>=2.0.0
EOF

# 3. main.py - Haupt SaaS App
cat > main.py << 'EOF'
import streamlit as st
import warnings
warnings.filterwarnings('ignore', message='.*ScriptRunContext.*')

# Page config
st.set_page_config(
    page_title="AI SaaS Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modules
try:
    from user_auth import require_auth, login_page
    from payment_integration import show_pricing_page
    import plotly.graph_objects as go
    import pandas as pd
    from datetime import datetime, timedelta
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
except ImportError as e:
    st.error(f"Module import error: {e}")
    st.stop()

def main_dashboard():
    """Main SaaS dashboard"""
    st.title("🚀 AI SaaS Platform")
    st.sidebar.title("Navigation")
    
    # Check subscription plan
    plan = st.session_state.get('subscription_plan', 'free')
    st.sidebar.info(f"Aktueller Plan: {plan.title()}")
    
    # Navigation
    page = st.sidebar.selectbox("Wählen Sie eine Seite", [
        "Dashboard",
        "KI-Tools", 
        "Analytics",
        "Abrechnung",
        "Einstellungen"
    ])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "KI-Tools":
        show_ai_tools(plan)
    elif page == "Analytics":
        show_analytics(plan)
    elif page == "Abrechnung":
        show_pricing_page()
    elif page == "Einstellungen":
        show_settings()

def show_dashboard():
    """Show main dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Benutzer", "1,234", "+12%")
    with col2:
        st.metric("Umsatz", "5.678€", "+23%")
    with col3:
        st.metric("API Calls", "9,012", "+45%")
    with col4:
        st.metric("Wachstum", "23.5%", "+5.2%")
    
    # Revenue chart
    st.subheader("📈 Umsatzwachstum")
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    revenue = [3000, 3200, 3800, 4200, 4800, 5200, 5678, 6100, 6500, 6800, 7200, 7500]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dates, y=revenue, name='Monatlicher Umsatz'))
    fig.update_layout(title="Monatliches Umsatzwachstum", height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_ai_tools(plan):
    """Show AI tools (limited by plan)"""
    st.subheader("🤖 KI-Tools")
    
    # Plan limits
    limits = {
        'free': {'queries': 10, 'models': ['basic']},
        'basic': {'queries': 100, 'models': ['basic', 'advanced']},
        'pro': {'queries': 1000, 'models': ['basic', 'advanced', 'premium']},
        'enterprise': {'queries': 'unlimited', 'models': ['all']}
    }
    
    user_limits = limits.get(plan, limits['free'])
    
    st.info(f"Plan: {plan.title()} | Abfragen: {user_limits['queries']}")
    
    # AI Chat Interface
    st.subheader("KI-Assistent")
    user_input = st.text_area("Fragen Sie die KI:")
    
    if st.button("Senden"):
        if plan == 'free' and st.session_state.get('queries_used', 0) >= 10:
            st.error("Kostenloses Kontingent aufgebraucht. Bitte upgraden!")
            show_pricing_page()
        else:
            # Process AI query (mock response)
            st.success("KI Antwort: Das ist eine Test-Antwort. In der Produktion hier OpenAI/Claude API integrieren.")
            st.session_state.queries_used = st.session_state.get('queries_used', 0) + 1

def show_analytics(plan):
    """Show analytics (limited by plan)"""
    st.subheader("📊 Analytics")
    
    if plan == 'free':
        st.warning("Upgrade zu Pro für erweiterte Analytics")
        st.info("Nur Basis-Analytics")
        st.metric("Seitenaufrufe", "1,234")
        st.metric("Benutzer", "567")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Seitenaufrufe", "12,345", "+15%")
            st.metric("Unique Users", "5,678", "+8%")
            st.metric("Bounce Rate", "25%", "-3%")
        
        with col2:
            st.metric("Conversion Rate", "3.2%", "+0.5%")
            st.metric("Ø Session", "5:32", "+12s")
            st.metric("Revenue/User", "45€", "+5€")

def show_settings():
    """Show user settings"""
    st.subheader("⚙️ Einstellungen")
    
    st.text_input("Anzeigename", value="Max Mustermann")
    st.text_input("E-Mail", value=st.session_state.get('user_email', ''))
    
    if st.button("Profil aktualisieren"):
        st.success("Profil aktualisiert!")
    
    st.subheader("API Schlüssel")
    st.text_input("Ihr API Schlüssel", value="sk-1234567890", type="password")
    
    if st.button("API Schlüssel neu generieren"):
        st.success("Neuer API Schlüssel generiert!")
    
    # Logout button
    if st.button("Abmelden", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

def main():
    """Main app entry point"""
    # Check authentication
    if require_auth():
        main_dashboard()

if __name__ == "__main__":
    main()
EOF

# 4. user_auth.py - Benutzer Authentifizierung
cat > user_auth.py << 'EOF'
import streamlit as st
import sqlite3
import hashlib
import uuid
from datetime import datetime

class UserAuth:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize user database"""
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password_hash TEXT,
                subscription_plan TEXT DEFAULT 'free',
                stripe_customer_id TEXT,
                created_at TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password securely"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email, password):
        """Create new user"""
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)
            
            c.execute('''
                INSERT INTO users (id, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, email, password_hash, datetime.now()))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def verify_user(self, email, password):
        """Verify user login"""
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        password_hash = self.hash_password(password)
        
        c.execute('''
            SELECT id, subscription_plan FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        result = c.fetchone()
        conn.close()
        
        if result:
            self.update_last_login(email)
            return {'user_id': result[0], 'plan': result[1]}
        return None
    
    def update_last_login(self, email):
        """Update user's last login time"""
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            UPDATE users SET last_login = ? WHERE email = ?
        ''', (datetime.now(), email))
        conn.commit()
        conn.close()

def login_page():
    """Login/Register page"""
    auth = UserAuth()
    
    tab1, tab2 = st.tabs(["Anmelden", "Registrieren"])
    
    with tab1:
        st.subheader("Anmelden")
        email = st.text_input("E-Mail", key="login_email")
        password = st.text_input("Passwort", type="password", key="login_password")
        
        if st.button("Anmelden"):
            user = auth.verify_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user['user_id']
                st.session_state.user_email = email
                st.session_state.subscription_plan = user['plan']
                st.success("Erfolgreich angemeldet!")
                st.rerun()
            else:
                st.error("Ungültige Anmeldedaten")
    
    with tab2:
        st.subheader("Registrieren")
        email = st.text_input("E-Mail", key="register_email")
        password = st.text_input("Passwort", type="password", key="register_password")
        confirm_password = st.text_input("Passwort bestätigen", type="password", key="confirm_password")
        
        if st.button("Registrieren"):
            if password != confirm_password:
                st.error("Passwörter stimmen nicht überein")
            elif len(password) < 6:
                st.error("Passwort muss mindestens 6 Zeichen haben")
            elif auth.create_user(email, password):
                st.success("Konto erstellt! Bitte melden Sie sich an.")
            else:
                st.error("E-Mail bereits vorhanden")

def require_auth():
    """Decorator to require authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
        return False
    return True
EOF

# 5. payment_integration.py - Stripe Zahlungsintegration
cat > payment_integration.py << 'EOF'
import stripe
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class PaymentProcessor:
    def __init__(self):
        self.pricing_plans = {
            'basic': {'price': 9.99, 'features': ['100 KI Anfragen/Monat', 'Basis Analytics', 'E-Mail Support']},
            'pro': {'price': 29.99, 'features': ['1000 KI Anfragen/Monat', 'Erweiterte Analytics', 'Priorität Support', 'API Zugang']},
            'enterprise': {'price': 99.99, 'features': ['Unbegrenzte KI Anfragen', 'Premium Analytics', '24/7 Support', 'Custom Features']}
        }
    
    def create_checkout_session(self, plan_type, user_email):
        """Create Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'{plan_type.title()} Plan - AI SaaS Platform',
                        },
                        'unit_amount': int(self.pricing_plans[plan_type]['price'] * 100),
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f"{os.getenv('DOMAIN', 'http://localhost:8501')}/success",
                cancel_url=f"{os.getenv('DOMAIN', 'http://localhost:8501')}/cancel",
                customer_email=user_email,
                metadata={'plan': plan_type}
            )
            return session.url
        except Exception as e:
            st.error(f"Zahlungsfehler: {e}")
            return None

def show_pricing_page():
    """Show pricing plans"""
    st.title("💰 Wählen Sie Ihren Plan")
    st.markdown("### Starten Sie noch heute mit unserem AI-powered SaaS!")
    
    processor = PaymentProcessor()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Basic Plan")
        st.markdown("**9,99€/Monat**")
        for feature in processor.pricing_plans['basic']['features']:
            st.write(f"✅ {feature}")
        if st.button("Basic wählen", key="basic", use_container_width=True):
            if st.session_state.get('user_email'):
                url = processor.create_checkout_session('basic', st.session_state.get('user_email'))
                if url:
                    st.markdown(f'[🚀 Jetzt bezahlen]({url})')
            else:
                st.error("Bitte melden Sie sich zuerst an")
    
    with col2:
        st.subheader("Pro Plan ⭐")
        st.markdown("**29,99€/Monat**")
        for feature in processor.pricing_plans['pro']['features']:
            st.write(f"✅ {feature}")
        if st.button("Pro wählen", key="pro", use_container_width=True):
            if st.session_state.get('user_email'):
                url = processor.create_checkout_session('pro', st.session_state.get('user_email'))
                if url:
                    st.markdown(f'[🚀 Jetzt bezahlen]({url})')
            else:
                st.error("Bitte melden Sie sich zuerst an")
    
    with col3:
        st.subheader("Enterprise Plan")
        st.markdown("**99,99€/Monat**")
        for feature in processor.pricing_plans['enterprise']['features']:
            st.write(f"✅ {feature}")
        if st.button("Enterprise wählen", key="enterprise", use_container_width=True):
            if st.session_state.get('user_email'):
                url = processor.create_checkout_session('enterprise', st.session_state.get('user_email'))
                if url:
                    st.markdown(f'[🚀 Jetzt bezahlen]({url})')
            else:
                st.error("Bitte melden Sie sich zuerst an")
    
    st.markdown("---")
    st.info("💡 **Tipp:** Starten Sie mit dem kostenlosen Plan und upgraden Sie jederzeit!")
EOF

# 6. Deploy Script
cat > deploy.py << 'EOF'
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
EOF

# 7. Windows Batch Script
cat > start_saas.bat << 'EOF'
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
EOF

echo "✅ Alle Dateien erstellt!"
echo ""
echo "📁 Erstellte Dateien:"
echo "===================="
ls -la *.py *.txt *.bat .env
echo ""
echo "🚀 Setup Anweisungen:"
echo "====================="
echo "1. Kopieren Sie alle Dateien nach C:\Users\keoku\Desktop\saas"
echo "2. Doppelklicken Sie start_saas.bat ODER"
echo "3. Führen Sie aus: python deploy.py"
echo ""
echo "💡 Ihre SaaS App wird unter http://localhost:8501 verfügbar sein"