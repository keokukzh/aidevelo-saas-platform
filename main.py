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
