#!/usr/bin/env python3
"""
CloutScape Enhanced Discord Bot v2
Sophisticated RSPS-integrated Discord bot with player authentication and management
"""

import os
import sys
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime
import discord
from discord.ext import commands, tasks
from discord.permissions import Permissions
import asyncio

# Import custom modules
from modules.rsps_integration import RSPSIntegration
from modules.gambling import GamblingSystem
from modules.pvp import PvPSystem
from modules.events import EventSystem
from modules.rewards import RewardSystem
from modules.webhooks import WebhookManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

class Config:
    """Bot configuration"""
    
    # Discord Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    GUILD_ID = os.getenv('GUILD_ID')  # Optional: specific guild ID
    
    # RSPS Configuration
    RSPS_HOST = os.getenv('RSPS_HOST', 'localhost')
    RSPS_PORT = int(os.getenv('RSPS_PORT', 43594))
    CLOUDFLARE_DOMAIN = os.getenv('CLOUDFLARE_DOMAIN', 'play.cloutscape.com')
    
    # Bot Configuration
    COMMAND_PREFIX = '!'
    BOT_STATUS = 'CloutScape RSPS | !help'
    
    # Download Links
    CLIENT_DOWNLOAD_URL = os.getenv('CLIENT_DOWNLOAD_URL', 'https://github.com/No6love9/CloutScape/releases/latest/download/client.jar')
    
    # Enhanced Channel Configuration
    CHANNELS = {
        'announcements': {
            'description': '📢 Server announcements and updates',
            'topic': 'Important announcements for CloutScape RSPS',
            'nsfw': False,
            'category': 'Information',
            'emoji': '📢'
        },
        'giveaways': {
            'description': '🎁 Giveaway announcements and entries',
            'topic': 'Participate in exciting giveaways and win prizes!',
            'nsfw': False,
            'category': 'Events',
            'emoji': '🎁'
        },
        'gambling-logs': {
            'description': '🎰 Real-time gambling activity logs',
            'topic': 'Dice, Poker, Blackjack, Slots, and Roulette results',
            'nsfw': False,
            'category': 'Gaming',
            'emoji': '🎰'
        },
        'pvp-kills': {
            'description': '⚔️ PvP kill logs and loot drops',
            'topic': 'Track PvP activity, kills, and epic loot drops',
            'nsfw': False,
            'category': 'Gaming',
            'emoji': '⚔️'
        },
        'leaderboards': {
            'description': '🏆 Community leaderboards and rankings',
            'topic': 'Top players, achievements, and hall of fame',
            'nsfw': False,
            'category': 'Community',
            'emoji': '🏆'
        },
        'events': {
            'description': '🎯 Event announcements and updates',
            'topic': 'Tournaments, raids, and special events',
            'nsfw': False,
            'category': 'Events',
            'emoji': '🎯'
        },
        'general': {
            'description': '💬 General discussion channel',
            'topic': 'General chat and community discussion',
            'nsfw': False,
            'category': 'Community',
            'emoji': '💬'
        },
        'bot-commands': {
            'description': '🤖 Bot commands and interactions',
            'topic': 'Use bot commands here - Type !help for command list',
            'nsfw': False,
            'category': 'Bot',
            'emoji': '🤖'
        },
        'server-status': {
            'description': '📊 Live server statistics',
            'topic': 'Real-time server status and player count',
            'nsfw': False,
            'category': 'Information',
            'emoji': '📊'
        },
        'game-guide': {
            'description': '🎮 How to play and guides',
            'topic': 'Learn how to play, download client, and get started',
            'nsfw': False,
            'category': 'Information',
            'emoji': '🎮'
        },
        'economy': {
            'description': '💰 Market and trading',
            'topic': 'Buy, sell, and trade items with other players',
            'nsfw': False,
            'category': 'Community',
            'emoji': '💰'
        },
        'support': {
            'description': '🔧 Player support tickets',
            'topic': 'Need help? Create a support ticket here',
            'nsfw': False,
            'category': 'Support',
            'emoji': '🔧'
        },
        'logs': {
            'description': '📝 Bot activity logs',
            'topic': 'System logs and administrative records',
            'nsfw': False,
            'category': 'Admin',
            'emoji': '📝'
        },
        'admin': {
            'description': '👑 Admin-only channel',
            'topic': 'Administrative discussions and server management',
            'nsfw': False,
            'category': 'Admin',
            'emoji': '👑'
        }
    }
    
    # Enhanced Role Configuration
    ROLES = {
        'Server Owner': {
            'color': discord.Color.from_rgb(220, 20, 60),  # Crimson
            'hoist': True,
            'mentionable': True,
            'permissions': ['administrator'],
            'emoji': '👑'
        },
        'Admin': {
            'color': discord.Color.from_rgb(255, 140, 0),  # Dark Orange
            'hoist': True,
            'mentionable': True,
            'permissions': ['administrator'],
            'emoji': '⚡'
        },
        'Moderator': {
            'color': discord.Color.from_rgb(255, 215, 0),  # Gold
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'manage_messages',
                'kick_members',
                'ban_members',
                'manage_channels'
            ],
            'emoji': '🛡️'
        },
        'Event Manager': {
            'color': discord.Color.from_rgb(218, 165, 32),  # Goldenrod
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'manage_channels',
                'manage_roles',
                'manage_messages'
            ],
            'emoji': '🎯'
        },
        'VIP': {
            'color': discord.Color.from_rgb(138, 43, 226),  # Blue Violet
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'send_messages',
                'embed_links',
                'attach_files',
                'use_external_emojis'
            ],
            'emoji': '💎'
        },
        'Veteran': {
            'color': discord.Color.from_rgb(30, 144, 255),  # Dodger Blue
            'hoist': True,
            'mentionable': False,
            'permissions': [
                'send_messages',
                'embed_links',
                'attach_files'
            ],
            'emoji': '🌟'
        },
        'PvP Legend': {
            'color': discord.Color.from_rgb(139, 0, 0),  # Dark Red
            'hoist': True,
            'mentionable': False,
            'permissions': ['send_messages'],
            'emoji': '⚔️'
        },
        'High Roller': {
            'color': discord.Color.from_rgb(0, 128, 0),  # Green
            'hoist': True,
            'mentionable': False,
            'permissions': ['send_messages'],
            'emoji': '🎰'
        },
        'Member': {
            'color': discord.Color.from_rgb(135, 206, 250),  # Light Sky Blue
            'hoist': False,
            'mentionable': False,
            'permissions': ['send_messages', 'read_message_history'],
            'emoji': '👤'
        },
        'Muted': {
            'color': discord.Color.greyple(),
            'hoist': False,
            'mentionable': False,
            'permissions': ['read_messages'],
            'emoji': '🔇'
        }
    }

