"""
CloutScape AIO - PvP Tracking System
Handles kill logs, loot tracking, and PvP statistics
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PvPSystem:
    """Advanced PvP tracking system"""
    
    def __init__(self, config_file: str = 'pvp_config.json'):
        self.config_file = config_file
        self.kills: List[Dict] = []
        self.player_stats: Dict = {}
        self.load_config()
    
    def load_config(self):
        """Load PvP configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.kills = config.get('kills', [])
                self.player_stats = config.get('stats', {})
        except FileNotFoundError:
            self.kills = []
            self.player_stats = {}
            self.save_config()
    
    def save_config(self):
        """Save PvP configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'kills': self.kills,
                    'stats': self.player_stats
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving PvP config: {e}")
    
    def log_kill(self, killer_id: str, killer_name: str, victim_id: str, 
                 victim_name: str, location: str, loot: List[Dict],
                 weapon: str = "Unknown") -> Dict:
        """
        Log a PvP kill
        
        Args:
            killer_id: Discord ID of killer
            killer_name: Name of killer
            victim_id: Discord ID of victim
            victim_name: Name of victim
            location: Location of kill (e.g., "Duel Arena", "Wilderness")
            loot: List of items dropped
            weapon: Weapon used
        
        Returns:
            Kill log entry
        """
        loot_value = sum(item.get('value', 0) for item in loot)
        
        kill_entry = {
            'timestamp': datetime.now().isoformat(),
            'killer_id': killer_id,
            'killer_name': killer_name,
            'victim_id': victim_id,
            'victim_name': victim_name,
            'location': location,
            'weapon': weapon,
            'loot': loot,
            'loot_value': loot_value
        }
        
        self.kills.append(kill_entry)
        self._update_player_stats(killer_id, killer_name, victim_id, victim_name, loot_value)
        self.save_config()
        
        return kill_entry
    
    def _update_player_stats(self, killer_id: str, killer_name: str, 
                            victim_id: str, victim_name: str, loot_value: int):
        """Update player PvP statistics"""
        # Update killer stats
        if killer_id not in self.player_stats:
            self.player_stats[killer_id] = {
                'name': killer_name,
                'kills': 0,
                'deaths': 0,
                'kd_ratio': 0.0,
                'total_loot': 0,
                'average_loot': 0,
                'kill_streak': 0,
                'best_kill_streak': 0
            }
        
        killer_stats = self.player_stats[killer_id]
        killer_stats['kills'] += 1
        killer_stats['total_loot'] += loot_value
        killer_stats['average_loot'] = killer_stats['total_loot'] / killer_stats['kills']
        killer_stats['kill_streak'] += 1
        
        if killer_stats['kill_streak'] > killer_stats['best_kill_streak']:
            killer_stats['best_kill_streak'] = killer_stats['kill_streak']
        
        killer_stats['kd_ratio'] = killer_stats['kills'] / max(1, killer_stats['deaths'])
        
        # Update victim stats
        if victim_id not in self.player_stats:
            self.player_stats[victim_id] = {
                'name': victim_name,
                'kills': 0,
                'deaths': 0,
                'kd_ratio': 0.0,
                'total_loot': 0,
                'average_loot': 0,
                'kill_streak': 0,
                'best_kill_streak': 0
            }
        
        victim_stats = self.player_stats[victim_id]
        victim_stats['deaths'] += 1
        victim_stats['kill_streak'] = 0
        victim_stats['kd_ratio'] = victim_stats['kills'] / max(1, victim_stats['deaths'])
    
    def get_player_stats(self, player_id: str) -> Optional[Dict]:
        """Get PvP statistics for a player"""
        return self.player_stats.get(player_id)
    
    def get_leaderboard(self, limit: int = 10, sort_by: str = 'kills') -> List[Dict]:
        """
        Get PvP leaderboard
        
        Args:
            limit: Number of top players
            sort_by: 'kills', 'kd_ratio', 'total_loot'
        
        Returns:
            List of top players
        """
        sorted_players = sorted(
            self.player_stats.values(),
            key=lambda x: x.get(sort_by, 0),
            reverse=True
        )
        return sorted_players[:limit]
    
    def get_recent_kills(self, limit: int = 10, player_id: Optional[str] = None) -> List[Dict]:
        """Get recent kills"""
        kills = self.kills
        
        if player_id:
            kills = [k for k in kills if k['killer_id'] == player_id]
        
        return sorted(kills, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_statistics(self) -> Dict:
        """Get overall PvP statistics"""
        total_kills = sum(p['kills'] for p in self.player_stats.values())
        total_deaths = sum(p['deaths'] for p in self.player_stats.values())
        total_loot = sum(p['total_loot'] for p in self.player_stats.values())
        
        return {
            'total_players': len(self.player_stats),
            'total_kills': total_kills,
            'total_deaths': total_deaths,
            'total_loot_value': total_loot,
            'average_kill_value': total_loot / max(1, total_kills),
            'top_killers': self.get_leaderboard(5, 'kills'),
            'top_loot_earners': self.get_leaderboard(5, 'total_loot')
        }
    
    def get_kill_hotspots(self, limit: int = 5) -> List[Dict]:
        """Get most dangerous locations"""
        locations = {}
        
        for kill in self.kills:
            location = kill['location']
            if location not in locations:
                locations[location] = {'kills': 0, 'total_loot': 0}
            
            locations[location]['kills'] += 1
            locations[location]['total_loot'] += kill['loot_value']
        
        sorted_locations = sorted(
            locations.items(),
            key=lambda x: x[1]['kills'],
            reverse=True
        )
        
        return [{'location': loc, **stats} for loc, stats in sorted_locations[:limit]]
