#!/usr/bin/env python3
"""
API Server for aidevelo.co
Provides REST API endpoints for the SaaS platform
"""

from flask import Flask, request, jsonify
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "AiDevelo.co API Server",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "pricing": "/api/pricing",
            "webhook": "/api/webhook/stripe"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"})

@app.route('/api/pricing')
def pricing():
    return jsonify({
        "plans": {
            "free": {"price": 0, "features": ["10 AI queries/month"]},
            "basic": {"price": 9.99, "features": ["100 AI queries/month", "Basic analytics"]},
            "pro": {"price": 29.99, "features": ["1000 AI queries/month", "Advanced analytics"]},
            "enterprise": {"price": 99.99, "features": ["Unlimited queries", "Custom features"]}
        }
    })

@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
        
        if event['type'] == 'checkout.session.completed':
            # Handle successful payment
            session = event['data']['object']
            # Update user subscription in database
            pass
            
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8503, debug=False)