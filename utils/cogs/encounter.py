import discord
from discord.ext import commands
import random


ENCOUNTERS = {
    "facile": [
        {
            "nemici": "3 Goblin",
            "ambiente": "Strada nel bosco",
            "descrizione": "Tre goblin saltano fuori dai cespugli con lance arrugginite, ringhiando minacce.",
            "bottino": "12 rame, un pugnale scheggiato, una mappa grossolana",
        },
        {
            "nemici": "2 Lupi",
            "ambiente": "Radura nella foresta",
            "descrizione": "Due lupi vi circondano con occhi affamati. Uno ringhia, l'altro si avvicina basso.",
            "bottino": "Pellicce di lupo (valore: 5 argenti)",
        },
        {
            "nemici": "4 Scheletri",
            "ambiente": "Cripta abbandonata",
            "descrizione": "Ossa scricchiolano mentre quattro scheletri si alzano dalle bare di pietra.",
            "bottino": "8 rame, un anello d'osso, una spada arrugginita",
        },
        {
            "nemici": "1 Orso Bruno",
            "ambiente": "Sentiero di montagna",
            "descrizione": "Un orso si erge sulle zampe posteriori. Sta proteggendo i suoi cuccioli.",
            "bottino": "Nessuno (è un orso, non un mostro — ma potete raccogliere bacche qui vicino)",
        },
        {
            "nemici": "6 Coboldi",
            "ambiente": "Tunnel minerario",
            "descrizione": "Sei coboldi vi tendono un'imboscata con trappole improvvisate e fionde.",
            "bottino": "18 rame, un sacco di pietre lucide, una torcia",
        },
    ],
    "medio": [
        {
            "nemici": "1 Orco + 3 Goblin",
            "ambiente": "Accampamento nella palude",
            "descrizione": "Un orco siede accanto a un falò. Tre goblin fanno la guardia. Hanno un prigioniero.",
            "bottino": "2 argenti, ascia da guerra, pozione di guarigione",
        },
        {
            "nemici": "1 Mimic",
            "ambiente": "Stanza del tesoro",
            "descrizione": "Un baule ornato giace al centro della stanza. Sembra… troppo invitante.",
            "bottino": "35 monete d'oro (se sopravvivete)",
        },
        {
            "nemici": "2 Gargoyle",
            "ambiente": "Torre in rovina",
            "descrizione": "Le statue ai lati della porta si muovono. Non erano statue.",
            "bottino": "Nessun tesoro materiale, ma la strada è ora libera",
        },
        {
            "nemici": "1 Troll",
            "ambiente": "Ponte di pietra",
            "descrizione": "Un troll emerge da sotto il ponte. «Pedaggio!» grugnisce. «O vi mangio.»",
            "bottino": "4 argenti, un osso massiccio usabile come mazza, razione di carne... dubbia",
        },
        {
            "nemici": "5 Banditi + 1 Capitano bandito",
            "ambiente": "Strada maestra",
            "descrizione": "Un gruppo di banditi vi blocca la strada. Il capitano sorride: «Borse o sangue.»",
            "bottino": "15 argenti, arco corto, una lettera sigillata misteriosa",
        },
    ],
    "difficile": [
        {
            "nemici": "1 Giovane Drago Rosso",
            "ambiente": "Caverna vulcanica",
            "descrizione": "Il calore è insopportabile. Un drago rosso giovane vi fissa dai suoi cumuli d'oro.",
            "bottino": "200 monete d'oro, gemme preziose, un'arma magica +1",
        },
        {
            "nemici": "1 Vampiro Iniziato",
            "ambiente": "Cripta sotto la cattedrale",
            "descrizione": "Una figura pallida emerge dall'ombra. I suoi occhi rossi brillano nella penombra.",
            "bottino": "Medaglione d'argento, 50 monete d'oro, una pergamena arcana",
        },
        {
            "nemici": "3 Elementali del Fuoco",
            "ambiente": "Portale planare instabile",
            "descrizione": "Il portale pulsa. Tre figure di fuoco puro ne emergono, incendiando tutto intorno.",
            "bottino": "Frammenti elementali (componente rara), 30 monete d'oro",
        },
        {
            "nemici": "1 Beholder Indebolito",
            "ambiente": "Covo sotterraneo",
            "descrizione": "Dieci occhi vi fissano dall'oscurità. Un solo grande occhio si apre lentamente.",
            "bottino": "Occhio del beholder (componente leggendaria), 100 monete d'oro, un tomo arcano",
        },
    ],
    "mortale": [
        {
            "nemici": "1 Lich",
            "ambiente": "Fortezza dimensionale",
            "descrizione": "L'aria gela. Un essere scheletrico in vesti regali fluttua davanti a voi. «Mortali…»",
            "bottino": "???  (prima dovete sopravvivere)",
        },
        {
            "nemici": "1 Drago Rosso Antico",
            "ambiente": "Montagna di cenere",
            "descrizione": "Il cielo diventa rosso. La montagna trema. Una sagoma immensa si staglia contro il sole.",
            "bottino": "Tesoro leggendario… se il mondo esiste ancora dopo lo scontro.",
        },
    ],
}

DIFFICOLTA_COLORI = {
    "facile": 0x2ECC71,
    "medio": 0xF39C12,
    "difficile": 0xE74C3C,
    "mortale": 0x8B0000,
}

DIFFICOLTA_EMOJI = {
    "facile": "🟢",
    "medio": "🟡",
    "difficile": "🔴",
    "mortale": "💀",
}


class Encounter(commands.Cog):
    """Generatore casuale di incontri."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["incontro", "combat", "combattimento"])
    async def encounter(self, ctx, difficolta: str = None):
        """Genera un incontro casuale.
        Uso: !encounter [facile|medio|difficile|mortale]
        Senza argomento: difficoltà casuale."""

        if difficolta is None:
            difficolta = random.choice(["facile", "medio", "difficile"])
        difficolta = difficolta.lower().strip()

        if difficolta not in ENCOUNTERS:
            validi = ", ".join(f"`{k}`" for k in ENCOUNTERS)
            await ctx.send(f"⚠️ Difficoltà non valida. Opzioni: {validi}")
            return

        enc = random.choice(ENCOUNTERS[difficolta])
        emoji = DIFFICOLTA_EMOJI[difficolta]
        colore = DIFFICOLTA_COLORI[difficolta]

        embed = discord.Embed(
            title=f"⚔️ Incontro — {emoji} {difficolta.capitalize()}",
            description=enc["descrizione"],
            color=colore,
        )
        embed.add_field(name="👹 Nemici", value=enc["nemici"], inline=True)
        embed.add_field(name="📍 Ambiente", value=enc["ambiente"], inline=True)
        embed.add_field(name="💰 Bottino potenziale", value=enc["bottino"], inline=False)
        embed.set_footer(text="Grimory Bot • Generatore Incontri · Tirate iniziativa!")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Encounter(bot))
