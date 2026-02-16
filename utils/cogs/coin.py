import random
import discord
from discord.ext import commands


PROFEZIE = [
    "Un incontro inaspettato cambierà il corso della tua avventura.",
    "Il prossimo dungeon nasconde più di quanto sembri.",
    "Non fidarti del prossimo NPC che ti offrirà un affare.",
    "Le stelle indicano un grande bottino nel tuo futuro.",
    "Un tradimento si nasconde tra le fila dei tuoi alleati.",
    "La fortuna è dalla tua parte… per ora.",
    "Una maledizione aleggia su qualcuno del gruppo.",
    "Un antico artefatto è più vicino di quanto pensi.",
    "Il prossimo tiro critico cambierà tutto.",
    "Attenzione ai mimic. Sono ovunque.",
    "Un drago ti osserva da lontano. Non è una metafora.",
    "La birra della prossima taverna sarà avvelenata. O forse no.",
    "Un alleato nasconde un segreto che potrebbe salvare… o distruggere il gruppo.",
    "Il DM ha qualcosa di terribile in serbo per te.",
    "Le prossime porte che aprirai riveleranno il tuo destino.",
    "Un fantasma del passato tornerà a farti visita.",
]


class Coin(commands.Cog):
    """Lancio della moneta e oracolo del destino."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["moneta", "flip"])
    async def coin(self, ctx):
        """Lancia una moneta — testa o croce!"""
        risultato = random.choice(["Testa", "Croce"])
        emoji = "👑" if risultato == "Testa" else "🛡️"

        embed = discord.Embed(
            title="🪙 Lancio della moneta",
            description=f"La moneta rotola sul tavolo...\n\n{emoji} **{risultato}!**",
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["destino", "profezia", "fortune"])
    async def oracle(self, ctx):
        """Consulta l'oracolo per una profezia misteriosa."""
        profezia = random.choice(PROFEZIE)

        embed = discord.Embed(
            title="🔮 L'Oracolo parla…",
            description=f"*«{profezia}»*",
            color=0x9B59B6,
        )
        embed.set_footer(text="Le profezie dell'Oracolo sono sempre... vagamente accurate.")
        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball"])
    async def destino8(self, ctx, *, domanda: str = None):
        """Fai una domanda al dado del destino (sì/no).
        Uso: !destino8 Troveremo il tesoro?"""
        risposte = [
            ("✅", "I dadi dicono: **Sì, certamente.**"),
            ("✅", "Le stelle sono favorevoli: **Sì.**"),
            ("✅", "L'oracolo annuisce: **Sicuramente.**"),
            ("✅", "I segni sono chiari: **Tutto indica di sì.**"),
            ("⚠️", "Difficile a dirsi… **chiedi di nuovo.**"),
            ("⚠️", "Le nebbie del futuro sono dense… **non è chiaro.**"),
            ("⚠️", "Il dado oscilla… **forse.**"),
            ("❌", "L'oracolo scuote la testa: **No.**"),
            ("❌", "I presagi sono infausti: **Non contarci.**"),
            ("❌", "Le stelle dicono: **Decisamente no.**"),
            ("❌", "Il dado del destino crolla: **Meglio di no.**"),
        ]

        emoji, risposta = random.choice(risposte)

        embed = discord.Embed(
            title="🎱 Dado del Destino",
            color=0x2C3E50,
        )
        if domanda:
            embed.add_field(name="Domanda", value=f"*{domanda}*", inline=False)
        embed.add_field(name="Risposta", value=f"{emoji} {risposta}", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Coin(bot))
