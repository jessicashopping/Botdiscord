import discord
from discord.ext import commands
import random

class Jokes(commands.Cog):
    """Comando per battute e freddure a tema D&D."""

    def __init__(self, bot):
        self.bot = bot
        # Lista di battute/freddure D&D
        self.jokes = [
            "Perché il ladro porta sempre una corda? Perché non vuole restare legato alle regole!",
            "Sai perché il bardo non usa mai l'arco? Perché preferisce le note!",
            "Un orco entra in un bar e dice: 'Birra! E non fate storie… o vi riduco in brandelli!'",
            "Perché il druido non va mai in vacanza? Perché ogni volta che cambia forma, perde il bagaglio!",
            "Cosa dice un mago quando perde la bacchetta? 'Accio panico!'",
            "Perché il chierico ama i dadi? Perché non importa il risultato, è sempre benedetto!",
            "Come chiami un goblin che sa cucinare? Uno chef di basso livello!",
            "Perché i draghi non giocano a dadi? Perché hanno paura del critico!",
            "Cosa fa un paladino quando cade in un pozzo? Contempla la propria fede!",
            "Sai perché i nani non raccontano mai barzellette? Perché fanno sempre scendere la morale!",
            # Puoi aggiungerne altre ancora…
        ]

    @commands.command()
    async def joke(self, ctx):
        """Invia una battuta/freddura casuale a tema D&D."""
        joke = random.choice(self.jokes)
        embed = discord.Embed(
            title="🤣 Freddura del tavolo",
            description=joke,
            color=0x9b59b6
        )
        embed.set_footer(text="D&D Bot • Divertiti al tavolo!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Jokes(bot))
