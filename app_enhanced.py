"""
CloutScape AIO - Enhanced Web App with Advanced Features
Flask web interface with gambling, PvP, events, and rewards management
"""

import os
import json
import logging
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session

from modules.gambling import GamblingSystem
from modules.pvp import PvPSystem
from modules.events import EventSystem
from modules.rewards import RewardSystem
from modules.webhooks import WebhookManager

# ============================================================================
# Configuration
# ============================================================================

class EnhancedConfig:
    """Enhanced web app configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 86400

# ============================================================================
# Logging
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Flask App
# ============================================================================

app = Flask(__name__)
app.config.from_object(EnhancedConfig)
Session(app)
CORS(app)

# ============================================================================
# Initialize Systems
# ============================================================================

gambling_system = GamblingSystem()
pvp_system = PvPSystem()
event_system = EventSystem()
reward_system = RewardSystem()
webhook_manager = WebhookManager()

# ============================================================================
# Utilities
# ============================================================================

def require_admin(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session or session['admin_id'] != EnhancedConfig.ADMIN_ID:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Routes - Gambling
# ============================================================================

@app.route('/api/gambling/stats', methods=['GET'])
def api_gambling_stats():
    """Get gambling statistics"""
    stats = gambling_system.get_statistics()
    return jsonify(stats)

@app.route('/api/gambling/leaderboard', methods=['GET'])
def api_gambling_leaderboard():
    """Get gambling leaderboard"""
    sort_by = request.args.get('sort_by', 'total_profit')
    limit = int(request.args.get('limit', 10))
    
    leaderboard = gambling_system.get_leaderboard(limit, sort_by)
    return jsonify(leaderboard)

@app.route('/api/gambling/recent', methods=['GET'])
def api_gambling_recent():
    """Get recent gambling games"""
    limit = int(request.args.get('limit', 10))
    game_type = request.args.get('game_type')
    
    games = gambling_system.get_recent_games(limit, game_type)
    return jsonify(games)

@app.route('/api/gambling/player/<player_id>', methods=['GET'])
def api_gambling_player(player_id):
    """Get player gambling statistics"""
    stats = gambling_system.get_player_stats(player_id)
    if not stats:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(stats)

# ============================================================================
# Routes - PvP
# ============================================================================

@app.route('/api/pvp/stats', methods=['GET'])
def api_pvp_stats():
    """Get PvP statistics"""
    stats = pvp_system.get_statistics()
    return jsonify(stats)

@app.route('/api/pvp/leaderboard', methods=['GET'])
def api_pvp_leaderboard():
    """Get PvP leaderboard"""
    sort_by = request.args.get('sort_by', 'kills')
    limit = int(request.args.get('limit', 10))
    
    leaderboard = pvp_system.get_leaderboard(limit, sort_by)
    return jsonify(leaderboard)

@app.route('/api/pvp/recent', methods=['GET'])
def api_pvp_recent():
    """Get recent PvP kills"""
    limit = int(request.args.get('limit', 10))
    player_id = request.args.get('player_id')
    
    kills = pvp_system.get_recent_kills(limit, player_id)
    return jsonify(kills)

@app.route('/api/pvp/hotspots', methods=['GET'])
def api_pvp_hotspots():
    """Get kill hotspots"""
    limit = int(request.args.get('limit', 5))
    hotspots = pvp_system.get_kill_hotspots(limit)
    return jsonify(hotspots)

@app.route('/api/pvp/player/<player_id>', methods=['GET'])
def api_pvp_player(player_id):
    """Get player PvP statistics"""
    stats = pvp_system.get_player_stats(player_id)
    if not stats:
        return jsonify({'error': 'Player not found'}), 404
    return jsonify(stats)

# ============================================================================
# Routes - Events
# ============================================================================

@app.route('/api/events/stats', methods=['GET'])
def api_events_stats():
    """Get event statistics"""
    stats = event_system.get_event_stats()
    return jsonify(stats)

@app.route('/api/events/active', methods=['GET'])
def api_events_active():
    """Get active events"""
    events = event_system.get_active_events()
    return jsonify(events)

@app.route('/api/events/completed', methods=['GET'])
def api_events_completed():
    """Get completed events"""
    limit = int(request.args.get('limit', 10))
    events = event_system.get_completed_events(limit)
    return jsonify(events)

@app.route('/api/events/leaderboard', methods=['GET'])
def api_events_leaderboard():
    """Get event participation leaderboard"""
    limit = int(request.args.get('limit', 10))
    leaderboard = event_system.get_leaderboard(limit)
    return jsonify(leaderboard)

@app.route('/api/events/<event_id>', methods=['GET'])
def api_event_details(event_id):
    """Get event details"""
    event = event_system.get_event(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify(event)

# ============================================================================
# Routes - Rewards
# ============================================================================

@app.route('/api/rewards/stats', methods=['GET'])
def api_rewards_stats():
    """Get economy statistics"""
    stats = reward_system.get_economy_stats()
    return jsonify(stats)

@app.route('/api/rewards/leaderboard/wealth', methods=['GET'])
def api_rewards_wealth_leaderboard():
    """Get wealth leaderboard"""
    limit = int(request.args.get('limit', 10))
    leaderboard = reward_system.get_wealth_leaderboard(limit)
    return jsonify(leaderboard)

@app.route('/api/rewards/leaderboard/spending', methods=['GET'])
def api_rewards_spending_leaderboard():
    """Get spending leaderboard"""
    limit = int(request.args.get('limit', 10))
    leaderboard = reward_system.get_spending_leaderboard(limit)
    return jsonify(leaderboard)

@app.route('/api/rewards/player/<player_id>', methods=['GET'])
def api_rewards_player(player_id):
    """Get player reward summary"""
    summary = reward_system.get_player_summary(player_id)
    return jsonify(summary)

@app.route('/api/rewards/transactions', methods=['GET'])
def api_rewards_transactions():
    """Get transaction history"""
    limit = int(request.args.get('limit', 50))
    player_id = request.args.get('player_id')
    
    if player_id:
        transactions = reward_system.get_transaction_history(player_id, limit)
    else:
        transactions = reward_system.get_all_transactions(limit)
    
    return jsonify(transactions)

# ============================================================================
# Routes - Admin
# ============================================================================

@app.route('/api/admin/webhooks', methods=['GET', 'POST'])
@require_admin
def api_admin_webhooks():
    """Get or set webhook URLs"""
    if request.method == 'GET':
        return jsonify(webhook_manager.webhooks)
    
    elif request.method == 'POST':
        data = request.get_json()
        webhook_type = data.get('type')
        url = data.get('url')
        
        if webhook_manager.set_webhook(webhook_type, url):
            return jsonify({'success': True, 'message': f'Webhook set for {webhook_type}'})
        else:
            return jsonify({'error': 'Invalid webhook URL'}), 400

@app.route('/api/admin/reset/<system>', methods=['POST'])
@require_admin
def api_admin_reset(system):
    """Reset system data"""
    if system == 'gambling':
        gambling_system.logs = []
        gambling_system.player_stats = {}
        gambling_system.save_config()
        return jsonify({'success': True, 'message': 'Gambling system reset'})
    
    elif system == 'pvp':
        pvp_system.kills = []
        pvp_system.player_stats = {}
        pvp_system.save_config()
        return jsonify({'success': True, 'message': 'PvP system reset'})
    
    elif system == 'events':
        event_system.events = {}
        event_system.save_config()
        return jsonify({'success': True, 'message': 'Events system reset'})
    
    elif system == 'rewards':
        reward_system.balances = {}
        reward_system.inventory = {}
        reward_system.transactions = []
        reward_system.save_config()
        return jsonify({'success': True, 'message': 'Rewards system reset'})
    
    return jsonify({'error': 'Unknown system'}), 400

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=debug
    )
