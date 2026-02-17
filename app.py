#!/usr/bin/env python3
"""
CloutScape AIO - Ultimate Gambling & RSPS Hub
Full Backend Implementation with Account Management, Chat, and Live Logs
"""

import os
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session
from modules.rsps_integration import RSPSIntegration

# ============================================================================
# Configuration
# ============================================================================

class WebConfig:
    """Web app configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'cloutscape-secret-key-2026')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'demo-token')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

# ============================================================================
# Initialization
# ============================================================================

app = Flask(__name__)
app.config.from_object(WebConfig)
Session(app)
CORS(app)

# Initialize RSPS Integration
rsps = RSPSIntegration()

# In-memory storage for real-time features (In production, use Redis/Database)
chat_history = []
live_bets = []
MAX_HISTORY = 50

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('web.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Utilities & Decorators
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session or session['admin_id'] != WebConfig.ADMIN_ID:
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Routes - Public & Pages
# ============================================================================

@app.route('/')
def index():
    """Main Gambling Hub"""
    return render_template('index.html')

@app.route('/setup')
def setup_page():
    return render_template('setup.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

# ============================================================================
# Authentication API
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    referral_code = data.get('referral_code')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
        
    web_id = f"web_{uuid.uuid4().hex[:8]}"
    result = rsps.register_player(web_id, "WebUser", username, referral_code)
    
    if result['success']:
        session['user_id'] = web_id
        session['username'] = username
        return jsonify({'success': True, 'message': 'Account created successfully'})
    else:
        return jsonify({'success': False, 'error': result.get('error', 'Registration failed')}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if rsps.authenticate_player(username, password):
        account = rsps.get_account_by_username(username)
        session['user_id'] = account['discord_id']
        session['username'] = username
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# Account & Wallet API
# ============================================================================

@app.route('/api/account/balance', methods=['GET'])
def get_balance():
    if 'username' not in session:
        return jsonify({'balance': 0, 'guest': True})
        
    account = rsps.get_account_by_username(session['username'])
    return jsonify({
        'balance': account.get('gp_balance', 0),
        'username': session['username'],
        'referral_code': account.get('referral_code'),
        'syndicate_tier': account.get('syndicate_tier', 'Recruit')
    })

@app.route('/api/syndicate/stats', methods=['GET'])
@login_required
def get_syndicate_stats():
    account = rsps.get_account(session['user_id'])
    # Count referrals
    referrals_count = 0
    for acc in rsps.accounts.values():
        if acc.get('referred_by') == session['user_id']:
            referrals_count += 1
            
    return jsonify({
        'tier': account.get('syndicate_tier', 'Recruit'),
        'trw': account.get('total_referred_wager', 0),
        'commissions': account.get('earned_commissions', 0),
        'referrals_count': referrals_count,
        'referral_code': account.get('referral_code')
    })

@app.route('/api/fairness/seeds', methods=['GET'])
@login_required
def get_fairness_seeds():
    account = rsps.get_account(session['user_id'])
    import hashlib
    server_seed_hash = hashlib.sha256(account['server_seed'].encode()).hexdigest()
    return jsonify({
        'server_seed_hash': server_seed_hash,
        'client_seed': account.get('client_seed', 'default'),
        'nonce': account.get('nonce', 0)
    })

@app.route('/api/fairness/update-client-seed', methods=['POST'])
@login_required
def update_client_seed():
    data = request.get_json()
    new_seed = data.get('client_seed')
    if not new_seed:
        return jsonify({'error': 'Seed required'}), 400
    
    account = rsps.get_account(session['user_id'])
    account['client_seed'] = new_seed
    account['nonce'] = 0 # Reset nonce on seed change
    rsps.save_accounts()
    return jsonify({'success': True})

@app.route('/api/account/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.get_json()
    amount = int(data.get('amount', 0))
    method = data.get('method', 'rsps')
    
    if amount <= 0:
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400
        
    # In a real app, this would interface with a payment gateway or RSPS bank
    rsps.add_gp(session['user_id'], amount)
    
    logger.info(f"Deposit: {session['username']} deposited {amount} via {method}")
    return jsonify({'success': True, 'new_balance': rsps.get_account(session['user_id'])['gp_balance']})

@app.route('/api/account/withdraw', methods=['POST'])
@login_required
def withdraw():
    data = request.get_json()
    amount = int(data.get('amount', 0))
    
    if amount <= 0:
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400
        
    if rsps.remove_gp(session['user_id'], amount):
        logger.info(f"Withdrawal: {session['username']} withdrew {amount}")
        return jsonify({'success': True, 'new_balance': rsps.get_account(session['user_id'])['gp_balance']})
        
    return jsonify({'success': False, 'error': 'Insufficient funds'}), 400

# ============================================================================
# Gambling & Real-time API
# ============================================================================

@app.route('/api/games/bet', methods=['POST'])
def place_bet():
    """
    Handles bet placement and result processing.
    In a production environment, the game logic should be server-side.
    """
    data = request.get_json()
    game = data.get('game')
    bet_amount = int(data.get('bet', 0))
    multiplier = float(data.get('multiplier', 0))
    payout = int(data.get('payout', 0))
    
    user = session.get('username', 'Guest')
    user_id = session.get('user_id')
    
    # If logged in, update actual balance
    if user_id:
        if payout > 0:
            rsps.add_gp(user_id, payout - bet_amount)
        else:
            rsps.remove_gp(user_id, bet_amount)
        
        # Process Syndicate Wager
        rsps.process_wager(user_id, bet_amount)
        
        # Increment Nonce for Provably Fair
        account = rsps.get_account(user_id)
        account['nonce'] = account.get('nonce', 0) + 1
        rsps.save_accounts()
            
    # Log the bet for the live feed
    bet_log = {
        'id': uuid.uuid4().hex[:6],
        'game': game,
        'user': user,
        'bet': bet_amount,
        'multiplier': multiplier,
        'payout': payout,
        'time': datetime.now().strftime('%H:%M:%S')
    }
    
    live_bets.insert(0, bet_log)
    if len(live_bets) > MAX_HISTORY:
        live_bets.pop()
        
    return jsonify({'success': True, 'bet': bet_log})

@app.route('/api/live/bets', methods=['GET'])
def get_live_bets():
    return jsonify(live_bets)

@app.route('/api/live/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        msg = data.get('message')
        user = session.get('username', 'Guest')
        
        if not msg:
            return jsonify({'error': 'Empty message'}), 400
            
        chat_msg = {
            'user': user,
            'message': msg,
            'time': datetime.now().strftime('%H:%M'),
            'color': 'text-blue-400' if user != 'Guest' else 'text-slate-500'
        }
        
        chat_history.append(chat_msg)
        if len(chat_history) > MAX_HISTORY:
            chat_history.pop(0)
            
        return jsonify(chat_msg)
        
    return jsonify(chat_history)

# ============================================================================
# Admin API
# ============================================================================

@app.route('/api/admin/stats')
@require_admin
def admin_stats():
    return jsonify({
        'total_users': len(rsps.accounts),
        'total_bets': len(live_bets),
        'server_status': rsps.get_server_status()
    })

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
