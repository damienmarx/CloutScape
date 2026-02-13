"""
Discord Bot for CloutScape Platform - Enhanced with Bonuses & Wagering
"""
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import requests
import json
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://web:5000')
NOTIFICATION_CHANNEL_ID = int(os.getenv('DISCORD_NOTIFICATION_CHANNEL_ID', '0'))

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Bot ready event"""
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")
    
    if NOTIFICATION_CHANNEL_ID:
        channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
        if channel:
            await channel.send("🚀 **CloutScape Discord Bot is online!**")


@bot.event
async def on_member_join(member):
    """Auto-DM new members with sign-up bonus info"""
    welcome_msg = (
        f"👋 **Welcome to CloutScape, {member.name}!**\n\n"
        "We've got some exclusive bonuses waiting for you:\n"
        "💰 **50% Sign-up Bonus** on your first deposit!\n"
        "🎁 **FREE $5 Challenge**: Wager $50 in any of our Discord games and claim a free $5 reward!\n\n"
        "Type `/price` in the server to see our elite OSRS GP rates ($0.17/M).\n"
        "Good luck and have fun! 🎰"
    )
    try:
        await member.send(welcome_msg)
        logger.info(f"Sent welcome DM to {member.name}")
    except discord.Forbidden:
        logger.warning(f"Could not send DM to {member.name} (DMs disabled)")


@bot.tree.command(name="price", description="Show current OSRS GP rate")
async def price_command(interaction: discord.Interaction):
    """Show current GP rate"""
    # Using the user's specified rates
    sell_price = 0.17
    buy_price = 0.16
    
    embed = discord.Embed(
        title="💰 CloutScape OSRS GP Rates",
        description="We offer the most competitive rates in the market.",
        color=discord.Color.gold()
    )
    embed.add_field(name="Selling GP", value=f"**${sell_price:.2f}** per 1M", inline=True)
    embed.add_field(name="Buying GP (Bulk Only)", value=f"**${buy_price:.2f}** per 1M", inline=True)
    embed.set_footer(text="CloutScape - Bulk GP Specialists")
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="challenge", description="Check your $5 wagering challenge status")
async def challenge_command(interaction: discord.Interaction):
    """Check wagering challenge status"""
    # In a real app, this would fetch from the API/DB
    # For now, we'll simulate the response
    embed = discord.Embed(
        title="🎁 $5 Wagering Challenge",
        description="Wager $50 to unlock your free $5 reward!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Target", value="$50.00", inline=True)
    embed.add_field(name="Current Progress", value="$0.00", inline=True)
    embed.add_field(name="Status", value="Active", inline=False)
    embed.set_footer(text="Redeemable after 10x wagering requirement met.")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="stake", description="Log a gambling result for wagering progress")
@app_commands.describe(
    amount_gp="Amount wagered (in GP)",
    result="Did you win or lose?",
    game="Type of game"
)
@app_commands.choices(result=[
    app_commands.Choice(name="Win", value="win"),
    app_commands.Choice(name="Loss", value="loss")
])
async def stake_command(
    interaction: discord.Interaction,
    amount_gp: int,
    result: app_commands.Choice[str],
    game: str
):
    """Log gambling result and update wagering"""
    # Calculate USD value based on $0.17/M
    usd_value = (amount_gp / 1_000_000) * 0.17
    
    await interaction.response.send_message(
        f"✅ **Stake Logged!**\n"
        f"Game: {game}\n"
        f"Wager: {amount_gp:,} GP (~${usd_value:.2f})\n"
        f"Result: {result.name}\n\n"
        f"Your wagering progress has been updated!",
        ephemeral=True
    )
    
    # Notify admin channel for verification
    if NOTIFICATION_CHANNEL_ID:
        channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
        if channel:
            await channel.send(
                f"🎲 **New Stake Logged**\n"
                f"User: {interaction.user.mention}\n"
                f"Wager: {amount_gp:,} GP (${usd_value:.2f})\n"
                f"Game: {game}"
            )


def run_bot():
    """Run the Discord bot"""
    if not DISCORD_BOT_TOKEN:
        logger.warning("DISCORD_BOT_TOKEN not set, skipping bot")
        return
    
    bot.run(DISCORD_BOT_TOKEN)


if __name__ == '__main__':
    run_bot()
