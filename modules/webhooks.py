"""
CloutScape AIO - Webhook Integration
Handles Discord webhook notifications for events, gambling, PvP, and rewards
"""

import aiohttp
import logging
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)

class WebhookType(Enum):
    """Webhook types"""
    GAMBLING = "gambling"
    PVP = "pvp"
    EVENT = "event"
    REWARD = "reward"
    SYSTEM = "system"

class WebhookManager:
    """Manages Discord webhook notifications"""
    
    def __init__(self):
        self.webhooks: Dict[str, str] = {}
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def initialize(self):
        """Initialize async session"""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close async session"""
        if self.session:
            await self.session.close()
    
    def set_webhook(self, webhook_type: str, url: str) -> bool:
        """Set webhook URL for a specific type"""
        try:
            if not url.startswith('https://discord.com/api/webhooks/'):
                logger.error(f"Invalid webhook URL format")
                return False
            
            self.webhooks[webhook_type] = url
            logger.info(f"Set {webhook_type} webhook")
            return True
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")
            return False
    
    async def send_embed(self, webhook_type: str, embed: Dict) -> bool:
        """Send embed message to webhook"""
        if webhook_type not in self.webhooks:
            logger.warning(f"No webhook configured for {webhook_type}")
            return False
        
        if not self.session:
            await self.initialize()
        
        try:
            async with self.session.post(
                self.webhooks[webhook_type],
                json={'embeds': [embed]}
            ) as response:
                return response.status == 204
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")
            return False
    
    # ========================================================================
    # Gambling Notifications
    # ========================================================================
    
    async def notify_gambling_win(self, player_name: str, game_type: str,
                                  bet: int, winnings: int, profit: int) -> bool:
        """Notify gambling win"""
        embed = {
            'title': f'🎰 {player_name} Won!',
            'description': f'**Game:** {game_type.title()}\n**Bet:** {bet:,} GP\n**Winnings:** {winnings:,} GP',
            'color': 0x10b981,
            'fields': [
                {
                    'name': 'Profit',
                    'value': f'+{profit:,} GP',
                    'inline': True
                },
                {
                    'name': 'Timestamp',
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.GAMBLING.value, embed)
    
    async def notify_gambling_loss(self, player_name: str, game_type: str,
                                   bet: int, loss: int) -> bool:
        """Notify gambling loss"""
        embed = {
            'title': f'💔 {player_name} Lost',
            'description': f'**Game:** {game_type.title()}\n**Bet:** {bet:,} GP',
            'color': 0xef4444,
            'fields': [
                {
                    'name': 'Loss',
                    'value': f'-{loss:,} GP',
                    'inline': True
                },
                {
                    'name': 'Timestamp',
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.GAMBLING.value, embed)
    
    async def notify_gambling_jackpot(self, player_name: str, game_type: str,
                                      winnings: int) -> bool:
        """Notify jackpot win"""
        embed = {
            'title': f'🎉 JACKPOT! {player_name}',
            'description': f'**Game:** {game_type.title()}\n**Winnings:** {winnings:,} GP',
            'color': 0xfbbf24,
            'fields': [
                {
                    'name': 'Amount',
                    'value': f'+{winnings:,} GP',
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.GAMBLING.value, embed)
    
    # ========================================================================
    # PvP Notifications
    # ========================================================================
    
    async def notify_pvp_kill(self, killer_name: str, victim_name: str,
                             location: str, loot_value: int, weapon: str = "Unknown") -> bool:
        """Notify PvP kill"""
        embed = {
            'title': f'⚔️ {killer_name} defeated {victim_name}',
            'description': f'**Location:** {location}\n**Weapon:** {weapon}',
            'color': 0xf59e0b,
            'fields': [
                {
                    'name': 'Loot Value',
                    'value': f'{loot_value:,} GP',
                    'inline': True
                },
                {
                    'name': 'Timestamp',
                    'value': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.PVP.value, embed)
    
    async def notify_kill_streak(self, player_name: str, streak: int) -> bool:
        """Notify kill streak"""
        embed = {
            'title': f'🔥 Kill Streak!',
            'description': f'{player_name} is on a **{streak} kill streak**!',
            'color': 0xff6b6b
        }
        
        return await self.send_embed(WebhookType.PVP.value, embed)
    
    # ========================================================================
    # Event Notifications
    # ========================================================================
    
    async def notify_event_created(self, event_title: str, creator_name: str,
                                   event_type: str, prize_value: int, duration_hours: int) -> bool:
        """Notify event creation"""
        embed = {
            'title': f'🎯 New {event_type.title()} Event!',
            'description': f'**{event_title}**\n**Created by:** {creator_name}',
            'color': 0x3b82f6,
            'fields': [
                {
                    'name': 'Total Prize Value',
                    'value': f'{prize_value:,} GP',
                    'inline': True
                },
                {
                    'name': 'Duration',
                    'value': f'{duration_hours} hours',
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.EVENT.value, embed)
    
    async def notify_event_winner(self, event_title: str, winner_name: str,
                                  prize: Dict) -> bool:
        """Notify event winner"""
        embed = {
            'title': f'🏆 Event Winner!',
            'description': f'{winner_name} won **{event_title}**!',
            'color': 0x10b981,
            'fields': [
                {
                    'name': 'Prize',
                    'value': f'{prize.get("name", "Unknown")} ({prize.get("value", 0):,} GP)',
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.EVENT.value, embed)
    
    # ========================================================================
    # Reward Notifications
    # ========================================================================
    
    async def notify_reward_received(self, player_name: str, amount: int,
                                     reason: str) -> bool:
        """Notify reward received"""
        embed = {
            'title': f'💰 Reward Received!',
            'description': f'{player_name} received **{amount:,} GP**',
            'color': 0x10b981,
            'fields': [
                {
                    'name': 'Reason',
                    'value': reason,
                    'inline': False
                }
            ]
        }
        
        return await self.send_embed(WebhookType.REWARD.value, embed)
    
    async def notify_item_received(self, player_name: str, item_name: str,
                                   quantity: int, rarity: str = "common") -> bool:
        """Notify item received"""
        rarity_colors = {
            'common': 0x808080,
            'uncommon': 0x10b981,
            'rare': 0x3b82f6,
            'epic': 0xa855f7,
            'legendary': 0xfbbf24
        }
        
        embed = {
            'title': f'📦 Item Received!',
            'description': f'{player_name} received **{quantity}x {item_name}**',
            'color': rarity_colors.get(rarity.lower(), 0x808080),
            'fields': [
                {
                    'name': 'Rarity',
                    'value': rarity.title(),
                    'inline': True
                }
            ]
        }
        
        return await self.send_embed(WebhookType.REWARD.value, embed)
    
    # ========================================================================
    # System Notifications
    # ========================================================================
    
    async def notify_system_message(self, title: str, message: str,
                                    color: int = 0x3b82f6) -> bool:
        """Send system notification"""
        embed = {
            'title': title,
            'description': message,
            'color': color,
            'timestamp': datetime.now().isoformat()
        }
        
        return await self.send_embed(WebhookType.SYSTEM.value, embed)
    
    async def notify_error(self, error_title: str, error_message: str) -> bool:
        """Notify system error"""
        embed = {
            'title': f'⚠️ {error_title}',
            'description': error_message,
            'color': 0xef4444
        }
        
        return await self.send_embed(WebhookType.SYSTEM.value, embed)
    
    # ========================================================================
    # Batch Notifications
    # ========================================================================
    
    async def send_leaderboard(self, webhook_type: str, title: str,
                               leaderboard: List[Dict]) -> bool:
        """Send leaderboard as embed"""
        fields = []
        for i, entry in enumerate(leaderboard[:10], 1):
            fields.append({
                'name': f'#{i} {entry.get("name", "Unknown")}',
                'value': f'{entry.get("value", 0):,}',
                'inline': False
            })
        
        embed = {
            'title': title,
            'color': 0x3b82f6,
            'fields': fields
        }
        
        return await self.send_embed(webhook_type, embed)
