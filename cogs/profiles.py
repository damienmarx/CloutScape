import discord
from discord.ext import commands
import logging
from datetime import datetime

from modules.rsps_integration import RSPSIntegration

logger = logging.getLogger(__name__)

class Profiles(commands.Cog):
    """Handles player profiles, progression, and statistics."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rsps_integration = RSPSIntegration()

    @commands.command(name=\'profile\', aliases=[\'p\'])
    async def profile(self, ctx, member: discord.Member = None):
        """View your or another player\'s profile"""
        member = member or ctx.author
        player_id = str(member.id)

        account = self.rsps_integration.get_player_stats(player_id)

        if account:
            embed = discord.Embed(
                title=f"👤 {account[\'username\']}\'s Profile",
                description=f"Rank: **{account[\'rank\']}**",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            embed.add_field(name="💰 GP Balance", value=f"{account[\'gp_balance\']:,}", inline=True)
            embed.add_field(name="📊 Total Logins", value=account[\'total_logins\'], inline=True)
            embed.add_field(name="🔒 Status", value="🔴 Banned" if account[\'is_banned\'] else "✅ Active", inline=True)
            embed.add_field(name="📅 Created", value=account[\'created_at\'].split(\'T\')[0], inline=True)
            embed.add_field(name="🕐 Last Login", value=account[\'last_login\'] if account[\'last_login\'] else "Never", inline=True)
            embed.set_footer(text=f"Discord: {member.display_name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {member.mention} does not have a registered account.")

    @commands.command(name=\'stats\')
    async def stats(self, ctx, member: discord.Member = None):
        """View detailed statistics for a player"""
        member = member or ctx.author
        player_id = str(member.id)

        account = self.rsps_integration.get_player_stats(player_id)

        if account:
            embed = discord.Embed(
                title=f"📊 {account[\'username\']}\'s Statistics",
                color=discord.Color.gold()
            )
            embed.add_field(name="Rank", value=account[\'rank\'], inline=True)
            embed.add_field(name="GP Balance", value=f"{account[\'gp_balance\']:,}", inline=True)
            embed.add_field(name="Total Logins", value=account[\'total_logins\'], inline=True)
            embed.add_field(name="Account Age", value=account[\'created_at\'].split(\'T\')[0], inline=True)
            embed.add_field(name="Status", value="🔴 Banned" if account[\'is_banned\'] else "✅ Active", inline=True)
            
            # Calculate account age in days
            created_date = datetime.fromisoformat(account[\'created_at\'])
            age_days = (datetime.now() - created_date).days
            embed.add_field(name="Account Age (Days)", value=age_days, inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {member.mention} does not have a registered account.")

    @commands.command(name=\'leaderboard\', aliases=[\'lb\'])
    async def leaderboard(self, ctx, sort_by: str = \'gp\'):
        """View the top players by GP or other stats"""
        valid_sorts = {\'gp\': \'gp_balance\', \'logins\': \'total_logins\'}
        
        if sort_by.lower() not in valid_sorts:
            await ctx.send("❌ Invalid sort option. Use `gp` or `logins`.")
            return

        sort_field = valid_sorts[sort_by.lower()]
        leaders = self.rsps_integration.get_leaderboard(sort_field, 10)

        if not leaders:
            await ctx.send("❌ No leaders to display yet.")
            return

        if sort_by.lower() == \'gp\':
            title = "🏆 Top 10 GP Leaders"
            field_name = "GP Balance"
        else:
            title = "📊 Top 10 Most Active"
            field_name = "Total Logins"

        embed = discord.Embed(title=title, color=discord.Color.gold())
        
        description = ""
        for i, player in enumerate(leaders, 1):
            if sort_by.lower() == \'gp\':
                value = f"{player[\'gp_balance\']:,} GP"
            else:
                value = f"{player[\'total_logins\']} logins"
            description += f"{i}. **{player[\'username\']}** - {value}\n"
        
        embed.description = description
        await ctx.send(embed=embed)

    @commands.command(name=\'achievements\')
    async def achievements(self, ctx, member: discord.Member = None):
        """View achievements for a player"""
        member = member or ctx.author
        player_id = str(member.id)

        account = self.rsps_integration.get_player_stats(player_id)

        if not account:
            await ctx.send(f"❌ {member.mention} does not have a registered account.")
            return

        embed = discord.Embed(
            title=f"🏅 {account[\'username\']}\'s Achievements",
            color=discord.Color.purple()
        )

        # Define achievements based on stats
        achievements = []
        
        if account[\'gp_balance\'] >= 1000000:
            achievements.append("💰 **Millionaire** - Reached 1M GP")
        elif account[\'gp_balance\'] >= 100000:
            achievements.append("💵 **Wealthy** - Reached 100K GP")
        
        if account[\'total_logins\'] >= 100:
            achievements.append("📅 **Dedicated** - 100+ logins")
        elif account[\'total_logins\'] >= 50:
            achievements.append("📅 **Regular** - 50+ logins")
        
        if account[\'rank\'] == \'VIP\':
            achievements.append("💎 **VIP Member** - Premium status")
        elif account[\'rank\'] == \'Legend\':
            achievements.append("⭐ **Legend** - Legendary rank")
        
        if not achievements:
            achievements.append("🔓 **Newcomer** - Just getting started!")

        embed.description = "\n".join(achievements)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profiles(bot))
