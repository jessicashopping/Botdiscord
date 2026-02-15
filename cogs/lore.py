import discord
from discord.ext import commands

class Lore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Dizionario contenente lore dei vari topic
        # Puoi aggiungere tutte le classi, razze, creature, incantesimi ecc.
        self.lore_data = {
            "barbaro": {
                "title": "Barbaro",
                "description": (
                    "I barbari sono potenti guerrieri alimentati dalle forze primordiali del multiverso. "
                    "Sono formidabili in combattimento corpo a corpo e sfruttano la loro furia per infliggere danni devastanti.\n\n"
                    "**Tratti principali:**\n- Forza e Costituzione\n- Resistenza ai danni contundenti, perforanti e taglienti durante la Furia\n- Vantaggio ai tiri di Forza\n- Nessuna concentrazione sugli incantesimi\n\n"
                    "**Equipaggiamento iniziale:**\n- Armi semplici e marziali\n- Armature leggere e medie e scudi"
                )
            },
            "bardo": {
                "title": "Bardo",
                "description": (
                    "I bardi usano parole, musica e danza per ispirare gli altri e incantare i nemici.\n\n"
                    "**Tratti principali:**\n- Carisma come abilità principale\n- Dadi di ispirazione bardica (d6 inizialmente)\n- Competenza in strumenti musicali e armi semplici\n- Capacità di lanciare incantesimi basati sul Carisma\n\n"
                    "**Equipaggiamento iniziale:**\n- Armatura leggera\n- Strumenti musicali a scelta\n- Pugnali e pack dell'intrattenitore"
                )
            },
            "elfo": {
                "title": "Elfo",
                "description": (
                    "Gli elfi sono creature agili e longeve, noti per la loro grazia e abilità con arco e magia.\n\n"
                    "**Tratti principali:**\n- Destrezza alta\n- Visione crepuscolare\n- Competenza in Percezione\n- Longevi e resistenti agli incantesimi di charme"
                )
            },
            # Aggiungi qui altri topic seguendo lo stesso schema
        }

    @commands.command()
    async def lore(self, ctx, *, topic: str = None):
        """
        Mostra informazioni lore su classi, razze o creature.
        Uso: !lore <topic>
        """
        if topic is None:
            available = ", ".join([k.replace("_", " ") for k in self.lore_data.keys()])
            await ctx.send(f"📚 Devi specificare un argomento. Ecco i topic disponibili:\n{available}")
            return

        key = topic.lower().replace(" ", "_")
        if key in self.lore_data:
            info = self.lore_data[key]
            embed = discord.Embed(
                title=info["title"],
                description=info["description"],
                color=0x3498db
            )
            embed.set_footer(text="D&D Bot • Scopri il mondo di D&D")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Mi dispiace, non ho informazioni su '{topic}'.")

    @lore.error
    async def lore_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Devi specificare un argomento. Esempio: `!lore barbaro`")

async def setup(bot):
    await bot.add_cog(Lore(bot))
