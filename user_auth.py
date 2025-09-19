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
