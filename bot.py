#!/usr/bin/env python3
import os
os.environ["DISCORD_NO_AUDIO"] = "1"
"""
CloutScape Enhanced Discord Bot v2
Sophisticated RSPS-integrated Discord bot with player authentication and management
"""
import sys
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime
import discord
from discord.ext import commands, tasks
from discord import Permissions
import asyncio
import random
import matplotlib.pyplot as plt
import io

# Import custom modules - assume they exist
try:
    from modules.rsps_integration import RSPSIntegration
    from modules.gambling import GamblingSystem
    from modules.pvp import PvPSystem
    from modules.events import EventSystem
    from modules.rewards import RewardSystem
    from modules.webhooks import WebhookManager
except ImportError as e:
    print(f"Missing module: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    handlers=[
        logging.FileHandler(\'bot.log\'),
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
    DISCORD_TOKEN = os.getenv(\'DISCORD_TOKEN\')
    ADMIN_ID = int(os.getenv(\'ADMIN_ID\', 0))
    GUILD_ID = os.getenv(\'GUILD_ID\')  # Optional: specific guild ID
    # RSPS Configuration
    RSPS_HOST = os.getenv(\'RSPS_HOST\', \'localhost\')
    RSPS_PORT = int(os.getenv(\'RSPS_PORT\', 43594))
    CLOUDFLARE_DOMAIN = os.getenv(\'CLOUDFLARE_DOMAIN\', \'play.cloutscape.com\')
    # Bot Configuration
    COMMAND_PREFIX = \'!\
    BOT_STATUS = \'CloutScape RSPS | !help\'
    # Download Links
    CLIENT_DOWNLOAD_URL = os.getenv(\'CLIENT_DOWNLOAD_URL\', \'https://github.com/No6love9/CloutScape/releases/latest/download/client.jar\')
    # Enhanced Channel Configuration
    CHANNELS = {
        \'announcements\': {
            \'description\': \'📢 Server announcements and updates\',
            \'topic\': \'Important announcements for CloutScape RSPS\',
            \'nsfw\': False,
            \'category\': \'Information\',
            \'emoji\': \'📢\'
        },
        \'giveaways\': {
            \'description\': \'🎁 Giveaway announcements and entries\',
            \'topic\': \'Participate in exciting giveaways and win prizes!\',
            \'nsfw\': False,
            \'category\': \'Events\',
            \'emoji\': \'🎁\'
        },
        \'gambling-logs\': {
            \'description\': \'🎰 Real-time gambling activity logs\',
            \'topic\': \'Dice, Poker, Blackjack, Slots, and Roulette results\',
            \'nsfw\': False,
            \'category\': \'Gaming\',
            \'emoji\': \'🎰\'
        },
        \'pvp-kills\': {
            \'description\': \'⚔️ PvP kill logs and loot drops\',
            \'topic\': \'Track PvP activity, kills, and epic loot drops\',
            \'nsfw\': False,
            \'category\': \'Gaming\',
            \'emoji\': \'⚔️\'
        },
        \'leaderboards\': {
            \'description\': \'🏆 Community leaderboards and rankings\',
            \'topic\': \'Top players, achievements, and hall of fame\',
            \'nsfw\': False,
            \'category\': \'Community\',
            \'emoji\': \'🏆\'
        },
        \'events\': {
            \'description\': \'🎯 Event announcements and updates\',
            \'topic\': \'Tournaments, raids, and special events\',
            \'nsfw\': False,
            \'category\': \'Events\',
            \'emoji\': \'🎯\'
        },
        \'general\': {
            \'description\': \'💬 General discussion channel\',
            \'topic\': \'General chat and community discussion\',
            \'nsfw\': False,
            \'category\': \'Community\',
            \'emoji\': \'💬\'
        },
        \'bot-commands\': {
            \'description\': \'🤖 Bot commands and interactions\',
            \'topic\': \'Use bot commands here - Type !help for command list\',
            \'nsfw\': False,
            \'category\': \'Bot\',
            \'emoji\': \'🤖\'
        },
        \'server-status\': {
            \'description\': \'📊 Live server statistics\',
            \'topic\': \'Real-time server status and player count\',
            \'nsfw\': False,
            \'category\': \'Information\',
            \'emoji\': \'📊\'
        },
        \'game-guide\': {
            \'description\': \'🎮 How to play and guides\',
            \'topic\': \'Learn how to play, download client, and get started\',
            \'nsfw\': False,
            \'category\': \'Information\',
            \'emoji\': \'🎮\'
        },
        \'economy\': {
            \'description\': \'💰 Market and trading\',
            \'topic\': \'Buy, sell, and trade items with other players\',
            \'nsfw\': False,
            \'category\': \'Community\',
            \'emoji\': \'💰\'
        },
        \'support\': {
            \'description\': \'🔧 Player support tickets\',
            \'topic\': \'Need help? Create a support ticket here\',
            \'nsfw\': False,
            \'category\': \'Support\',
            \'emoji\': \'🔧\'
        },
        \'logs\': {
            \'description\': \'📝 Bot activity logs\',
            \'topic\': \'System logs and administrative records\',
            \'nsfw\': False,
            \'category\': \'Admin\',
            \'emoji\': \'📝\'
        },
        \'admin\': {
            \'description\': \'👑 Admin-only channel\',
            \'topic\': \'Administrative discussions and server management\',
            \'nsfw\': False,
            \'category\': \'Admin\',
            \'emoji\': \'👑\'
        },
        # New channels from SYSTEM_PROMPT.md
        \'casino\': {
            \'description\': \'🎲 All casino games and gambling activities\',
            \'topic\': \'Roll the dice, play poker, and win big!\',
            \'nsfw\': True,
            \'category\': \'Gaming\',
            \'emoji\': \'🎲\'
        },
        \'pos-shop\': {
            \'description\': \'🛍️ Player-owned shops and item trading\',
            \'topic\': \'Buy and sell items with other players\',
            \'nsfw\': False,
            \'category\': \'Economy\',
            \'emoji\': \'🛍️\'
        },
        \'games\': {
            \'description\': \'🎮 General games and events channel\',
            \'topic\': \'Participate in various games and events\',
            \'nsfw\': False,
            \'category\': \'Gaming\',
            \'emoji\': \'🎮\'
        },
        \'private-vaults\': {
            \'description\': \'🔒 Private player vaults and storage\',
            \'topic\': \'Securely store your valuable items\',
            \'nsfw\': False,
            \'category\': \'Economy\',
            \'emoji\': \'🔒\'
        }
    }
    # Enhanced Role Configuration
    ROLES = {
        \'Server Owner\': {
            \'color\': discord.Color.from_rgb(220, 20, 60),  # Crimson
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [\'administrator\'],
            \'emoji\': \'👑\'
        },
        \'Admin\': {
            \'color\': discord.Color.from_rgb(255, 140, 0),  # Dark Orange
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [\'administrator\'],
            \'emoji\': \'⚡\'
        },
        \'Moderator\': {
            \'color\': discord.Color.from_rgb(255, 215, 0),  # Gold
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [
                \'manage_messages\',
                \'kick_members\',
                \'ban_members\',
                \'manage_channels\'
            ],
            \'emoji\': \'🛡️\'
        },
        \'Event Manager\': {
            \'color\': discord.Color.from_rgb(218, 165, 32),  # Goldenrod
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [
                \'manage_channels\',
                \'manage_roles\',
                \'manage_messages\'
            ],
            \'emoji\': \'🎯\'
        },
        \'VIP\': {
            \'color\': discord.Color.from_rgb(138, 43, 226),  # Blue Violet
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [
                \'send_messages\',
                \'embed_links\',
                \'attach_files\',
                \'use_external_emojis\'
            ],
            \'emoji\': \'💎\'
        },
        \'Veteran\': {
            \'color\': discord.Color.from_rgb(30, 144, 255),  # Dodger Blue
            \'hoist\': True,
            \'mentionable\': False,
            \'permissions\': [
                \'send_messages\',
                \'embed_links\',
                \'attach_files\'
            ],
            \'emoji\': \'🌟\'
        },
        \'PvP Legend\': {
            \'color\': discord.Color.from_rgb(139, 0, 0),  # Dark Red
            \'hoist\': True,
            \'mentionable\': False,
            \'permissions\': [\'send_messages\'],
            \'emoji\': \'⚔️\'
        },
        \'High Roller\': {
            \'color\': discord.Color.from_rgb(0, 128, 0),  # Green
            \'hoist\': True,
            \'mentionable\': False,
            \'permissions\': [\'send_messages\'],
            \'emoji\': \'🎰\'
        },
        \'Member\': {
            \'color\': discord.Color.from_rgb(135, 206, 250),  # Light Sky Blue
            \'hoist\': False,
            \'mentionable\': False,
            \'permissions\': [\'send_messages\', \'read_message_history\'],
            \'emoji\': \'👤\'
        },
        \'Muted\': {
            \'color\': discord.Color.greyple(),
            \'hoist\': False,
            \'mentionable\': False,
            \'permissions\': [\'read_messages\'],
            \'emoji\': \'🔇\'
        },
        # New roles from SYSTEM_PROMPT.md
        \'Adventurer\': {
            \'color\': discord.Color.from_rgb(100, 149, 237), # Cornflower Blue
            \'hoist\': True,
            \'mentionable\': False,
            \'permissions\': [\'send_messages\', \'read_message_history\'],
            \'emoji\': \'🚶\'
        },
        \'Legend\': {
            \'color\': discord.Color.from_rgb(255, 215, 0), # Gold
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [\'send_messages\', \'read_message_history\', \'embed_links\'],
            \'emoji\': \'🌟\'
        },
        \'Degen\': {
            \'color\': discord.Color.from_rgb(178, 34, 34), # Firebrick
            \'hoist\': True,
            \'mentionable\': True,
            \'permissions\': [\'send_messages\', \'read_message_history\', \'embed_links\', \'attach_files\'],
            \'emoji\': \'😈\'
        }
    }

