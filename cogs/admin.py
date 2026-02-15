import discord
from discord.ext import commands
import logging
from datetime import datetime

from modules.rsps_integration import RSPSIntegration

logger = logging.getLogger(__name__)

class Admin(commands.Cog):
    """Handles all administrative commands and server management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rsps_integration = RSPSIntegration()

    @commands.command(name=\'addgp\')
    @commands.has_permissions(administrator=True)
    async def add_gp(self, ctx, member: discord.Member, amount: int):
        """Add GP to a player (Admin only)"""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return

        try:
            if self.rsps_integration.add_gp(str(member.id), amount):
                account = self.rsps_integration.get_player_stats(str(member.id))
                embed = discord.Embed(
                    title="✅ GP Added",
                    description=f"Added {amount:,} GP to {member.display_name}",
                    color=discord.Color.green()
                )
                embed.add_field(name="New Balance", value=f"{account['gp_balance']:,} GP", inline=False)
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} added {amount} GP to {member.display_name}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Add GP error: {e}")
            await ctx.send("❌ Failed to add GP.")

    @commands.command(name=\'removegp\')
    @commands.has_permissions(administrator=True)
    async def remove_gp(self, ctx, member: discord.Member, amount: int):
        """Remove GP from a player (Admin only)"""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return

        try:
            if self.rsps_integration.remove_gp(str(member.id), amount):
                account = self.rsps_integration.get_player_stats(str(member.id))
                embed = discord.Embed(
                    title="✅ GP Removed",
                    description=f"Removed {amount:,} GP from {member.display_name}",
                    color=discord.Color.orange()
                )
                embed.add_field(name="New Balance", value=f"{account['gp_balance']:,} GP", inline=False)
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} removed {amount} GP from {member.display_name}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Remove GP error: {e}")
            await ctx.send("❌ Failed to remove GP.")

    @commands.command(name=\'setgp\')
    @commands.has_permissions(administrator=True)
    async def set_gp(self, ctx, member: discord.Member, amount: int):
        """Set a player\'s GP balance to a specific amount (Admin only)"""
        if amount < 0:
            await ctx.send("❌ Amount cannot be negative.")
            return

        try:
            account = self.rsps_integration.get_account(str(member.id))
            if account:
                current_balance = account.get(\'gp_balance\', 0)
                difference = amount - current_balance
                
                if difference > 0:
                    self.rsps_integration.add_gp(str(member.id), difference)
                elif difference < 0:
                    self.rsps_integration.remove_gp(str(member.id), abs(difference))
                
                embed = discord.Embed(
                    title="✅ GP Balance Set",
                    description=f"Set {member.display_name}\'s GP to {amount:,}",
                    color=discord.Color.green()
                )
                embed.add_field(name="Previous Balance", value=f"{current_balance:,} GP", inline=True)
                embed.add_field(name="New Balance", value=f"{amount:,} GP", inline=True)
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} set {member.display_name}\'s GP to {amount}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Set GP error: {e}")
            await ctx.send("❌ Failed to set GP.")

    @commands.command(name=\'ban\')
    @commands.has_permissions(administrator=True)
    async def ban_player(self, ctx, member: discord.Member, *, reason: str = "Violation of rules"):
        """Ban a player (Admin only)"""
        try:
            if self.rsps_integration.ban_player(str(member.id), reason):
                embed = discord.Embed(
                    title="✅ Player Banned",
                    description=f"Banned {member.display_name}",
                    color=discord.Color.red()
                )
                embed.add_field(name="Reason", value=reason, inline=False)
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} banned {member.display_name}: {reason}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Ban error: {e}")
            await ctx.send("❌ Failed to ban player.")

    @commands.command(name=\'unban\')
    @commands.has_permissions(administrator=True)
    async def unban_player(self, ctx, member: discord.Member):
        """Unban a player (Admin only)"""
        try:
            if self.rsps_integration.unban_player(str(member.id)):
                embed = discord.Embed(
                    title="✅ Player Unbanned",
                    description=f"Unbanned {member.display_name}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} unbanned {member.display_name}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Unban error: {e}")
            await ctx.send("❌ Failed to unban player.")

    @commands.command(name=\'resetpass\')
    @commands.has_permissions(administrator=True)
    async def reset_password(self, ctx, member: discord.Member):
        """Reset a player\'s password (Admin only)"""
        try:
            new_password = self.rsps_integration.reset_password(str(member.id))
            if new_password:
                try:
                    embed = discord.Embed(
                        title="🔑 Password Reset",
                        description=f"Your password has been reset by an administrator.",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="New Password", value=f"||`{new_password}`||", inline=False)
                    embed.set_footer(text="Keep this password safe!")
                    await member.send(embed=embed)
                    await ctx.send(f"✅ Password reset for {member.display_name}! DM sent.")
                    logger.info(f"{ctx.author.display_name} reset password for {member.display_name}")
                except discord.Forbidden:
                    await ctx.send(f"✅ Password reset, but couldn\'t DM. New password: ||`{new_password}`||")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Reset password error: {e}")
            await ctx.send("❌ Failed to reset password.")

    @commands.command(name=\'broadcast\')
    @commands.has_permissions(administrator=True)
    async def broadcast(self, ctx, *, message: str):
        """Send an announcement to the announcements channel (Admin only)"""
        try:
            announcements = discord.utils.get(ctx.guild.text_channels, name=\'announcements\')
            if announcements:
                embed = discord.Embed(
                    title="📢 Announcement",
                    description=message,
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"By {ctx.author.display_name}")
                await announcements.send(embed=embed)
                await ctx.send("✅ Announcement sent!")
                logger.info(f"{ctx.author.display_name} broadcast: {message}")
            else:
                await ctx.send("❌ No announcements channel found.")
        except Exception as e:
            logger.error(f"Broadcast error: {e}")
            await ctx.send("❌ Failed to send announcement.")

    @commands.command(name=\'players\')
    @commands.has_permissions(administrator=True)
    async def list_players(self, ctx):
        """List all registered players (Admin only)"""
        try:
            players = self.rsps_integration.get_all_players()
            if not players:
                await ctx.send("❌ No registered players.")
                return

            embed = discord.Embed(title="👥 Registered Players", color=discord.Color.blue())
            
            player_list = ""
            for i, player in enumerate(players[:20], 1): # Show first 20
                status = "🔴 Banned" if player.get(\'is_banned\') else "✅ Active"
                player_list += f"{i}. {player[\'username\']} - {player[\'gp_balance\']:,} GP {status}\n"
            
            embed.description = player_list
            embed.set_footer(text=f"Total players: {len(players)}")
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"List players error: {e}")
            await ctx.send("❌ Failed to list players.")

    @commands.command(name=\'delaccount\')
    @commands.has_permissions(administrator=True)
    async def delete_account(self, ctx, member: discord.Member):
        """Delete a player\'s account (Admin only)"""
        try:
            account = self.rsps_integration.get_account(str(member.id))
            if account:
                username = account[\'username\']
                self.rsps_integration.delete_account(str(member.id))
                embed = discord.Embed(
                    title="✅ Account Deleted",
                    description=f"Deleted account for {member.display_name} ({username})",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} deleted account for {member.display_name}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Delete account error: {e}")
            await ctx.send("❌ Failed to delete account.")

    @commands.command(name=\'setrank\')
    @commands.has_permissions(administrator=True)
    async def set_rank(self, ctx, member: discord.Member, *, rank: str):
        """Set a player\'s rank (Admin only)"""
        try:
            if self.rsps_integration.set_rank(str(member.id), rank):
                embed = discord.Embed(
                    title="✅ Rank Set",
                    description=f"Set {member.display_name}\'s rank to {rank}",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                logger.info(f"{ctx.author.display_name} set {member.display_name}\'s rank to {rank}")
            else:
                await ctx.send(f"❌ {member.mention} does not have a registered account.")
        except Exception as e:
            logger.error(f"Set rank error: {e}")
            await ctx.send("❌ Failed to set rank.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
