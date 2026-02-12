#!/usr/bin/env python3
"""
CloutScape AIO - Discord Setup Bot Web App
Flask web interface for bot management and monitoring
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List
from functools import wraps
import requests

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session
import discord
from discord.ext import commands

# ============================================================================
# Configuration
# ============================================================================

class WebConfig:
    """Web app configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    BOT_INVITE_URL = os.getenv('BOT_INVITE_URL', 'https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

# ============================================================================
# Logging
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Flask App
# ============================================================================

app = Flask(__name__)
app.config.from_object(WebConfig)
Session(app)
CORS(app)

# ============================================================================
# Utilities
# ============================================================================

def load_server_configs() -> Dict:
    """Load server configurations from file"""
    config_file = 'server_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading configs: {e}")
    return {}

def get_bot_stats() -> Dict:
    """Get bot statistics"""
    configs = load_server_configs()
    
    return {
        'total_servers': len(configs),
        'total_channels': sum(c.get('channels', 0) for c in configs.values()),
        'total_roles': sum(c.get('roles', 0) for c in configs.values()),
        'setup_date': datetime.now().isoformat()
    }

def require_admin(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session or session['admin_id'] != WebConfig.ADMIN_ID:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Routes - Public
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    stats = get_bot_stats()
    return render_template('index.html', stats=stats)

@app.route('/setup')
def setup_page():
    """Setup page"""
    return render_template('setup.html', bot_invite_url=WebConfig.BOT_INVITE_URL)

@app.route('/docs')
def docs():
    """Documentation page"""
    return render_template('docs.html')

# ============================================================================
# Routes - Admin
# ============================================================================

@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/api/admin/login', methods=['POST'])
def admin_login_api():
    """Admin login API"""
    data = request.get_json()
    admin_id = data.get('admin_id')
    token = data.get('token')
    
    if not admin_id or not token:
        return jsonify({'error': 'Missing credentials'}), 400
    
    try:
        admin_id = int(admin_id)
    except ValueError:
        return jsonify({'error': 'Invalid admin ID'}), 400
    
    # Verify credentials (in production, use proper auth)
    if admin_id == WebConfig.ADMIN_ID and token == WebConfig.DISCORD_TOKEN:
        session['admin_id'] = admin_id
        session.permanent = True
        return jsonify({'success': True, 'redirect': '/admin/dashboard'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/admin/dashboard')
@require_admin
def admin_dashboard():
    """Admin dashboard"""
    stats = get_bot_stats()
    configs = load_server_configs()
    return render_template('admin_dashboard.html', stats=stats, servers=configs)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# API Routes - Admin
# ============================================================================

@app.route('/api/admin/stats', methods=['GET'])
@require_admin
def api_stats():
    """Get bot statistics"""
    stats = get_bot_stats()
    return jsonify(stats)

@app.route('/api/admin/servers', methods=['GET'])
@require_admin
def api_servers():
    """Get all configured servers"""
    configs = load_server_configs()
    
    servers = []
    for guild_id, config in configs.items():
        servers.append({
            'id': guild_id,
            'name': config.get('guild_name', 'Unknown'),
            'channels': config.get('channels', 0),
            'roles': config.get('roles', 0),
            'setup_date': config.get('setup_date', 'Unknown'),
            'status': config.get('status', 'unknown')
        })
    
    return jsonify(servers)

@app.route('/api/admin/server/<guild_id>', methods=['GET'])
@require_admin
def api_server_details(guild_id):
    """Get server details"""
    configs = load_server_configs()
    
    if guild_id not in configs:
        return jsonify({'error': 'Server not found'}), 404
    
    return jsonify(configs[guild_id])

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@require_admin
def api_settings():
    """Get or update bot settings"""
    settings_file = 'bot_settings.json'
    
    if request.method == 'GET':
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        else:
            settings = {}
        return jsonify(settings)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        try:
            with open(settings_file, 'w') as f:
                json.dump(data, f, indent=2)
            return jsonify({'success': True, 'message': 'Settings updated'})
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return jsonify({'error': str(e)}), 500

# ============================================================================
# API Routes - Public
# ============================================================================

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get bot status"""
    stats = get_bot_stats()
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'stats': stats
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """Get bot information"""
    return jsonify({
        'name': 'CloutScape AIO Discord Setup Bot',
        'version': '1.0.0',
        'description': 'Automated Discord server configuration for CloutScape AIO',
        'features': [
            'Auto-create channels',
            'Auto-create roles',
            'Set permissions',
            'Save configuration',
            'Web management'
        ]
    })

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
# Template Rendering
# ============================================================================

@app.context_processor
def inject_config():
    """Inject configuration into templates"""
    return {
        'app_name': 'CloutScape AIO Setup Bot',
        'app_version': '1.0.0',
        'current_year': datetime.now().year
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run app
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=debug
    )
