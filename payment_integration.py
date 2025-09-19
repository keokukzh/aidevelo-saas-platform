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
