"""
CloutScape AIO - Rewards and Economy System
Handles GP distribution, item rewards, and transaction history
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class TransactionType(Enum):
    """Transaction types"""
    REWARD = "reward"
    GAMBLE_WIN = "gamble_win"
    GAMBLE_LOSS = "gamble_loss"
    EVENT_PRIZE = "event_prize"
    PURCHASE = "purchase"
    TRANSFER = "transfer"
    ADMIN = "admin"

class RewardSystem:
    """Advanced rewards and economy system"""
    
    def __init__(self, config_file: str = 'rewards_config.json'):
        self.config_file = config_file
        self.balances: Dict[str, int] = {}
        self.inventory: Dict[str, List[Dict]] = {}
        self.transactions: List[Dict] = []
        self.load_config()
    
    def load_config(self):
        """Load rewards configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.balances = config.get('balances', {})
                self.inventory = config.get('inventory', {})
                self.transactions = config.get('transactions', [])
        except FileNotFoundError:
            self.balances = {}
            self.inventory = {}
            self.transactions = []
            self.save_config()
    
    def save_config(self):
        """Save rewards configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'balances': self.balances,
                    'inventory': self.inventory,
                    'transactions': self.transactions
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving rewards config: {e}")
    
    # ========================================================================
    # GP/Currency Management
    # ========================================================================
    
    def add_gp(self, player_id: str, player_name: str, amount: int, 
               reason: str, source_id: Optional[str] = None) -> Dict:
        """
        Add GP to player balance
        
        Args:
            player_id: Discord ID
            player_name: Player name
            amount: Amount to add
            reason: Reason for reward
            source_id: Source of reward (event ID, etc.)
        
        Returns:
            Transaction record
        """
        if player_id not in self.balances:
            self.balances[player_id] = 0
        
        self.balances[player_id] += amount
        
        transaction = {
            'id': f"txn_{len(self.transactions)}",
            'timestamp': datetime.now().isoformat(),
            'type': TransactionType.REWARD.value,
            'player_id': player_id,
            'player_name': player_name,
            'amount': amount,
            'reason': reason,
            'source_id': source_id,
            'new_balance': self.balances[player_id]
        }
        
        self.transactions.append(transaction)
        self.save_config()
        
        logger.info(f"Added {amount} GP to {player_name} ({player_id}): {reason}")
        return transaction
    
    def remove_gp(self, player_id: str, player_name: str, amount: int,
                  reason: str) -> Optional[Dict]:
        """Remove GP from player balance"""
        if player_id not in self.balances or self.balances[player_id] < amount:
            logger.warning(f"Insufficient GP for {player_name}: {amount}")
            return None
        
        self.balances[player_id] -= amount
        
        transaction = {
            'id': f"txn_{len(self.transactions)}",
            'timestamp': datetime.now().isoformat(),
            'type': TransactionType.GAMBLE_LOSS.value,
            'player_id': player_id,
            'player_name': player_name,
            'amount': -amount,
            'reason': reason,
            'new_balance': self.balances[player_id]
        }
        
        self.transactions.append(transaction)
        self.save_config()
        
        return transaction
    
    def transfer_gp(self, from_id: str, from_name: str, to_id: str, 
                    to_name: str, amount: int) -> bool:
        """Transfer GP between players"""
        if from_id not in self.balances or self.balances[from_id] < amount:
            return False
        
        self.balances[from_id] -= amount
        if to_id not in self.balances:
            self.balances[to_id] = 0
        self.balances[to_id] += amount
        
        transaction = {
            'id': f"txn_{len(self.transactions)}",
            'timestamp': datetime.now().isoformat(),
            'type': TransactionType.TRANSFER.value,
            'from_id': from_id,
            'from_name': from_name,
            'to_id': to_id,
            'to_name': to_name,
            'amount': amount
        }
        
        self.transactions.append(transaction)
        self.save_config()
        
        logger.info(f"Transferred {amount} GP from {from_name} to {to_name}")
        return True
    
    def get_balance(self, player_id: str) -> int:
        """Get player GP balance"""
        return self.balances.get(player_id, 0)
    
    # ========================================================================
    # Item Management
    # ========================================================================
    
    def add_item(self, player_id: str, item: Dict) -> bool:
        """
        Add item to player inventory
        
        Args:
            player_id: Discord ID
            item: Item dictionary with 'name', 'quantity', 'value', etc.
        
        Returns:
            Success status
        """
        if player_id not in self.inventory:
            self.inventory[player_id] = []
        
        # Check if item already exists
        for inv_item in self.inventory[player_id]:
            if inv_item['name'].lower() == item['name'].lower():
                inv_item['quantity'] += item.get('quantity', 1)
                self.save_config()
                return True
        
        # Add new item
        self.inventory[player_id].append({
            'name': item['name'],
            'quantity': item.get('quantity', 1),
            'value': item.get('value', 0),
            'rarity': item.get('rarity', 'common'),
            'added_at': datetime.now().isoformat()
        })
        
        self.save_config()
        return True
    
    def remove_item(self, player_id: str, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory"""
        if player_id not in self.inventory:
            return False
        
        for item in self.inventory[player_id]:
            if item['name'].lower() == item_name.lower():
                item['quantity'] -= quantity
                if item['quantity'] <= 0:
                    self.inventory[player_id].remove(item)
                self.save_config()
                return True
        
        return False
    
    def get_inventory(self, player_id: str) -> List[Dict]:
        """Get player inventory"""
        return self.inventory.get(player_id, [])
    
    def get_inventory_value(self, player_id: str) -> int:
        """Get total value of player inventory"""
        total = 0
        for item in self.get_inventory(player_id):
            total += item.get('value', 0) * item.get('quantity', 1)
        return total
    
    # ========================================================================
    # Transactions and History
    # ========================================================================
    
    def get_transaction_history(self, player_id: str, limit: int = 10) -> List[Dict]:
        """Get player transaction history"""
        player_txns = [t for t in self.transactions if t.get('player_id') == player_id]
        return sorted(player_txns, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_all_transactions(self, limit: int = 50) -> List[Dict]:
        """Get all transactions"""
        return sorted(self.transactions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    # ========================================================================
    # Leaderboards
    # ========================================================================
    
    def get_wealth_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get richest players"""
        players = []
        for player_id, balance in self.balances.items():
            inventory_value = self.get_inventory_value(player_id)
            players.append({
                'id': player_id,
                'gp': balance,
                'inventory_value': inventory_value,
                'total_wealth': balance + inventory_value
            })
        
        sorted_players = sorted(players, key=lambda x: x['total_wealth'], reverse=True)
        return sorted_players[:limit]
    
    def get_spending_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get biggest spenders"""
        spending = {}
        
        for txn in self.transactions:
            if txn['type'] in [TransactionType.GAMBLE_LOSS.value, TransactionType.PURCHASE.value]:
                player_id = txn.get('player_id')
                if player_id:
                    if player_id not in spending:
                        spending[player_id] = 0
                    spending[player_id] += abs(txn.get('amount', 0))
        
        sorted_spenders = sorted(spending.items(), key=lambda x: x[1], reverse=True)
        return [{'id': p_id, 'total_spent': amount} for p_id, amount in sorted_spenders[:limit]]
    
    # ========================================================================
    # Statistics
    # ========================================================================
    
    def get_economy_stats(self) -> Dict:
        """Get overall economy statistics"""
        total_gp = sum(self.balances.values())
        total_items = sum(len(inv) for inv in self.inventory.values())
        total_inventory_value = sum(self.get_inventory_value(p_id) for p_id in self.inventory.keys())
        
        return {
            'total_players': len(self.balances),
            'total_gp_in_circulation': total_gp,
            'total_items': total_items,
            'total_inventory_value': total_inventory_value,
            'total_wealth': total_gp + total_inventory_value,
            'average_balance': total_gp / max(1, len(self.balances)),
            'total_transactions': len(self.transactions)
        }
    
    def get_player_summary(self, player_id: str) -> Dict:
        """Get complete player economic summary"""
        return {
            'player_id': player_id,
            'gp_balance': self.get_balance(player_id),
            'inventory': self.get_inventory(player_id),
            'inventory_value': self.get_inventory_value(player_id),
            'total_wealth': self.get_balance(player_id) + self.get_inventory_value(player_id),
            'recent_transactions': self.get_transaction_history(player_id, 5)
        }
