import discord
from discord.ext import commands
import logging
import random

from modules.gambling import GamblingSystem, GambleType
from modules.rsps_integration import RSPSIntegration

logger = logging.getLogger(__name__)

class Games(commands.Cog):
    """Handles all casino games and gambling activities."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.gambling_system = GamblingSystem()
        self.rsps_integration = RSPSIntegration()

    async def _check_balance_and_deduct(self, ctx, player_id: str, bet_amount: int) -> bool:
        account = self.rsps_integration.get_player_stats(player_id)
        if not account or account['gp_balance'] < bet_amount:
            await ctx.send(f"❌ {ctx.author.mention}, you don't have enough GP to place that bet. Your current balance is {account['gp_balance']:,} GP.")
            return False
        self.rsps_integration.remove_gp(player_id, bet_amount)
        return True

    async def _payout_winner(self, ctx, player_id: str, player_name: str, winnings: int, game_type: GambleType):
        self.rsps_integration.add_gp(player_id, winnings)
        embed = discord.Embed(
            title=f"🎉 {game_type.value.replace('_', ' ').title()} Winner!",
            description=f"**{player_name}** won **{winnings:,} GP**!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        logger.info(f"{player_name} won {winnings} GP in {game_type.value}")

    async def _handle_loss(self, ctx, player_name: str, bet_amount: int, game_type: GambleType):
        embed = discord.Embed(
            title=f"💸 {game_type.value.replace('_', ' ').title()} Loss!",
            description=f"**{player_name}** lost **{bet_amount:,} GP**.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        logger.info(f"{player_name} lost {bet_amount} GP in {game_type.value}")

    @commands.command(name=\'dice\')
    async def dice_duel(self, ctx, bet_amount: int, opponent: discord.Member):
        """Roll dice against another player. Higher roll wins."""
        if bet_amount <= 0:
            await ctx.send("❌ Bet amount must be positive.")
            return

        player_id = str(ctx.author.id)
        opponent_id = str(opponent.id)

        if player_id == opponent_id:
            await ctx.send("❌ You cannot dice duel yourself.")
            return

        if not await self._check_balance_and_deduct(ctx, player_id, bet_amount):
            return
        if not await self._check_balance_and_deduct(ctx, opponent_id, bet_amount):
            self.rsps_integration.add_gp(player_id, bet_amount) # Refund player
            return

        player_roll = random.randint(1, 100)
        opponent_roll = random.randint(1, 100)

        result = self.gambling_system.roll_dice(player_id, ctx.author.name, bet_amount, player_roll, opponent_roll)

        embed = discord.Embed(title="🎲 Dice Duel!", color=discord.Color.blue())
        embed.add_field(name=f"{ctx.author.display_name}\'s Roll", value=player_roll, inline=True)
        embed.add_field(name=f"{opponent.display_name}\'s Roll", value=opponent_roll, inline=True)

        if result['player_wins']:
            await self._payout_winner(ctx, player_id, ctx.author.display_name, result['winnings'], GambleType.DICE)
            self.rsps_integration.add_gp(opponent_id, bet_amount - result['winnings']) # Refund opponent if they lost less than their bet
            embed.description = f"{ctx.author.mention} wins {result['winnings']:,} GP!"
        elif result['opponent_roll'] > result['player_roll']:
            await self._payout_winner(ctx, opponent_id, opponent.display_name, bet_amount * 2, GambleType.DICE)
            embed.description = f"{opponent.mention} wins {bet_amount * 2:,} GP!"
        else: # Tie
            self.rsps_integration.add_gp(player_id, bet_amount)
            self.rsps_integration.add_gp(opponent_id, bet_amount)
            embed.description = "It's a tie! Bets returned."

        await ctx.send(embed=embed)

    @commands.command(name=\'flowerpoker\', aliases=[\'fp\'])
    async def flower_poker(self, ctx, bet_amount: int, opponent: discord.Member):
        """Play flower poker against another player. Best hand wins."""
        if bet_amount <= 0:
            await ctx.send("❌ Bet amount must be positive.")
            return

        player_id = str(ctx.author.id)
        opponent_id = str(opponent.id)

        if player_id == opponent_id:
            await ctx.send("❌ You cannot play flower poker against yourself.")
            return

        if not await self._check_balance_and_deduct(ctx, player_id, bet_amount):
            return
        if not await self._check_balance_and_deduct(ctx, opponent_id, bet_amount):
            self.rsps_integration.add_gp(player_id, bet_amount) # Refund player
            return

        # Simulate flower poker hands (5 cards, values 1-13 for simplicity)
        player_hand = [random.randint(1, 13) for _ in range(5)]
        opponent_hand = [random.randint(1, 13) for _ in range(5)]

        result = self.gambling_system.flower_poker(player_id, ctx.author.name, bet_amount, player_hand, opponent_hand)

        embed = discord.Embed(title="🌸 Flower Poker!", color=discord.Color.purple())
        embed.add_field(name=f"{ctx.author.display_name}\'s Hand", value=f"{player_hand} (Rank: {result['player_rank']})", inline=False)
        embed.add_field(name=f"{opponent.display_name}\'s Hand", value=f"{opponent_hand} (Rank: {result['opponent_rank']})", inline=False)

        if result['player_wins']:
            await self._payout_winner(ctx, player_id, ctx.author.display_name, result['winnings'], GambleType.FLOWER_POKER)
            self.rsps_integration.add_gp(opponent_id, bet_amount - result['winnings']) # Refund opponent if they lost less than their bet
            embed.description = f"{ctx.author.mention} wins {result['winnings']:,} GP!"
        elif result['opponent_rank'] > result['player_rank']:
            await self._payout_winner(ctx, opponent_id, opponent.display_name, bet_amount * 2, GambleType.FLOWER_POKER)
            embed.description = f"{opponent.mention} wins {bet_amount * 2:,} GP!"
        else: # Tie
            self.rsps_integration.add_gp(player_id, bet_amount)
            self.rsps_integration.add_gp(opponent_id, bet_amount)
            embed.description = "It's a tie! Bets returned."

        await ctx.send(embed=embed)

    @commands.command(name=\'slots\')
    async def slots(self, ctx, bet_amount: int):
        """Spin the slot machine!"""
        if bet_amount <= 0:
            await ctx.send("❌ Bet amount must be positive.")
            return

        player_id = str(ctx.author.id)

        if not await self._check_balance_and_deduct(ctx, player_id, bet_amount):
            return

        result = self.gambling_system.slots(player_id, ctx.author.name, bet_amount)

        reels_str = " | ".join(result['reels'])
        embed = discord.Embed(title="🎰 Slot Machine!", description=f"[{reels_str}]", color=discord.Color.orange())

        if result['player_wins']:
            await self._payout_winner(ctx, player_id, ctx.author.display_name, result['winnings'], GambleType.SLOTS)
            embed.description += f"\n🎉 You won {result['winnings']:,} GP!"
        else:
            await self._handle_loss(ctx, ctx.author.display_name, bet_amount, GambleType.SLOTS)
            embed.description += f"\nBetter luck next time! You lost {bet_amount:,} GP."

        await ctx.send(embed=embed)

    @commands.command(name=\'craps\')
    async def craps(self, ctx, bet_amount: int):
        """Play a simplified game of craps."""
        if bet_amount <= 0:
            await ctx.send("❌ Bet amount must be positive.")
            return

        player_id = str(ctx.author.id)

        if not await self._check_balance_and_deduct(ctx, player_id, bet_amount):
            return

        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        roll = die1 + die2

        player_wins = False
        winnings = 0
        message = f"You rolled {die1} + {die2} = **{roll}**!\n"

        if roll == 7 or roll == 11:
            player_wins = True
            winnings = bet_amount * 2
            message += "🎉 You win!"
        elif roll == 2 or roll == 3 or roll == 12:
            player_wins = False
            message += "Craps! You lose!"
        else:
            point = roll
            message += f"Point is **{point}**. Roll again to hit {point} before a 7.\n"
            await ctx.send(message)
            message = ""

            # Subsequent rolls
            while True:
                await ctx.send("Rolling again...")
                await asyncio.sleep(2) # Simulate delay
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                new_roll = die1 + die2
                message += f"You rolled {die1} + {die2} = **{new_roll}**!\n"

                if new_roll == point:
                    player_wins = True
                    winnings = bet_amount * 2
                    message += "🎉 You hit your point! You win!"
                    break
                elif new_roll == 7:
                    player_wins = False
                    message += "Seven out! You lose!"
                    break
                else:
                    message += f"Still trying for {point}...\n"

        if player_wins:
            self.rsps_integration.add_gp(player_id, winnings)
            embed = discord.Embed(title="🎲 Craps Game!", description=message, color=discord.Color.green())
            embed.add_field(name="Winnings", value=f"{winnings:,} GP", inline=False)
        else:
            embed = discord.Embed(title="🎲 Craps Game!", description=message, color=discord.Color.red())
            embed.add_field(name="Loss", value=f"{bet_amount:,} GP", inline=False)

        await ctx.send(embed=embed)
        logger.info(f"{ctx.author.display_name} played craps. Won: {player_wins}, Winnings: {winnings}")

async def setup(bot):
    await bot.add_cog(Games(bot))
