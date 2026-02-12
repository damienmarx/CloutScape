#!/usr/bin/env python3
"""
CloutScape AIO - Discord Setup Bot
Automatically configures Discord servers with all required channels, roles, and permissions.
Only requires: Discord Token and Admin ID
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
    
    # Bot Configuration
    COMMAND_PREFIX = '!'
    BOT_STATUS = 'CloutScape AIO Setup'
    
    # Channel Configuration
    CHANNELS = {
        'announcements': {
            'description': 'Server announcements and updates',
            'topic': 'Important announcements for CloutScape AIO',
            'nsfw': False,
            'category': 'Information'
        },
        'giveaways': {
            'description': 'Giveaway announcements and entries',
            'topic': 'Participate in exciting giveaways',
            'nsfw': False,
            'category': 'Events'
        },
        'gambling-logs': {
            'description': 'Real-time gambling activity logs',
            'topic': 'Dice, Poker, Blackjack results',
            'nsfw': False,
            'category': 'Gaming'
        },
        'pvp-kills': {
            'description': 'PvP kill logs and loot drops',
            'topic': 'Track PvP activity and rewards',
            'nsfw': False,
            'category': 'Gaming'
        },
        'leaderboards': {
            'description': 'Community leaderboards and rankings',
            'topic': 'Top players and achievements',
            'nsfw': False,
            'category': 'Community'
        },
        'events': {
            'description': 'Event announcements and updates',
            'topic': 'Tournaments, raids, and special events',
            'nsfw': False,
            'category': 'Events'
        },
        'general': {
            'description': 'General discussion channel',
            'topic': 'General chat and community discussion',
            'nsfw': False,
            'category': 'Community'
        },
        'bot-commands': {
            'description': 'Bot commands and interactions',
            'topic': 'Use bot commands here',
            'nsfw': False,
            'category': 'Bot'
        },
        'logs': {
            'description': 'Bot activity logs',
            'topic': 'System logs and errors',
            'nsfw': False,
            'category': 'Admin'
        },
        'admin': {
            'description': 'Admin-only channel',
            'topic': 'Administrative discussions',
            'nsfw': False,
            'category': 'Admin'
        }
    }
    
    # Role Configuration
    ROLES = {
        'Admin': {
            'color': discord.Color.red(),
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'administrator'
            ]
        },
        'Event Manager': {
            'color': discord.Color.gold(),
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'manage_channels',
                'manage_roles',
                'manage_messages',
                'send_messages',
                'embed_links',
                'attach_files'
            ]
        },
        'VIP': {
            'color': discord.Color.purple(),
            'hoist': True,
            'mentionable': True,
            'permissions': [
                'send_messages',
                'embed_links',
                'attach_files',
                'read_message_history'
            ]
        },
        'Member': {
            'color': discord.Color.blue(),
            'hoist': False,
            'mentionable': False,
            'permissions': [
                'send_messages',
                'read_message_history'
            ]
        },
        'Muted': {
            'color': discord.Color.greyple(),
            'hoist': False,
            'mentionable': False,
            'permissions': [
                'read_messages',
                'connect'
            ]
        }
    }

# ============================================================================
# Discord Bot
# ============================================================================

class CloutScapeBot(commands.Cog):
    """Main bot cog for CloutScape setup"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config_file = 'server_config.json'
        self.setup_status = {}
        self.load_configs()
    
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
    
    async def create_categories(self, guild: discord.Guild) -> Dict[str, discord.CategoryChannel]:
        """Create channel categories"""
        categories = {}
        category_names = set(ch['category'] for ch in Config.CHANNELS.values())
        
        for cat_name in category_names:
            try:
                category = await guild.create_category(cat_name)
                categories[cat_name] = category
                logger.info(f"Created category: {cat_name}")
            except Exception as e:
                logger.error(f"Error creating category {cat_name}: {e}")
        
        return categories
    
    async def create_channels(self, guild: discord.Guild, categories: Dict[str, discord.CategoryChannel]) -> Dict[str, discord.TextChannel]:
        """Create all required channels"""
        channels = {}
        
        for channel_name, channel_config in Config.CHANNELS.items():
            try:
                category = categories.get(channel_config['category'])
                
                channel = await guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    topic=channel_config['topic'],
                    nsfw=channel_config['nsfw']
                )
                
                # Set channel permissions
                await self.set_channel_permissions(channel, guild)
                
                channels[channel_name] = channel
                logger.info(f"Created channel: {channel_name}")
                
            except Exception as e:
                logger.error(f"Error creating channel {channel_name}: {e}")
        
        return channels
    
    async def set_channel_permissions(self, channel: discord.TextChannel, guild: discord.Guild):
        """Set channel-specific permissions"""
        try:
            # Default: deny everyone
            await channel.set_permissions(
                guild.default_role,
                send_messages=False,
                read_messages=True
            )
            
            # Allow specific roles based on channel
            if 'admin' in channel.name:
                admin_role = discord.utils.get(guild.roles, name='Admin')
                if admin_role:
                    await channel.set_permissions(
                        admin_role,
                        send_messages=True,
                        manage_messages=True,
                        read_messages=True
                    )
            
            elif 'logs' in channel.name:
                admin_role = discord.utils.get(guild.roles, name='Admin')
                if admin_role:
                    await channel.set_permissions(
                        admin_role,
                        send_messages=True,
                        read_messages=True
                    )
            
            else:
                # Allow member role to send messages
                member_role = discord.utils.get(guild.roles, name='Member')
                if member_role:
                    await channel.set_permissions(
                        member_role,
                        send_messages=True,
                        read_messages=True
                    )
            
        except Exception as e:
            logger.error(f"Error setting permissions for {channel.name}: {e}")
    
    async def create_roles(self, guild: discord.Guild) -> Dict[str, discord.Role]:
        """Create all required roles"""
        roles = {}
        
        for role_name, role_config in Config.ROLES.items():
            try:
                # Check if role already exists
                existing_role = discord.utils.get(guild.roles, name=role_name)
                if existing_role:
                    logger.info(f"Role already exists: {role_name}")
                    roles[role_name] = existing_role
                    continue
                
                # Create permissions
                perms_dict = {}
                for perm in role_config['permissions']:
                    perms_dict[perm] = True
                
                permissions = Permissions(**perms_dict)
                
                # Create role
                role = await guild.create_role(
                    name=role_name,
                    color=role_config['color'],
                    hoist=role_config['hoist'],
                    mentionable=role_config['mentionable'],
                    permissions=permissions
                )
                
                roles[role_name] = role
                logger.info(f"Created role: {role_name}")
                
            except Exception as e:
                logger.error(f"Error creating role {role_name}: {e}")
        
        return roles
    
    async def setup_server(self, guild: discord.Guild) -> bool:
        """Complete server setup"""
        try:
            logger.info(f"Starting setup for server: {guild.name} (ID: {guild.id})")
            
            # Create roles
            roles = await self.create_roles(guild)
            logger.info(f"Created {len(roles)} roles")
            
            # Create categories
            categories = await self.create_categories(guild)
            logger.info(f"Created {len(categories)} categories")
            
            # Create channels
            channels = await self.create_channels(guild, categories)
            logger.info(f"Created {len(channels)} channels")
            
            # Save configuration
            self.setup_status[str(guild.id)] = {
                'guild_name': guild.name,
                'setup_date': datetime.now().isoformat(),
                'roles': len(roles),
                'categories': len(categories),
                'channels': len(channels),
                'status': 'completed'
            }
            self.save_configs()
            
            logger.info(f"Setup completed for {guild.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error during server setup: {e}")
            return False
    
    @commands.command(name='setup')
    @commands.has_permissions(administrator=True)
    async def setup_command(self, ctx: commands.Context):
        """Setup the server with all required channels and roles"""
        
        # Check if already setup
        guild_id = str(ctx.guild.id)
        if guild_id in self.setup_status:
            await ctx.send("❌ This server has already been set up!")
            return
        
        # Confirm setup
        embed = discord.Embed(
            title="🚀 CloutScape AIO Setup",
            description="This will create all required channels, roles, and permissions.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="This will create:",
            value=f"• {len(Config.ROLES)} roles\n"
                  f"• {len(set(ch['category'] for ch in Config.CHANNELS.values()))} categories\n"
                  f"• {len(Config.CHANNELS)} channels",
            inline=False
        )
        embed.add_field(
            name="⚠️ Warning",
            value="This action cannot be undone. Proceed?",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
        # Wait for confirmation
        try:
            msg = await self.bot.wait_for(
                'message',
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                timeout=30.0
            )
            
            if msg.content.lower() not in ['yes', 'y', 'confirm']:
                await ctx.send("❌ Setup cancelled.")
                return
            
        except asyncio.TimeoutError:
            await ctx.send("❌ Setup cancelled (timeout).")
            return
        
        # Start setup
        status_msg = await ctx.send("⏳ Setting up server... This may take a minute.")
        
        success = await self.setup_server(ctx.guild)
        
        if success:
            embed = discord.Embed(
                title="✅ Setup Complete!",
                description="Your server has been configured for CloutScape AIO",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Created:",
                value=f"• {len(Config.ROLES)} roles\n"
                      f"• {len(set(ch['category'] for ch in Config.CHANNELS.values()))} categories\n"
                      f"• {len(Config.CHANNELS)} channels",
                inline=False
            )
            embed.add_field(
                name="Next Steps:",
                value="1. Invite the bot to your server\n"
                      "2. Assign roles to members\n"
                      "3. Configure webhook URLs\n"
                      "4. Start using CloutScape AIO!",
                inline=False
            )
            
            await status_msg.edit(content="", embed=embed)
        else:
            await status_msg.edit(content="❌ Setup failed. Check logs for details.")
    
    @commands.command(name='status')
    async def status_command(self, ctx: commands.Context):
        """Check setup status"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.setup_status:
            await ctx.send("❌ This server has not been set up yet. Use `!setup` to get started.")
            return
        
        status = self.setup_status[guild_id]
        
        embed = discord.Embed(
            title="📊 Server Status",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server", value=status['guild_name'], inline=False)
        embed.add_field(name="Setup Date", value=status['setup_date'], inline=False)
        embed.add_field(name="Roles", value=f"{status['roles']} created", inline=True)
        embed.add_field(name="Categories", value=f"{status['categories']} created", inline=True)
        embed.add_field(name="Channels", value=f"{status['channels']} created", inline=True)
        embed.add_field(name="Status", value=f"✅ {status['status']}", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx: commands.Context):
        """Show help message"""
        embed = discord.Embed(
            title="🤖 CloutScape AIO Setup Bot",
            description="Automated Discord server configuration",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Commands:",
            value="**!setup** - Setup the server (Admin only)\n"
                  "**!status** - Check setup status\n"
                  "**!help** - Show this message",
            inline=False
        )
        embed.add_field(
            name="Features:",
            value="✅ Auto-creates 10 channels\n"
                  "✅ Auto-creates 5 roles\n"
                  "✅ Sets up permissions\n"
                  "✅ Saves configuration",
            inline=False
        )
        embed.add_field(
            name="Requirements:",
            value="• Bot must have Administrator permission\n"
                  "• User must be server Administrator",
            inline=False
        )
        
        await ctx.send(embed=embed)


# ============================================================================
# Main Bot
# ============================================================================

def create_bot() -> commands.Bot:
    """Create and configure the bot"""
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    bot = commands.Bot(
        command_prefix=Config.COMMAND_PREFIX,
        intents=intents,
        help_command=None
    )
    
    @bot.event
    async def on_ready():
        logger.info(f"Bot logged in as {bot.user}")
        logger.info(f"Bot is in {len(bot.guilds)} guilds")
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=Config.BOT_STATUS
            )
        )
    
    @bot.event
    async def on_guild_join(guild: discord.Guild):
        logger.info(f"Bot joined guild: {guild.name} (ID: {guild.id})")
    
    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `!help` for available commands.")
        else:
            logger.error(f"Command error: {error}")
            await ctx.send(f"❌ An error occurred: {str(error)}")
    
    return bot


def main():
    """Main entry point"""
    
    # Validate configuration
    if not Config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN environment variable not set")
        sys.exit(1)
    
    if not Config.ADMIN_ID or Config.ADMIN_ID == 0:
        logger.warning("ADMIN_ID not set. Some features may not work.")
    
    # Create bot
    bot = create_bot()
    
    # Add cog
    asyncio.run(bot.add_cog(CloutScapeBot(bot)))
    
    # Run bot
    try:
        logger.info("Starting CloutScape Discord Setup Bot...")
        bot.run(Config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
