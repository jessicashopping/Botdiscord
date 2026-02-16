import discord
from discord.ext import commands
import random


# ── Generatore nomi taverna ──────────────────────────────
PREFISSI = [
    "Il Drago", "L'Orso", "Il Cinghiale", "La Fenice", "Il Corvo",
    "Il Cervo", "La Sirena", "Il Grifone", "Il Lupo", "L'Unicorno",
    "Il Goblin", "La Chimera", "Il Falco", "La Civetta", "Il Serpente",
    "Lo Spettro", "Il Basilisco", "La Volpe", "Il Toro", "La Lince",
]

SUFFISSI = [
    "Ubriaco", "Danzante", "Dorato", "Nero", "Rosso", "Urlante",
    "Addormentato", "Ridacchiante", "Errante", "Infuocato", "D'Argento",
    "Solitario", "Maledetto", "Luminoso", "Rumoroso", "Misterioso",
    "Affamato", "Felice", "Storico", "Leggendario",
]

PIATTI = [
    "Stufato di cinghiale con patate", "Pollo arrosto alle erbe",
    "Zuppa di funghi del sottosuolo", "Costolette di montone alla birra",
    "Pane nero con formaggio stagionato", "Pesce di fiume alla griglia",
    "Salsicce speziate con crauti", "Torta di mele con miele",
    "Porridge con frutta secca", "Cosciotto di cervo al rosmarino",
    "Formaggio fuso su pane tostato", "Spezzatino di coniglio",
    "Uova di drago sode (probabilmente di gallina)", "Insalata di radici selvatiche",
    "Pasticcio di carne in crosta",
]

BEVANDE = [
    "Birra scura nanica — 4 rame", "Idromele dorato — 8 rame",
    "Vino rosso di Baldur's Gate — 1 argento", "Sidro di mele elfiche — 6 rame",
    "Acqua di fonte (gratuita, ma il barista ti giudica)",
    "Grappa del dragone — 2 argenti (forte!)", "Tè alle erbe del druido — 3 rame",
    "Birra chiara halfling — 5 rame", "Liquore infernale — 3 argenti (a tuo rischio)",
    "Latte caldo con miele — 2 rame",
]

VOCI_LOCANDA = [
    "Si dice che nelle miniere a nord abbiano trovato una vena d'oro… o qualcosa di peggio.",
    "Un mercante è scomparso sulla strada del bosco tre notti fa. Nessuno osa andare a cercarlo.",
    "Il barone sta reclutando mercenari. Nessuno sa per cosa.",
    "Una strega vive nella palude a est. Alcuni dicono che curi i malati… altri che li mangi.",
    "Hanno visto luci strane nel cimitero dopo la mezzanotte.",
    "Un drago è stato avvistato a ovest. Probabilmente solo un wyvern… probabilmente.",
    "La gilda dei ladri ha messo una taglia su qualcuno. Chi? Dipende da chi chiedi.",
    "Un bardo racconta di una torre abbandonata piena di tesori. L'ultimo gruppo non è tornato.",
    "Il fabbro giura di aver forgiato una spada che brilla al buio. Vuole 200 monete d'oro.",
    "Le guardie sono nervose. Qualcosa li ha spaventati durante la ronda notturna.",
    "Un nano ubriaco dice di conoscere l'ingresso segreto di un dungeon antico.",
    "Il tempio cerca volontari per 'una missione di routine'. Nessuno ci crede.",
    "Si mormora che il sindaco abbia un patto con i banditi della foresta.",
    "Un circo itinerante arriva domani. L'ultimo circo che è passato qui... beh, è una lunga storia.",
]

BARISTI = [
    ("Gorm", "nano burbero con una benda sull'occhio", "«Ordina, paga, e non rompere i bicchieri.»"),
    ("Tilda", "umana robusta con un mestolo sempre in mano", "«La zuppa è gratis col secondo boccale. Terzo boccale, ti porto al letto.»"),
    ("Silvius", "mezzelfo sorridente con un grembiule macchiato", "«Ogni cliente è un amico! …finché paga.»"),
    ("Branka", "nana con trecce rosse e un martello sotto il bancone", "«L'ultima rissa è costata tre tavoli. Non fatene un'altra.»"),
    ("Pip", "halfling allegro che deve salire su uno sgabello", "«Il miglior idromele del continente! Lo faccio io, con amore.»"),
    ("Korgath", "mezzorco tatuato che pulisce un boccale", "«Birra. O fuori.»"),
    ("Elara", "elfa anziana con occhi gentili", "«Siediti, caro. Raccontami le tue avventure.»"),
]

ATMOSFERE = [
    "Musica di liuto riempie la sala, mentre una coppia danza vicino al camino.",
    "Un gruppo di nani canta a squarciagola canzoni di miniera.",
    "Il locale è quasi vuoto. Solo un gatto dorme su una sedia nell'angolo.",
    "Un bardo racconta una storia epica a un pubblico rapito.",
    "Due mercenari discutono animatamente su chi ha ucciso più goblin.",
    "L'aria è densa di fumo di pipa e profumo di stufato.",
    "Un giocatore di dadi sta vincendo troppo. Qualcuno lo guarda male.",
    "Una cameriera serve birra a velocità impressionante.",
    "Nell'angolo, una figura incappucciata osserva tutto in silenzio.",
    "Una partita a carte sta degenerando. Qualcuno ha barato.",
]


class Taverna(commands.Cog):
    """Generatore casuale di taverne."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["locanda", "inn"])
    async def taverna(self, ctx):
        """Genera una taverna casuale con nome, barista, menù e dicerie."""

        nome = f"{random.choice(PREFISSI)} {random.choice(SUFFISSI)}"
        barista_nome, barista_desc, barista_frase = random.choice(BARISTI)
        atmosfera = random.choice(ATMOSFERE)

        piatti = random.sample(PIATTI, k=3)
        bevande = random.sample(BEVANDE, k=3)
        voce = random.choice(VOCI_LOCANDA)

        embed = discord.Embed(
            title=f"🍺 {nome}",
            description=f"*{atmosfera}*",
            color=0xCD853F,
        )

        embed.add_field(
            name=f"🧑‍🍳 Barista — {barista_nome}",
            value=f"*{barista_desc}*\n{barista_frase}",
            inline=False,
        )

        menu = "\n".join(f"• {p}" for p in piatti)
        embed.add_field(name="🍖 Piatti del giorno", value=menu, inline=True)

        bev = "\n".join(f"• {b}" for b in bevande)
        embed.add_field(name="🍺 Bevande", value=bev, inline=True)

        embed.add_field(
            name="🗣️ Voce che gira…",
            value=f"*«{voce}»*",
            inline=False,
        )

        embed.set_footer(text="Grimory Bot • Generatore Taverne")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Taverna(bot))
