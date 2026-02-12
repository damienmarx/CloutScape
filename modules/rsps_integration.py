#!/usr/bin/env python3
"""
RSPS Integration Module
Handles communication between Discord bot and RSPS server
"""

import json
import os
import hashlib
import random
import string
import socket
import struct
from typing import Optional, Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RSPSIntegration:
    """Manages RSPS server integration with Discord"""
    
    def __init__(self, server_host: str = "localhost", server_port: int = 43594):
        self.server_host = server_host
        self.server_port = server_port
        self.accounts_file = 'player_accounts.json'
        self.accounts = self.load_accounts()
        
    def load_accounts(self) -> Dict:
        """Load player accounts from file"""
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading accounts: {e}")
                return {}
        return {}
    
    def save_accounts(self):
        """Save player accounts to file"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            logger.info("Accounts saved successfully")
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def generate_password(self, length: int = 12) -> str:
        """Generate secure random password"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def hash_password(self, password: str) -> str:
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_player(self, discord_id: str, discord_name: str, username: str) -> Dict:
        """
        Register a new player account
        
        Args:
            discord_id: Discord user ID
            discord_name: Discord username
            username: In-game username
            
        Returns:
            Dict with account details or error
        """
        # Check if Discord ID already has an account
        if discord_id in self.accounts:
            return {
                'success': False,
                'error': 'You already have an account registered!',
                'username': self.accounts[discord_id]['username']
            }
        
        # Check if username is already taken
        for account in self.accounts.values():
            if account['username'].lower() == username.lower():
                return {
                    'success': False,
                    'error': 'Username is already taken!'
                }
        
        # Validate username
        if not self.validate_username(username):
            return {
                'success': False,
                'error': 'Invalid username! Use 3-12 alphanumeric characters.'
            }
        
        # Generate password
        password = self.generate_password()
        
        # Create account
        account = {
            'username': username,
            'password': password,
            'password_hash': self.hash_password(password),
            'discord_id': discord_id,
            'discord_name': discord_name,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'total_logins': 0,
            'is_banned': False,
            'is_admin': False,
            'gp_balance': 10000,  # Starting GP
            'rank': 'Member'
        }
        
        self.accounts[discord_id] = account
        self.save_accounts()
        
        logger.info(f"Registered new player: {username} (Discord: {discord_name})")
        
        return {
            'success': True,
            'username': username,
            'password': password,
            'message': 'Account created successfully!'
        }
    
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        if len(username) < 3 or len(username) > 12:
            return False
        if not username.replace('_', '').replace('-', '').isalnum():
            return False
        return True
    
    def get_account(self, discord_id: str) -> Optional[Dict]:
        """Get account by Discord ID"""
        return self.accounts.get(discord_id)
    
    def get_account_by_username(self, username: str) -> Optional[Dict]:
        """Get account by username"""
        for account in self.accounts.values():
            if account['username'].lower() == username.lower():
                return account
        return None
    
    def update_last_login(self, discord_id: str):
        """Update player's last login time"""
        if discord_id in self.accounts:
            self.accounts[discord_id]['last_login'] = datetime.now().isoformat()
            self.accounts[discord_id]['total_logins'] += 1
            self.save_accounts()
    
    def ban_player(self, discord_id: str, reason: str = "Violation of rules") -> bool:
        """Ban a player"""
        if discord_id in self.accounts:
            self.accounts[discord_id]['is_banned'] = True
            self.accounts[discord_id]['ban_reason'] = reason
            self.accounts[discord_id]['banned_at'] = datetime.now().isoformat()
            self.save_accounts()
            logger.info(f"Banned player: {self.accounts[discord_id]['username']}")
            return True
        return False
    
    def unban_player(self, discord_id: str) -> bool:
        """Unban a player"""
        if discord_id in self.accounts:
            self.accounts[discord_id]['is_banned'] = False
            self.accounts[discord_id]['unbanned_at'] = datetime.now().isoformat()
            self.save_accounts()
            logger.info(f"Unbanned player: {self.accounts[discord_id]['username']}")
            return True
        return False
    
    def add_gp(self, discord_id: str, amount: int) -> bool:
        """Add GP to player's balance"""
        if discord_id in self.accounts:
            self.accounts[discord_id]['gp_balance'] = self.accounts[discord_id].get('gp_balance', 0) + amount
            self.save_accounts()
            logger.info(f"Added {amount} GP to {self.accounts[discord_id]['username']}")
            return True
        return False
    
    def remove_gp(self, discord_id: str, amount: int) -> bool:
        """Remove GP from player's balance"""
        if discord_id in self.accounts:
            current_balance = self.accounts[discord_id].get('gp_balance', 0)
            if current_balance >= amount:
                self.accounts[discord_id]['gp_balance'] = current_balance - amount
                self.save_accounts()
                logger.info(f"Removed {amount} GP from {self.accounts[discord_id]['username']}")
                return True
        return False
    
    def set_rank(self, discord_id: str, rank: str) -> bool:
        """Set player's rank"""
        if discord_id in self.accounts:
            self.accounts[discord_id]['rank'] = rank
            self.save_accounts()
            logger.info(f"Set rank {rank} for {self.accounts[discord_id]['username']}")
            return True
        return False
    
    def get_online_players(self) -> List[str]:
        """
        Get list of online players from RSPS server
        This would connect to the actual server in production
        """
        # TODO: Implement actual server connection
        # For now, return empty list
        return []
    
    def send_server_command(self, command: str) -> bool:
        """
        Send command to RSPS server
        This would use socket connection in production
        """
        # TODO: Implement actual server communication
        logger.info(f"Would send command to server: {command}")
        return True
    
    def get_player_stats(self, discord_id: str) -> Optional[Dict]:
        """Get player statistics"""
        account = self.get_account(discord_id)
        if not account:
            return None
        
        return {
            'username': account['username'],
            'rank': account.get('rank', 'Member'),
            'gp_balance': account.get('gp_balance', 0),
            'total_logins': account.get('total_logins', 0),
            'last_login': account.get('last_login', 'Never'),
            'created_at': account.get('created_at', 'Unknown'),
            'is_banned': account.get('is_banned', False)
        }
    
    def get_all_players(self) -> List[Dict]:
        """Get all registered players"""
        players = []
        for discord_id, account in self.accounts.items():
            players.append({
                'discord_id': discord_id,
                'username': account['username'],
                'rank': account.get('rank', 'Member'),
                'gp_balance': account.get('gp_balance', 0),
                'total_logins': account.get('total_logins', 0),
                'is_banned': account.get('is_banned', False)
            })
        return players
    
    def get_leaderboard(self, sort_by: str = 'gp_balance', limit: int = 10) -> List[Dict]:
        """
        Get player leaderboard
        
        Args:
            sort_by: Field to sort by (gp_balance, total_logins)
            limit: Number of players to return
        """
        players = self.get_all_players()
        
        # Filter out banned players
        players = [p for p in players if not p.get('is_banned', False)]
        
        # Sort by specified field
        players.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
        
        return players[:limit]
    
    def reset_password(self, discord_id: str) -> Optional[str]:
        """Reset player's password"""
        if discord_id in self.accounts:
            new_password = self.generate_password()
            self.accounts[discord_id]['password'] = new_password
            self.accounts[discord_id]['password_hash'] = self.hash_password(new_password)
            self.save_accounts()
            logger.info(f"Reset password for {self.accounts[discord_id]['username']}")
            return new_password
        return None
    
    def delete_account(self, discord_id: str) -> bool:
        """Delete a player account"""
        if discord_id in self.accounts:
            username = self.accounts[discord_id]['username']
            del self.accounts[discord_id]
            self.save_accounts()
            logger.info(f"Deleted account: {username}")
            return True
        return False
    
    def get_server_status(self) -> Dict:
        """Get RSPS server status"""
        # TODO: Implement actual server status check
        return {
            'online': True,
            'players_online': 0,
            'uptime': '0h 0m',
            'version': '317',
            'max_players': 100
        }
    
    def authenticate_player(self, username: str, password: str) -> bool:
        """Authenticate player login"""
        account = self.get_account_by_username(username)
        if not account:
            return False
        
        if account.get('is_banned', False):
            return False
        
        password_hash = self.hash_password(password)
        return password_hash == account.get('password_hash', '')
    
    def log_game_event(self, event_type: str, data: Dict):
        """Log game events for Discord notifications"""
        event = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to events file for webhook processing
        events_file = 'game_events.json'
        events = []
        
        if os.path.exists(events_file):
            try:
                with open(events_file, 'r') as f:
                    events = json.load(f)
            except:
                events = []
        
        events.append(event)
        
        # Keep only last 100 events
        events = events[-100:]
        
        with open(events_file, 'w') as f:
            json.dump(events, f, indent=2)
        
        logger.info(f"Logged game event: {event_type}")
