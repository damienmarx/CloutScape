import discord
from discord.ext import commands
import logging

from modules.rsps_integration import RSPSIntegration

logger = logging.getLogger(__name__)

class Economy(commands.Cog):
    """Handles all economy-related commands and interactions."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rsps_integration = RSPSIntegration() # Initialize RSPS integration

    @commands.command(name='balance', aliases=['bal', 'gp'])
    async def balance(self, ctx):
        """Check your current GP balance."""
        player_id = str(ctx.author.id)
        account = self.rsps_integration.get_player_stats(player_id)

        if account:
            embed = discord.Embed(
                title=f"💰 {ctx.author.display_name}'s Balance",
                description=f"You currently have **{account['gp_balance']:,} GP**.",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {ctx.author.mention}, you don't have a registered account. Use `!register <username>` to create one.")

    @commands.command(name='transfer')
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer GP to another player."""
        if amount <= 0:
            await ctx.send("❌ You can only transfer positive amounts of GP.")
            return

        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        if sender_id == receiver_id:
            await ctx.send("❌ You cannot transfer GP to yourself.")
            return

        sender_account = self.rsps_integration.get_player_stats(sender_id)
        receiver_account = self.rsps_integration.get_player_stats(receiver_id)

        if not sender_account:
            await ctx.send(f"❌ {ctx.author.mention}, you don't have a registered account.")
            return
        if not receiver_account:
            await ctx.send(f"❌ {member.mention} does not have a registered account.")
            return

        if sender_account['gp_balance'] < amount:
            await ctx.send(f"❌ {ctx.author.mention}, you do not have enough GP to transfer {amount:,} GP.")
            return

        # Perform the transfer
        self.rsps_integration.remove_gp(sender_id, amount)
        self.rsps_integration.add_gp(receiver_id, amount)

        embed = discord.Embed(
            title="💸 GP Transfer Successful!",
            description=f"**{ctx.author.display_name}** transferred **{amount:,} GP** to **{member.display_name}**.",
            color=discord.Color.green()
        )
        embed.add_field(name="Your New Balance", value=f"{self.rsps_integration.get_player_stats(sender_id)['gp_balance']:,} GP", inline=True)
        embed.add_field(name=f"{member.display_name}'s New Balance", value=f"{self.rsps_integration.get_player_stats(receiver_id)['gp_balance']:,} GP", inline=True)
        await ctx.send(embed=embed)
        logger.info(f"{ctx.author.display_name} transferred {amount} GP to {member.display_name}")

async def setup(bot):
    await bot.add_cog(Economy(bot))
