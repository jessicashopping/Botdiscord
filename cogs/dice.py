import discord
from discord.ext import commands
import random
import re

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *, dice: str):
        """
        Comando per tirare dadi. Puoi usare più tipi di dadi e modificatori.
        Esempio: !roll 1d4 + 1d20 + 3
        """
        try:
            dice_str = dice.replace(" ", "")
            
            # trova tutti i dadi
            dice_pattern = r'(\d*)d(\d+)'
            dice_matches = re.findall(dice_pattern, dice_str)
            
            # rimuovi tutti i dadi dalla stringa, così rimangono solo i modificatori
            dice_cleaned = re.sub(dice_pattern, '', dice_str)
            
            # trova modificatori puri
            mod_pattern = r'([+-]\d+)'
            mod_matches = re.findall(mod_pattern, dice_cleaned)
            mod_total = sum(int(m) for m in mod_matches)

            if not dice_matches and not mod_matches:
                await ctx.send("Formato del dado non valido. Usa ad esempio `1d20` o `2d6+3`.")
                return

            results = []
            total = mod_total
            for count, sides in dice_matches:
                count = int(count) if count else 1
                sides = int(sides)
                rolls = [random.randint(1, sides) for _ in range(count)]
                results.append((f"{count}d{sides}", rolls))
                total += sum(rolls)

            # costruisci embed
            embed = discord.Embed(title="🎲 Risultato Tiro Dadi", color=0x1abc9c)
            for dice_type, rolls in results:
                embed.add_field(name=dice_type, value=", ".join(map(str, rolls)), inline=False)
            if mod_matches:
                embed.add_field(name="Modificatori", value=", ".join(mod_matches), inline=False)
            embed.add_field(name="Totale", value=str(total), inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Errore nel tirare i dadi: {e}")

async def setup(bot):
    await bot.add_cog(Dice(bot))
