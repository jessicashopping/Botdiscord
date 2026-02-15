import random
import discord
from discord.ext import commands


class Coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx):
        risultato = random.choice(["Testa", "Croce"])

        embed = discord.Embed(
            title="🪙 Lancio della moneta",
            description=f"Risultato: **{risultato}**",
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Coin(bot))
