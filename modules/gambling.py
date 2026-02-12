"""
CloutScape AIO - Gambling System Module
Handles dice rolls, flower poker, blackjack, and gambling statistics
"""

import json
import random
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class GambleType(Enum):
    """Gambling game types"""
    DICE = "dice"
    FLOWER_POKER = "poker"
    BLACKJACK = "blackjack"
    SLOTS = "slots"
    ROULETTE = "roulette"

class GamblingSystem:
    """Advanced gambling system with multiple games"""
    
    def __init__(self, config_file: str = 'gambling_config.json'):
        self.config_file = config_file
        self.logs: List[Dict] = []
        self.player_stats: Dict = {}
        self.load_config()
    
    def load_config(self):
        """Load gambling configuration"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.logs = config.get('logs', [])
                self.player_stats = config.get('stats', {})
        except FileNotFoundError:
            self.logs = []
            self.player_stats = {}
            self.save_config()
    
    def save_config(self):
        """Save gambling configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({
                    'logs': self.logs,
                    'stats': self.player_stats
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving gambling config: {e}")
    
    # ========================================================================
    # Dice Games
    # ========================================================================
    
    def roll_dice(self, player_id: str, player_name: str, bet_amount: int, 
                  player_roll: int, opponent_roll: int) -> Dict:
        """
        Process a dice roll game
        
        Args:
            player_id: Discord user ID
            player_name: Discord username
            bet_amount: Amount wagered
            player_roll: Player's dice roll (1-100)
            opponent_roll: Opponent's dice roll (1-100)
        
        Returns:
            Game result dictionary
        """
        player_roll = max(1, min(100, player_roll))
        opponent_roll = max(1, min(100, opponent_roll))
        
        player_wins = player_roll > opponent_roll
        winnings = bet_amount * 2 if player_wins else 0
        
        result = {
            'type': GambleType.DICE.value,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'player_name': player_name,
            'bet': bet_amount,
            'player_roll': player_roll,
            'opponent_roll': opponent_roll,
            'player_wins': player_wins,
            'winnings': winnings,
            'net_profit': winnings - bet_amount
        }
        
        self.logs.append(result)
        self._update_player_stats(player_id, player_name, result)
        self.save_config()
        
        return result
    
    def flower_poker(self, player_id: str, player_name: str, bet_amount: int,
                     player_hand: List[int], opponent_hand: List[int]) -> Dict:
        """
        Process a flower poker game
        
        Args:
            player_id: Discord user ID
            player_name: Discord username
            bet_amount: Amount wagered
            player_hand: Player's hand (5 cards)
            opponent_hand: Opponent's hand (5 cards)
        
        Returns:
            Game result dictionary
        """
        player_rank = self._evaluate_poker_hand(player_hand)
        opponent_rank = self._evaluate_poker_hand(opponent_hand)
        
        player_wins = player_rank > opponent_rank
        winnings = bet_amount * 2 if player_wins else 0
        
        result = {
            'type': GambleType.FLOWER_POKER.value,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'player_name': player_name,
            'bet': bet_amount,
            'player_hand': player_hand,
            'player_rank': player_rank,
            'opponent_hand': opponent_hand,
            'opponent_rank': opponent_rank,
            'player_wins': player_wins,
            'winnings': winnings,
            'net_profit': winnings - bet_amount
        }
        
        self.logs.append(result)
        self._update_player_stats(player_id, player_name, result)
        self.save_config()
        
        return result
    
    def blackjack(self, player_id: str, player_name: str, bet_amount: int,
                  player_hand: List[int], dealer_hand: List[int]) -> Dict:
        """
        Process a blackjack game
        
        Args:
            player_id: Discord user ID
            player_name: Discord username
            bet_amount: Amount wagered
            player_hand: Player's hand (card values)
            dealer_hand: Dealer's hand (card values)
        
        Returns:
            Game result dictionary
        """
        player_score = self._calculate_blackjack_score(player_hand)
        dealer_score = self._calculate_blackjack_score(dealer_hand)
        
        # Determine winner
        if player_score > 21:
            player_wins = False
            reason = "Player bust"
        elif dealer_score > 21:
            player_wins = True
            reason = "Dealer bust"
        elif player_score == 21 and len(player_hand) == 2:
            player_wins = True
            reason = "Blackjack!"
        elif player_score > dealer_score:
            player_wins = True
            reason = "Higher score"
        elif player_score < dealer_score:
            player_wins = False
            reason = "Dealer wins"
        else:
            player_wins = False
            reason = "Push"
        
        multiplier = 2.5 if reason == "Blackjack!" else 2
        winnings = int(bet_amount * multiplier) if player_wins else 0
        
        result = {
            'type': GambleType.BLACKJACK.value,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'player_name': player_name,
            'bet': bet_amount,
            'player_hand': player_hand,
            'player_score': player_score,
            'dealer_hand': dealer_hand,
            'dealer_score': dealer_score,
            'player_wins': player_wins,
            'reason': reason,
            'winnings': winnings,
            'net_profit': winnings - bet_amount
        }
        
        self.logs.append(result)
        self._update_player_stats(player_id, player_name, result)
        self.save_config()
        
        return result
    
    def slots(self, player_id: str, player_name: str, bet_amount: int) -> Dict:
        """
        Process a slot machine game
        
        Args:
            player_id: Discord user ID
            player_name: Discord username
            bet_amount: Amount wagered
        
        Returns:
            Game result dictionary
        """
        symbols = ['🍎', '🍊', '🍋', '🍌', '🍉', '🎰']
        reels = [random.choice(symbols) for _ in range(3)]
        
        # Determine payout
        if all(r == reels[0] for r in reels):
            multiplier = 10  # Jackpot
        elif reels[0] == reels[1] or reels[1] == reels[2]:
            multiplier = 3  # Two matching
        else:
            multiplier = 0  # No match
        
        winnings = bet_amount * multiplier
        
        result = {
            'type': GambleType.SLOTS.value,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'player_name': player_name,
            'bet': bet_amount,
            'reels': reels,
            'multiplier': multiplier,
            'player_wins': multiplier > 0,
            'winnings': winnings,
            'net_profit': winnings - bet_amount
        }
        
        self.logs.append(result)
        self._update_player_stats(player_id, player_name, result)
        self.save_config()
        
        return result
    
    def roulette(self, player_id: str, player_name: str, bet_amount: int,
                 bet_type: str, bet_value: int) -> Dict:
        """
        Process a roulette game
        
        Args:
            player_id: Discord user ID
            player_name: Discord username
            bet_amount: Amount wagered
            bet_type: 'number', 'color', 'odd/even'
            bet_value: The bet (number 0-36, 'red'/'black', 'odd'/'even')
        
        Returns:
            Game result dictionary
        """
        spin = random.randint(0, 36)
        
        # Determine if bet wins
        player_wins = False
        multiplier = 0
        
        if bet_type == 'number':
            player_wins = spin == bet_value
            multiplier = 36 if player_wins else 0
        elif bet_type == 'color':
            red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
            spin_color = 'red' if spin in red_numbers else 'black'
            player_wins = spin_color == bet_value
            multiplier = 2 if player_wins else 0
        elif bet_type == 'odd_even':
            spin_type = 'odd' if spin % 2 == 1 else 'even'
            player_wins = spin_type == bet_value
            multiplier = 2 if player_wins else 0
        
        winnings = bet_amount * multiplier if player_wins else 0
        
        result = {
            'type': GambleType.ROULETTE.value,
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'player_name': player_name,
            'bet': bet_amount,
            'bet_type': bet_type,
            'bet_value': bet_value,
            'spin': spin,
            'player_wins': player_wins,
            'multiplier': multiplier,
            'winnings': winnings,
            'net_profit': winnings - bet_amount
        }
        
        self.logs.append(result)
        self._update_player_stats(player_id, player_name, result)
        self.save_config()
        
        return result
    
    # ========================================================================
    # Statistics and Analytics
    # ========================================================================
    
    def _update_player_stats(self, player_id: str, player_name: str, result: Dict):
        """Update player statistics"""
        if player_id not in self.player_stats:
            self.player_stats[player_id] = {
                'name': player_name,
                'total_bets': 0,
                'total_winnings': 0,
                'total_profit': 0,
                'games_played': 0,
                'games_won': 0,
                'win_rate': 0.0,
                'by_game': {}
            }
        
        stats = self.player_stats[player_id]
        game_type = result['type']
        
        stats['total_bets'] += result['bet']
        stats['total_winnings'] += result['winnings']
        stats['total_profit'] += result['net_profit']
        stats['games_played'] += 1
        
        if result.get('player_wins'):
            stats['games_won'] += 1
        
        stats['win_rate'] = (stats['games_won'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
        
        if game_type not in stats['by_game']:
            stats['by_game'][game_type] = {
                'played': 0,
                'won': 0,
                'total_bet': 0,
                'total_profit': 0
            }
        
        game_stats = stats['by_game'][game_type]
        game_stats['played'] += 1
        game_stats['total_bet'] += result['bet']
        game_stats['total_profit'] += result['net_profit']
        
        if result.get('player_wins'):
            game_stats['won'] += 1
    
    def get_player_stats(self, player_id: str) -> Optional[Dict]:
        """Get statistics for a specific player"""
        return self.player_stats.get(player_id)
    
    def get_leaderboard(self, limit: int = 10, sort_by: str = 'total_profit') -> List[Dict]:
        """
        Get gambling leaderboard
        
        Args:
            limit: Number of top players to return
            sort_by: 'total_profit', 'total_winnings', 'games_won', 'win_rate'
        
        Returns:
            List of top players
        """
        sorted_players = sorted(
            self.player_stats.values(),
            key=lambda x: x.get(sort_by, 0),
            reverse=True
        )
        return sorted_players[:limit]
    
    def get_recent_games(self, limit: int = 10, game_type: Optional[str] = None) -> List[Dict]:
        """Get recent gambling games"""
        games = self.logs
        
        if game_type:
            games = [g for g in games if g['type'] == game_type]
        
        return sorted(games, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_statistics(self) -> Dict:
        """Get overall gambling statistics"""
        total_bets = sum(p['total_bets'] for p in self.player_stats.values())
        total_winnings = sum(p['total_winnings'] for p in self.player_stats.values())
        total_games = len(self.logs)
        
        return {
            'total_players': len(self.player_stats),
            'total_games': total_games,
            'total_bets': total_bets,
            'total_winnings': total_winnings,
            'total_profit': total_winnings - total_bets,
            'average_bet': total_bets / total_games if total_games > 0 else 0,
            'games_by_type': self._count_games_by_type()
        }
    
    def _count_games_by_type(self) -> Dict[str, int]:
        """Count games by type"""
        counts = {}
        for log in self.logs:
            game_type = log['type']
            counts[game_type] = counts.get(game_type, 0) + 1
        return counts
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def _evaluate_poker_hand(self, hand: List[int]) -> int:
        """Evaluate poker hand strength (1-10)"""
        # Simplified poker hand evaluation
        # In a real system, this would be more complex
        hand_sorted = sorted(hand, reverse=True)
        
        # Check for pairs, straights, etc.
        unique = len(set(hand))
        
        if unique == 1:
            return 10  # Five of a kind (impossible in real poker)
        elif unique == 2:
            return 8   # Four of a kind or Full house
        elif unique == 3:
            return 6   # Three of a kind or Two pair
        elif unique == 4:
            return 4   # One pair
        else:
            return 2   # High card
    
    def _calculate_blackjack_score(self, hand: List[int]) -> int:
        """Calculate blackjack hand score"""
        score = sum(hand)
        aces = hand.count(11)
        
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        return score