# ============================================================================
# Modular RSPS Manager (for wipe, etc.)
# ============================================================================
class RSPSManager:
    def __init__(self):
        self.rsps = RSPSIntegration(Config.RSPS_HOST, Config.RSPS_PORT)
    
    def wipe_players(self):
        self.rsps.wipe_all_players()

# ============================================================================
# Discord Bot Cog
# ============================================================================
class CloutScapeBot(commands.Cog):
    """Enhanced CloutScape bot with RSPS integration"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_file = \'server_config.json\'
        self.setup_status = {}
        # Initialize systems
        try:
            self.gambling = GamblingSystem()
            self.pvp = PvPSystem()
            self.events = EventSystem()
            self.rewards = RewardSystem()
            self.webhooks = WebhookManager()
            self.rsps_manager = RSPSManager()
        except Exception as e:
            logger.error(f"Error initializing systems: {e}")
            raise
        self.load_configs()

    def cog_load(self):
        self.update_server_status.start()
        self.update_leaderboards.start()

    def cog_unload(self):
        self.update_server_status.cancel()
        self.update_leaderboards.cancel()

    def load_configs(self):
        """Load saved server configurations"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    self.setup_status = json.load(f)
                logger.info(f"Loaded configurations for {len(self.setup_status)} servers")
            else:
                logger.info("No existing server configurations found.")
        except Exception as e:
            logger.error(f"Error loading configs: {e}")

    def save_configs(self):
        """Save server configurations"""
        try:
            with open(self.config_file, \'w\') as f:
                json.dump(self.setup_status, f, indent=2)
            logger.info("Configurations saved")
        except Exception as e:
            logger.error(f"Error saving configs: {e}")

    @tasks.loop(minutes=5)
    async def update_server_status(self):
        """Periodically update server status in a dedicated channel"""
        status = self.rsps_manager.rsps.get_server_status()
        embed = discord.Embed(title="Server Status", color=discord.Color.blue())
        embed.add_field(name="Online", value="✅ Yes" if status["online"] else "❌ No", inline=True)
        embed.add_field(name="Players Online", value=status["players_online"], inline=True)
        embed.add_field(name="Uptime", value=status["uptime"], inline=True)
        embed.add_field(name="Version", value=status["version"], inline=True)
        embed.add_field(name="Max Players", value=status["max_players"], inline=True)

        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name=\'server-status\')
            if channel:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    logger.error(f"Error sending server status to {guild.name}: {e}")

    @tasks.loop(hours=1)
    async def update_leaderboards(self):
        """Periodically update leaderboards in a dedicated channel"""
        gp_leaders = self.rsps_manager.rsps.get_leaderboard(\'gp_balance\', 10)
        if not gp_leaders:
            return

        embed = discord.Embed(title="🏆 Top 10 GP Leaders", color=discord.Color.gold())
        description = ""
        for i, player in enumerate(gp_leaders):
            description += f"{i+1}. {player[\'username\']} - {player[\'gp_balance\']:,} GP\n"
        embed.description = description

        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name=\'leaderboards\')
            if channel:
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    logger.error(f"Error sending leaderboard to {guild.name}: {e}")

    @commands.command(name=\'register\')
    async def register(self, ctx, username: str):
        """Register your in-game account with Discord"""
        player_id = str(ctx.author.id)
        player_name = ctx.author.name

        result = self.rsps_manager.rsps.register_player(player_id, player_name, username)

        if result[\'success\']:
            embed = discord.Embed(
                title="✅ Account Registered!",
                description=f"Welcome, {username}! Your account has been created.",
                color=discord.Color.green()
            )
            embed.add_field(name="Username", value=result[\'username\'], inline=False)
            embed.add_field(name="Password", value=f"||`{result[\'password\']}`||", inline=False)
            embed.set_footer(text="Keep your password safe! You can change it in-game.")
            await ctx.author.send(embed=embed)
            await ctx.send(f"✅ {ctx.author.mention}, your account has been registered. Check your DMs for login details!")
            logger.info(f"Player {player_name} registered with username {username}")
        else:
            await ctx.send(f"❌ Registration failed: {result[\'error\']}")
            logger.warning(f"Player {player_name} failed to register: {result[\'error\']}")

    @commands.command(name=\'profile\')
    async def profile(self, ctx, member: Optional[discord.Member] = None):
        """View your or another player\'s profile"""
        member = member or ctx.author
        player_id = str(member.id)

        account = self.rsps_manager.rsps.get_player_stats(player_id)

        if account:
            embed = discord.Embed(
                title=f"👤 {account[\'username\']}\'s Profile",
                color=discord.Color.blue()
            )
            embed.add_field(name="Rank", value=account[\'rank\'], inline=True)
            embed.add_field(name="GP Balance", value=f"{account[\'gp_balance\']:,}", inline=True)
            embed.add_field(name="Total Logins", value=account[\'total_logins\'], inline=True)
            embed.add_field(name="Last Login", value=account[\'last_login\'], inline=True)
            embed.add_field(name="Created At", value=account[\'created_at\'], inline=True)
            embed.add_field(name="Banned", value="Yes" if account[\'is_banned\'] else "No", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {member.mention} does not have a registered account.")

    @commands.command(name=\'balance\', aliases=[\'bal\', \'gp\'])
    async def balance(self, ctx):
        """Check your current GP balance"""
        player_id = str(ctx.author.id)
        account = self.rsps_manager.rsps.get_player_stats(player_id)

        if account:
            await ctx.send(f"💰 {ctx.author.mention}, your current GP balance is: {account[\'gp_balance\']:,}")
        else:
            await ctx.send(f"❌ {ctx.author.mention}, you don\'t have a registered account. Use `!register <username>` to create one.")

    @commands.command(name=\'dice\')
    async def dice_roll(self, ctx, bet_amount: int, opponent: discord.Member):
        """Roll dice against another player"""
        player_id = str(ctx.author.id)
        opponent_id = str(opponent.id)

        # Basic balance check (will be replaced by proper economy system)
        player_account = self.rsps_manager.rsps.get_account(player_id)
        opponent_account = self.rsps_manager.rsps.get_account(opponent_id)

        if not player_account or not opponent_account:
            await ctx.send("❌ Both players need registered accounts.")
            return
        if player_account[\'gp_balance\'] < bet_amount or opponent_account[\'gp_balance\'] < bet_amount:
            await ctx.send("❌ Both players need enough GP to bet.")
            return

        player_roll = random.randint(1, 100)
        opponent_roll = random.randint(1, 100)

        result = self.gambling.roll_dice(player_id, ctx.author.name, bet_amount, player_roll, opponent_roll)

        if result[\'player_wins\']:
            self.rsps_manager.rsps.remove_gp(player_id, bet_amount)
            self.rsps_manager.rsps.add_gp(player_id, result[\'winnings\'])
            self.rsps_manager.rsps.remove_gp(opponent_id, bet_amount)
            embed = discord.Embed(title="🎲 Dice Roll Winner!", description=f"{ctx.author.mention} wins {result[\'winnings\']:,} GP!", color=discord.Color.green())
        else:
            self.rsps_manager.rsps.remove_gp(player_id, bet_amount)
            self.rsps_manager.rsps.add_gp(opponent_id, bet_amount * 2)
            embed = discord.Embed(title="🎲 Dice Roll Loser!", description=f"{opponent.mention} wins {bet_amount * 2:,} GP!", color=discord.Color.red())

        embed.add_field(name=f"{ctx.author.name}\'s Roll", value=player_roll, inline=True)
        embed.add_field(name=f"{opponent.name}\'s Roll", value=opponent_roll, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name=\'leaderboard\', aliases=[\'lb\'])
    async def leaderboard(self, ctx, sort_by: str = \'gp\'):
        """View the top players by GP or other stats"""
        if sort_by.lower() == \'gp\':
            leaders = self.rsps_manager.rsps.get_leaderboard(\'gp_balance\', 10)
            title = "🏆 Top 10 GP Leaders"
            field_name = "GP Balance"
        elif sort_by.lower() == \'logins\':
            leaders = self.rsps_manager.rsps.get_leaderboard(\'total_logins\', 10)
            title = "📊 Top 10 Login Streaks"
            field_name = "Total Logins"
        else:
            await ctx.send("❌ Invalid sort option. Use `gp` or `logins`.")
            return

        if not leaders:
            await ctx.send("❌ No leaders to display yet.")
            return

        embed = discord.Embed(title=title, color=discord.Color.gold())
        description = ""
        for i, player in enumerate(leaders):
            description += f"{i+1}. {player[\'username\']} - {player[sort_by.lower() if sort_by.lower() == \'gp\' else \'total_logins\']:,}\n"
        embed.description = description
        await ctx.send(embed=embed)

    @commands.command(name=\'addgp\')
    @commands.has_permissions(administrator=True)
    async def add_gp(self, ctx, member: discord.Member, amount: int):
        """Add GP to a player (Admin only)"""
        try:
            if self.rsps_manager.rsps.add_gp(str(member.id), amount):
                await ctx.send(f"✅ Added {amount:,} GP to {member.display_name}!")
                logger.info(f"{ctx.author} added {amount} GP to {member}")
            else:
                await ctx.send(f"❌ {member.mention} no account.")
        except Exception as e:
            logger.error(f"Addgp error: {e}")
            await ctx.send("❌ Addgp failed.")

    @commands.command(name=\'removegp\')
    @commands.has_permissions(administrator=True)
    async def remove_gp(self, ctx, member: discord.Member, amount: int):
        """Remove GP from a player (Admin only)"""
        try:
            if self.rsps_manager.rsps.remove_gp(str(member.id), amount):
                await ctx.send(f"✅ Removed {amount:,} GP from {member.display_name}!")
                logger.info(f"{ctx.author} removed {amount} GP from {member}")
            else:
                await ctx.send("❌ Failed to remove GP.")
        except Exception as e:
            logger.error(f"Removegp error: {e}")
            await ctx.send("❌ Removegp failed.")

    @commands.command(name=\'ban\')
    @commands.has_permissions(administrator=True)
    async def ban_player(self, ctx, member: discord.Member, *, reason: str = "Violation of rules"):
        """Ban a player (Admin only)"""
        try:
            if self.rsps_manager.rsps.ban_player(str(member.id), reason):
                await ctx.send(f"✅ Banned {member.display_name}! Reason: {reason}")
                logger.info(f"{ctx.author} banned {member}: {reason}")
            else:
                await ctx.send(f"❌ {member.mention} no account.")
        except Exception as e:
            logger.error(f"Ban error: {e}")
            await ctx.send("❌ Ban failed.")

    @commands.command(name=\'unban\')
    @commands.has_permissions(administrator=True)
    async def unban_player(self, ctx, member: discord.Member):
        """Unban a player (Admin only)"""
        try:
            if self.rsps_manager.rsps.unban_player(str(member.id)):
                await ctx.send(f"✅ Unbanned {member.display_name}!")
                logger.info(f"{ctx.author} unbanned {member}")
            else:
                await ctx.send(f"❌ {member.mention} no account.")
        except Exception as e:
            logger.error(f"Unban error: {e}")
            await ctx.send("❌ Unban failed.")

    @commands.command(name=\'resetpass\')
    @commands.has_permissions(administrator=True)
    async def reset_password(self, ctx, member: discord.Member):
        """Reset player password (Admin only)"""
        try:
            new_password = self.rsps_manager.rsps.reset_password(str(member.id))
            if new_password:
                try:
                    await member.send(f"🔑 Password reset: ||`{new_password}`||")
                    await ctx.send(f"✅ Password reset for {member.display_name}! DM sent.")
                    logger.info(f"{ctx.author} reset password for {member}")
                except discord.Forbidden:
                    await ctx.send(f"✅ Reset, but no DM. Password: ||`{new_password}`||")
            else:
                await ctx.send(f"❌ {member.mention} no account.")
        except Exception as e:
            logger.error(f"Resetpass error: {e}")
            await ctx.send("❌ Resetpass failed.")

    @commands.command(name=\'broadcast\')
    @commands.has_permissions(administrator=True)
    async def broadcast(self, ctx, *, message: str):
        """Send announcement to announcements channel (Admin only)"""
        try:
            announcements = discord.utils.get(ctx.guild.text_channels, name=\'announcements\')
            if announcements:
                embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.red(), timestamp=datetime.now())
                embed.set_footer(text=f"By {ctx.author.display_name}")
                await announcements.send(embed=embed)
                await ctx.send("✅ Sent!")
                logger.info(f"{ctx.author} broadcast: {message}")
            else:
                await ctx.send("❌ No announcements channel.")
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            await ctx.send("❌ Broadcast failed.")

    @commands.command(name=\'setup\')
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Advanced server setup with channels and roles"""
        try:
            await ctx.send("🚀 Setup starting...")
            
            # Create categories
            categories = {}
            for cat_name in set(ch[\'category\'] for ch in Config.CHANNELS.values()):
                category = discord.utils.get(ctx.guild.categories, name=cat_name)
                if not category:
                    category = await ctx.guild.create_category(cat_name)
                    logger.info(f"Created category: {cat_name}")
                categories[cat_name] = category
            
            # Create roles
            for role_name, role_config in Config.ROLES.items():
                existing = discord.utils.get(ctx.guild.roles, name=role_name)
                if not existing:
                    perms_dict = {p: True for p in role_config[\'permissions’]}
                    permissions = Permissions(**perms_dict)
                    role = await ctx.guild.create_role(
                        name=role_name,
                        color=role_config[\'color\'],
                        hoist=role_config[\'hoist\'],
                        mentionable=role_config[\'mentionable\'],
                        permissions=permissions
                    )
                    logger.info(f"Created role: {role_name}")
                else:
                    logger.info(f"Role already exists: {role_name}")

            # Create channels
            for ch_name, ch_config in Config.CHANNELS.items():
                existing = discord.utils.get(ctx.guild.text_channels, name=ch_name)
                if not existing:
                    category = categories.get(ch_config[\'category\'])
                    if category:
                        await ctx.guild.create_text_channel(name=ch_name, category=category, topic=ch_config[\'topic\'], nsfw=ch_config[\'nsfw\'])
                        logger.info(f"Created channel: {ch_name}")
                    else:
                        logger.warning(f"Category {ch_config[\'category\']} not found for channel {ch_name}")
                else:
                    logger.info(f"Channel already exists: {ch_name}")

            self.setup_status[str(ctx.guild.id)] = {\'guild_name\': ctx.guild.name, \'setup_date\': datetime.now().isoformat(), \'status\': \'completed\'}
            self.save_configs()
            await ctx.send("✅ Setup complete!")
            logger.info(f"Setup for {ctx.guild.name}")
        except Exception as e:
            logger.error(f"Setup error: {e}")
            await ctx.send(f"❌ Setup failed: {str(e)}")

    @commands.command(name=\'wipe\')
    @commands.has_permissions(administrator=True)
    async def wipe(self, ctx):
        """Wipe RSPS data (dangerous, admin only)"""
        try:
            msg = await ctx.send("⚠️ Wipe all data? Type \'yes\' to confirm (30s).")
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == \'yes\'
            await self.bot.wait_for(\'message\', check=check, timeout=30.0)
            self.rsps_manager.wipe_players()
            await ctx.send("✅ Wiped.")
            logger.info(f"{ctx.author} wiped data")
        except asyncio.TimeoutError:
            await ctx.send("❌ Wipe cancelled.")
        except Exception as e:
            logger.error(f"Wipe error: {e}")
            await ctx.send("❌ Wipe failed.")

    @commands.command(name=\'remake\')
    @commands.has_permissions(administrator=True)
    async def remake(self, ctx):
        """Remake channels and roles (admin only)"""
        try:
            await self.setup(ctx)  # Reuse setup for remake
            await ctx.send("✅ Remake complete.")
        except Exception as e:
            logger.error(f"Remake error: {e}")
            await ctx.send("❌ Remake failed.")

    @commands.group(name=\'role\')
    @commands.has_permissions(administrator=True)
    async def role(self, ctx):
        """Roles manager"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Use: !role add/remove/list")

    @role.command(name=\'add\')
    async def role_add(self, ctx, member: discord.Member, *, role_name: str):
        """Add role to user"""
        try:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                await member.add_roles(role)
                await ctx.send(f"✅ Added {role_name} to {member.mention}")
            else:
                await ctx.send(f"❌ {role_name} not found.")
        except Exception as e:
            logger.error(f"Role add error: {e}")
            await ctx.send("❌ Add failed.")

    @role.command(name=\'remove\')
    async def role_remove(self, ctx, member: discord.Member, *, role_name: str):
        """Remove role from user"""
        try:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role:
                await member.remove_roles(role)
                await ctx.send(f"✅ Removed {role_name} from {member.mention}")
            else:
                await ctx.send(f"❌ {role_name} not found.")
        except Exception as e:
            logger.error(f"Role remove error: {e}")
            await ctx.send("❌ Remove failed.")

    @role.command(name=\'list\')
    async def role_list(self, ctx):
        """List roles"""
        try:
            roles = "\n".join(r.name for r in ctx.guild.roles)
            embed = discord.Embed(title="Roles List", description=roles, color=discord.Color.blue())
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Role list error: {e}")
            await ctx.send("❌ List failed.")

    @commands.command(name=\'lbimage\')
    async def lb_image(self, ctx):
        """Image visualizer for leaderboard"""
        try:
            gp_leaders = self.rsps_manager.rsps.get_leaderboard(\'gp_balance\', 5)
            if not gp_leaders:
                await ctx.send("❌ No leaders.")
                return
            names = [p[\'username\'] for p in gp_leaders]
            balances = [p[\'gp_balance\'] for p in gp_leaders]
            fig, ax = plt.subplots()
            ax.bar(names, balances)
            ax.set_title("Top GP Leaders")
            ax.set_ylabel("GP")
            buf = io.BytesIO()
            fig.savefig(buf, format=\'png\')
            buf.seek(0)
            file = discord.File(buf, filename="lb.png")
            await ctx.send(file=file)
        except Exception as e:
            logger.error(f"Lbimage error: {e}")
            await ctx.send("❌ Image failed.")

# ============================================================================
# Bot Initialization
# ============================================================================
class CustomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(command_prefix=Config.COMMAND_PREFIX, intents=intents, help_command=None)

    async def setup_hook(self):
        await self.add_cog(CloutScapeBot(self))
        await self.load_extension("cogs.economy")
        await self.load_extension("cogs.games")
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.profiles")
        logger.info("Cog loaded")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        logger.info(f"In {len(self.guilds)} guilds")
        await self.change_presence(activity=discord.Game(name=Config.BOT_STATUS))
        logger.info("Ready!")

    async def on_member_join(self, member):
        general = discord.utils.get(member.guild.text_channels, name=\'general\')
        if general:
            embed = discord.Embed(
                title=f"Welcome {member.display_name}!",
                description="Get started with !register",
                color=discord.Color.green()
            )
            await general.send(embed=embed)

def main():
    if not Config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN is missing")
        sys.exit(1)

    bot = CustomBot()

    try:
        bot.run(Config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid token — check DISCORD_TOKEN")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Bot startup failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
