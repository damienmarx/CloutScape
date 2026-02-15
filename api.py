#!/usr/bin/env python3
"""
CloutScape Backend API
Flask-based REST API for game state, economy, and player management
"""

import os
import json
import logging
from datetime import datetime
from functools import wraps
from typing import Dict, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS

from modules.rsps_integration import RSPSIntegration
from modules.gambling import GamblingSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    handlers=[
        logging.FileHandler(\'api.log\'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize systems
rsps = RSPSIntegration()
gambling = GamblingSystem()

# API Configuration
API_KEY = os.getenv(\'CLOUTSCAPE_API_KEY\', \'dev-key-change-in-production\')

# ============================================================================
# Authentication Middleware
# ============================================================================

def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get(\'X-API-Key\')
        if not api_key or api_key != API_KEY:
            return jsonify({\'error\': \'Unauthorized\'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Player Endpoints
# ============================================================================

@app.route(\'/api/players/<player_id>\', methods=[\'GET\'])
def get_player(player_id: str):
    """Get player profile and statistics"""
    try:
        account = rsps.get_player_stats(player_id)
        if not account:
            return jsonify({\'error\': \'Player not found\'}), 404
        return jsonify(account), 200
    except Exception as e:
        logger.error(f"Error getting player {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/players\', methods=[\'GET\'])
def list_players():
    """List all registered players"""
    try:
        players = rsps.get_all_players()
        return jsonify({\'players\': players, \'total\': len(players)}), 200
    except Exception as e:
        logger.error(f"Error listing players: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/players/<player_id>/balance\', methods=[\'GET\'])
def get_balance(player_id: str):
    """Get player\'s current GP balance"""
    try:
        account = rsps.get_account(player_id)
        if not account:
            return jsonify({\'error\': \'Player not found\'}), 404
        return jsonify({\'player_id\': player_id, \'balance\': account.get(\'gp_balance\', 0)}), 200
    except Exception as e:
        logger.error(f"Error getting balance for {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/players/<player_id>/balance\', methods=[\'POST\'])
@require_api_key
def update_balance(player_id: str):
    """Update player\'s GP balance (Admin only)"""
    try:
        data = request.get_json()
        action = data.get(\'action\')  # \'add\' or \'remove\'
        amount = data.get(\'amount\', 0)

        if not action or amount <= 0:
            return jsonify({\'error\': \'Invalid request\'}), 400

        if action == \'add\':
            rsps.add_gp(player_id, amount)
        elif action == \'remove\':
            rsps.remove_gp(player_id, amount)
        else:
            return jsonify({\'error\': \'Invalid action\'}), 400

        account = rsps.get_account(player_id)
        return jsonify({\'player_id\': player_id, \'balance\': account.get(\'gp_balance\', 0)}), 200
    except Exception as e:
        logger.error(f"Error updating balance for {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

# ============================================================================
# Leaderboard Endpoints
# ============================================================================

@app.route(\'/api/leaderboard/gp\', methods=[\'GET\'])
def leaderboard_gp():
    """Get GP leaderboard"""
    try:
        limit = request.args.get(\'limit\', 10, type=int)
        leaders = rsps.get_leaderboard(\'gp_balance\', limit)
        return jsonify({\'leaderboard\': leaders, \'type\': \'gp\'}), 200
    except Exception as e:
        logger.error(f"Error getting GP leaderboard: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/leaderboard/logins\', methods=[\'GET\'])
def leaderboard_logins():
    """Get login leaderboard"""
    try:
        limit = request.args.get(\'limit\', 10, type=int)
        leaders = rsps.get_leaderboard(\'total_logins\', limit)
        return jsonify({\'leaderboard\': leaders, \'type\': \'logins\'}), 200
    except Exception as e:
        logger.error(f"Error getting login leaderboard: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

# ============================================================================
# Gambling Endpoints
# ============================================================================

@app.route(\'/api/gambling/stats/<player_id>\', methods=[\'GET\'])
def get_gambling_stats(player_id: str):
    """Get player\'s gambling statistics"""
    try:
        stats = gambling.get_player_stats(player_id)
        if not stats:
            return jsonify({\'error\': \'No gambling stats found\'}), 404
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting gambling stats for {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/gambling/logs\', methods=[\'GET\'])
def get_gambling_logs():
    """Get recent gambling logs"""
    try:
        limit = request.args.get(\'limit\', 50, type=int)
        logs = gambling.get_recent_logs(limit)
        return jsonify({\'logs\': logs, \'total\': len(logs)}), 200
    except Exception as e:
        logger.error(f"Error getting gambling logs: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

# ============================================================================
# Server Status Endpoints
# ============================================================================

@app.route(\'/api/status\', methods=[\'GET\'])
def server_status():
    """Get RSPS server status"""
    try:
        status = rsps.get_server_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting server status: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/health\', methods=[\'GET\'])
def health_check():
    """Health check endpoint"""
    return jsonify({\'status\': \'ok\', \'timestamp\': datetime.now().isoformat()}), 200

# ============================================================================
# Admin Endpoints
# ============================================================================

@app.route(\'/api/admin/ban/<player_id>\', methods=[\'POST\'])
@require_api_key
def ban_player(player_id: str):
    """Ban a player (Admin only)"""
    try:
        data = request.get_json()
        reason = data.get(\'reason\', \'Violation of rules\')
        
        if rsps.ban_player(player_id, reason):
            return jsonify({\'status\': \'banned\', \'player_id\': player_id}), 200
        else:
            return jsonify({\'error\': \'Player not found\'}), 404
    except Exception as e:
        logger.error(f"Error banning player {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/admin/unban/<player_id>\', methods=[\'POST\'])
@require_api_key
def unban_player(player_id: str):
    """Unban a player (Admin only)"""
    try:
        if rsps.unban_player(player_id):
            return jsonify({\'status\': \'unbanned\', \'player_id\': player_id}), 200
        else:
            return jsonify({\'error\': \'Player not found\'}), 404
    except Exception as e:
        logger.error(f"Error unbanning player {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

@app.route(\'/api/admin/reset-password/<player_id>\', methods=[\'POST\'])
@require_api_key
def reset_password(player_id: str):
    """Reset a player\'s password (Admin only)"""
    try:
        new_password = rsps.reset_password(player_id)
        if new_password:
            return jsonify({\'status\': \'reset\', \'player_id\': player_id, \'new_password\': new_password}), 200
        else:
            return jsonify({\'error\': \'Player not found\'}), 404
    except Exception as e:
        logger.error(f"Error resetting password for {player_id}: {e}")
        return jsonify({\'error\': \'Internal server error\'}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({\'error\': \'Endpoint not found\'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({\'error\': \'Internal server error\'}), 500

# ============================================================================
# Main
# ============================================================================

def main():
    """Start the Flask API server"""
    debug = os.getenv(\'FLASK_DEBUG\', \'False\').lower() == \'true\'
    port = int(os.getenv(\'API_PORT\', 5000))
    host = os.getenv(\'API_HOST\', \'0.0.0.0\')
    
    logger.info(f"Starting CloutScape API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == \'__main__\':
    main()