# ============================================================================
# Discord Bot
# ============================================================================

class CloutScapeBot(commands.Cog):
    """Enhanced CloutScape bot with RSPS integration"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_file = 'server_config.json'
        self.setup_status = {}
        
        # Initialize systems
        self.rsps = RSPSIntegration(Config.RSPS_HOST, Config.RSPS_PORT)
        self.gambling = GamblingSystem()
        self.pvp = PvPSystem()
        self.events = EventSystem()
        self.rewards = RewardSystem()
        self.webhooks = WebhookManager()
        
        self.load_configs()
        
        # Start background tasks
        self.update_server_status.start()
        self.update_leaderboards.start()
    
    def load_configs(self):
        """Load saved server configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.setup_status = json.load(f)
                logger.info(f"Loaded configurations for {len(self.setup_status)} servers")
            except Exception as e:
                logger.error(f"Error loading configs: {e}")
    
    def save_configs(self):
        """Save server configurations"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.setup_status, f, indent=2)
            logger.info("Configurations saved")
        except Exception as e:
            logger.error(f"Error saving configs: {e}")
    
    @tasks.loop(minutes=5)
    async def update_server_status(self):
        """Update server status channel"""
        try:
            for guild in self.bot.guilds:
                status_channel = discord.utils.get(guild.text_channels, name='server-status')
                if status_channel:
                    status = self.rsps.get_server_status()
                    players = self.rsps.get_all_players()
                    
                    embed = discord.Embed(
                        title="📊 CloutScape Server Status",
                        description="Real-time server statistics",
                        color=discord.Color.green() if status['online'] else discord.Color.red(),
                        timestamp=datetime.now()
                    )
                    
                    embed.add_field(
                        name="🟢 Server Status",
                        value="Online" if status['online'] else "Offline",
                        inline=True
                    )
                    
                    embed.add_field(
                        name="👥 Players Online",
                        value=f"{status['players_online']}/{status['max_players']}",
                        inline=True
                    )
                    
                    embed.add_field(
                        name="⏱️ Uptime",
                        value=status['uptime'],
                        inline=True
                    )
                    
                    embed.add_field(
                        name="📝 Total Registered",
                        value=str(len(players)),
                        inline=True
                    )
                    
                    embed.add_field(
                        name="🎮 Version",
                        value=status['version'],
                        inline=True
                    )
                    
                    embed.add_field(
                        name="🌐 Connect",
                        value=Config.CLOUDFLARE_DOMAIN,
                        inline=True
                    )
                    
                    embed.set_footer(text="Updates every 5 minutes")
                    
                    # Delete old messages and send new one
                    async for message in status_channel.history(limit=10):
                        if message.author == self.bot.user:
                            await message.delete()
                    
                    await status_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error updating server status: {e}")
    
    @tasks.loop(minutes=10)
    async def update_leaderboards(self):
        """Update leaderboards channel"""
        try:
            for guild in self.bot.guilds:
                lb_channel = discord.utils.get(guild.text_channels, name='leaderboards')
                if lb_channel:
                    # GP Leaderboard
                    gp_leaders = self.rsps.get_leaderboard('gp_balance', 10)
                    
                    embed = discord.Embed(
                        title="🏆 CloutScape Leaderboards",
                        description="Top players in CloutScape",
                        color=discord.Color.gold(),
                        timestamp=datetime.now()
                    )
                    
                    if gp_leaders:
                        gp_text = ""
                        medals = ["🥇", "🥈", "🥉"]
                        for i, player in enumerate(gp_leaders):
                            medal = medals[i] if i < 3 else f"{i+1}."
                            gp_text += f"{medal} **{player['username']}** - {player['gp_balance']:,} GP\n"
                        
                        embed.add_field(
                            name="💰 Richest Players",
                            value=gp_text,
                            inline=False
                        )
                    
                    # Login Leaderboard
                    login_leaders = self.rsps.get_leaderboard('total_logins', 5)
                    if login_leaders:
                        login_text = ""
                        for i, player in enumerate(login_leaders):
                            login_text += f"{i+1}. **{player['username']}** - {player['total_logins']} logins\n"
                        
                        embed.add_field(
                            name="🎮 Most Active Players",
                            value=login_text,
                            inline=False
                        )
                    
                    embed.set_footer(text="Updates every 10 minutes")
                    
                    # Delete old messages and send new one
                    async for message in lb_channel.history(limit=10):
                        if message.author == self.bot.user:
                            await message.delete()
                    
                    await lb_channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error updating leaderboards: {e}")
    
    @commands.command(name='register')
    async def register(self, ctx, username: str = None):
        """Register a new RSPS account"""
        if not username:
            await ctx.send("❌ Please provide a username! Example: `!register YourName`")
            return
        
        result = self.rsps.register_player(
            str(ctx.author.id),
            str(ctx.author),
            username
        )
        
        if result['success']:
            # Send DM with credentials
            try:
                embed = discord.Embed(
                    title="✅ Account Created Successfully!",
                    description=f"Welcome to CloutScape, **{username}**!",
                    color=discord.Color.green()
                )
                
                embed.add_field(
                    name="📝 Username",
                    value=f"`{result['username']}`",
                    inline=False
                )
                
                embed.add_field(
                    name="🔑 Password",
                    value=f"||`{result['password']}`||",
                    inline=False
                )
                
                embed.add_field(
                    name="⚠️ Important",
                    value="Save these credentials! You'll need them to log in.",
                    inline=False
                )
                
                embed.add_field(
                    name="📥 Download Client",
                    value=f"[Click here to download]({Config.CLIENT_DOWNLOAD_URL})",
                    inline=False
                )
                
                embed.add_field(
                    name="🌐 Server Address",
                    value=f"`{Config.CLOUDFLARE_DOMAIN}`",
                    inline=False
                )
                
                embed.add_field(
                    name="🎮 How to Play",
                    value="1. Download the client\n2. Run client.jar\n3. Login with your credentials\n4. Enjoy!",
                    inline=False
                )
                
                embed.set_footer(text="CloutScape RSPS | Have fun!")
                
                await ctx.author.send(embed=embed)
                await ctx.send(f"✅ Account created! Check your DMs for login details, **{ctx.author.mention}**!")
                
                # Assign Member role
                member_role = discord.utils.get(ctx.guild.roles, name='Member')
                if member_role:
                    await ctx.author.add_roles(member_role)
                
                logger.info(f"Registered new player: {username} (Discord: {ctx.author})")
                
            except discord.Forbidden:
                await ctx.send(f"❌ Couldn't send you a DM! Please enable DMs from server members and try again.")
        else:
            await ctx.send(f"❌ {result['error']}")
    
    @commands.command(name='download')
    async def download(self, ctx):
        """Get client download link"""
        embed = discord.Embed(
            title="📥 Download CloutScape Client",
            description="Get the game client to start playing!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🔗 Download Link",
            value=f"[Click here to download client.jar]({Config.CLIENT_DOWNLOAD_URL})",
            inline=False
        )
        
        embed.add_field(
            name="📋 Requirements",
            value="• Java 11 or higher\n• Windows, Mac, or Linux\n• Active CloutScape account",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Quick Start",
            value="1. Download client.jar\n2. Double-click to run\n3. Login with your credentials\n4. Start playing!",
            inline=False
        )
        
        embed.add_field(
            name="❓ Need an account?",
            value="Use `!register YourUsername` to create one!",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='stats')
    async def stats(self, ctx, member: discord.Member = None):
        """View player statistics"""
        target = member or ctx.author
        stats = self.rsps.get_player_stats(str(target.id))
        
        if not stats:
            await ctx.send(f"❌ {target.mention} doesn't have an account! Use `!register` to create one.")
            return
        
        embed = discord.Embed(
            title=f"📊 Player Statistics - {stats['username']}",
            color=discord.Color.blue()
        )
        
        embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
        
        embed.add_field(
            name="💰 GP Balance",
            value=f"{stats['gp_balance']:,} GP",
            inline=True
        )
        
        embed.add_field(
            name="🎖️ Rank",
            value=stats['rank'],
            inline=True
        )
        
        embed.add_field(
            name="🎮 Total Logins",
            value=str(stats['total_logins']),
            inline=True
        )
        
        embed.add_field(
            name="📅 Account Created",
            value=stats['created_at'][:10] if stats['created_at'] != 'Unknown' else 'Unknown',
            inline=True
        )
        
        embed.add_field(
            name="🕐 Last Login",
            value=stats['last_login'][:10] if stats['last_login'] and stats['last_login'] != 'Never' else 'Never',
            inline=True
        )
        
        embed.add_field(
            name="🚫 Status",
            value="Banned" if stats['is_banned'] else "Active",
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        """View top players"""
        gp_leaders = self.rsps.get_leaderboard('gp_balance', 10)
        
        embed = discord.Embed(
            title="🏆 CloutScape Leaderboards",
            description="Top players by GP balance",
            color=discord.Color.gold()
        )
        
        if gp_leaders:
            medals = ["🥇", "🥈", "🥉"]
            text = ""
            for i, player in enumerate(gp_leaders):
                medal = medals[i] if i < 3 else f"{i+1}."
                text += f"{medal} **{player['username']}** - {player['gp_balance']:,} GP\n"
            
            embed.add_field(
                name="💰 Richest Players",
                value=text,
                inline=False
            )
        else:
            embed.add_field(
                name="💰 Richest Players",
                value="No players yet!",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show help message"""
        embed = discord.Embed(
            title="🤖 CloutScape Bot Commands",
            description="All available commands",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="👤 Player Commands",
            value=(
                "`!register <username>` - Create RSPS account\n"
                "`!download` - Get client download link\n"
                "`!stats [@user]` - View player statistics\n"
                "`!leaderboard` - View top players\n"
                "`!help` - Show this message"
            ),
            inline=False
        )
        
        if ctx.author.guild_permissions.administrator:
            embed.add_field(
                name="👑 Admin Commands",
                value=(
                    "`!setup` - Setup Discord server\n"
                    "`!addgp <@user> <amount>` - Add GP to player\n"
                    "`!removegp <@user> <amount>` - Remove GP from player\n"
                    "`!ban <@user>` - Ban player\n"
                    "`!unban <@user>` - Unban player\n"
                    "`!resetpass <@user>` - Reset player password\n"
                    "`!broadcast <message>` - Server announcement"
                ),
                inline=False
            )
        
        embed.set_footer(text="CloutScape RSPS | Type !help for commands")
        
        await ctx.send(embed=embed)
    
    # Admin commands continue in next part...
    
    @commands.command(name='addgp')
    @commands.has_permissions(administrator=True)
    async def add_gp(self, ctx, member: discord.Member, amount: int):
        """Add GP to a player (Admin only)"""
        if self.rsps.add_gp(str(member.id), amount):
            await ctx.send(f"✅ Added {amount:,} GP to **{member.display_name}**!")
            logger.info(f"Admin {ctx.author} added {amount} GP to {member}")
        else:
            await ctx.send(f"❌ {member.mention} doesn't have an account!")
    
    @commands.command(name='removegp')
    @commands.has_permissions(administrator=True)
    async def remove_gp(self, ctx, member: discord.Member, amount: int):
        """Remove GP from a player (Admin only)"""
        if self.rsps.remove_gp(str(member.id), amount):
            await ctx.send(f"✅ Removed {amount:,} GP from **{member.display_name}**!")
            logger.info(f"Admin {ctx.author} removed {amount} GP from {member}")
        else:
            await ctx.send(f"❌ Failed to remove GP! Check if player has enough GP.")
    
    @commands.command(name='ban')
    @commands.has_permissions(administrator=True)
    async def ban_player(self, ctx, member: discord.Member, *, reason: str = "Violation of rules"):
        """Ban a player (Admin only)"""
        if self.rsps.ban_player(str(member.id), reason):
            await ctx.send(f"✅ Banned **{member.display_name}**! Reason: {reason}")
            logger.info(f"Admin {ctx.author} banned {member}: {reason}")
        else:
            await ctx.send(f"❌ {member.mention} doesn't have an account!")
    
    @commands.command(name='unban')
    @commands.has_permissions(administrator=True)
    async def unban_player(self, ctx, member: discord.Member):
        """Unban a player (Admin only)"""
        if self.rsps.unban_player(str(member.id)):
            await ctx.send(f"✅ Unbanned **{member.display_name}**!")
            logger.info(f"Admin {ctx.author} unbanned {member}")
        else:
            await ctx.send(f"❌ {member.mention} doesn't have an account!")
    
    @commands.command(name='resetpass')
    @commands.has_permissions(administrator=True)
    async def reset_password(self, ctx, member: discord.Member):
        """Reset player password (Admin only)"""
        new_password = self.rsps.reset_password(str(member.id))
        if new_password:
            try:
                await member.send(f"🔑 Your password has been reset!\n\nNew password: ||`{new_password}`||\n\nKeep it safe!")
                await ctx.send(f"✅ Password reset for **{member.display_name}**! They've been sent a DM.")
                logger.info(f"Admin {ctx.author} reset password for {member}")
            except discord.Forbidden:
                await ctx.send(f"✅ Password reset, but couldn't DM them. New password: ||`{new_password}`||")
        else:
            await ctx.send(f"❌ {member.mention} doesn't have an account!")
    
    @commands.command(name='broadcast')
    @commands.has_permissions(administrator=True)
    async def broadcast(self, ctx, *, message: str):
        """Send announcement to announcements channel (Admin only)"""
        announcements = discord.utils.get(ctx.guild.text_channels, name='announcements')
        if announcements:
            embed = discord.Embed(
                title="📢 Server Announcement",
                description=message,
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(text=f"Announced by {ctx.author.display_name}")
            await announcements.send(embed=embed)
            await ctx.send("✅ Announcement sent!")
            logger.info(f"Admin {ctx.author} sent broadcast: {message}")
        else:
            await ctx.send("❌ Announcements channel not found!")
    
    @commands.command(name='setup')
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Setup Discord server with all channels and roles"""
        # Implementation from original bot.py
        await ctx.send("🚀 Starting server setup... This may take a minute!")
        
        try:
            # Create categories
            categories = {}
            category_names = set(ch['category'] for ch in Config.CHANNELS.values())
            
            for cat_name in category_names:
                category = discord.utils.get(ctx.guild.categories, name=cat_name)
                if not category:
                    category = await ctx.guild.create_category(cat_name)
                categories[cat_name] = category
            
            # Create roles
            for role_name, role_config in Config.ROLES.items():
                existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
                if not existing_role:
                    perms_dict = {}
                    for perm in role_config['permissions']:
                        perms_dict[perm] = True
                    permissions = Permissions(**perms_dict)
                    
                    await ctx.guild.create_role(
                        name=role_name,
                        color=role_config['color'],
                        hoist=role_config['hoist'],
                        mentionable=role_config['mentionable'],
                        permissions=permissions
                    )
            
            # Create channels
            for channel_name, channel_config in Config.CHANNELS.items():
                existing_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                if not existing_channel:
                    category = categories.get(channel_config['category'])
                    await ctx.guild.create_text_channel(
                        name=channel_name,
                        category=category,
                        topic=channel_config['topic']
                    )
            
            # Save configuration
            self.setup_status[str(ctx.guild.id)] = {
                'guild_name': ctx.guild.name,
                'setup_date': datetime.now().isoformat(),
                'status': 'completed'
            }
            self.save_configs()
            
            await ctx.send("✅ Server setup complete! All channels and roles have been created.")
            logger.info(f"Setup completed for guild: {ctx.guild.name}")
            
        except Exception as e:
            await ctx.send(f"❌ Error during setup: {str(e)}")
            logger.error(f"Setup error: {e}")

# ============================================================================
# Bot Initialization
# ============================================================================

def main():
    """Initialize and run the bot"""
    
    # Check for required environment variables
    if not Config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        sys.exit(1)
    
    if not Config.ADMIN_ID:
        logger.error("ADMIN_ID not found in environment variables!")
        sys.exit(1)
    
    # Create bot instance
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    bot = commands.Bot(
        command_prefix=Config.COMMAND_PREFIX,
        intents=intents,
        help_command=None  # We'll use custom help
    )
    
    @bot.event
    async def on_ready():
        """Bot ready event"""
        logger.info(f"Bot logged in as {bot.user}")
        logger.info(f"Bot is in {len(bot.guilds)} guilds")
        
        # Set bot status
        await bot.change_presence(
            activity=discord.Game(name=Config.BOT_STATUS)
        )
        
        logger.info("CloutScape bot is ready!")
    
    @bot.event
    async def on_member_join(member):
        """Welcome new members"""
        general = discord.utils.get(member.guild.text_channels, name='general')
        if general:
            embed = discord.Embed(
                title=f"Welcome to CloutScape, {member.display_name}! 🎉",
                description=(
                    f"Welcome {member.mention}!\n\n"
                    "**Get Started:**\n"
                    "1. Use `!register YourUsername` to create an account\n"
                    "2. Use `!download` to get the game client\n"
                    "3. Use `!help` to see all commands\n\n"
                    "Enjoy your stay!"
                ),
                color=discord.Color.green()
            )
            await general.send(embed=embed)
    
    # Add cog
    asyncio.run(bot.add_cog(CloutScapeBot(bot)))
    
    # Run bot
    try:
        bot.run(Config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to run bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
