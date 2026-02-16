import discord
from discord.ext import commands
import random


BATTUTE = [
    "Perché il ladro porta sempre una corda? Perché non vuole restare legato alle regole!",
    "Sai perché il bardo non usa mai l'arco? Perché preferisce le note!",
    "Un orco entra in un bar: «Birra! E non fate storie… o vi riduco in brandelli!»",
    "Perché il druido non va mai in vacanza? Ogni volta che cambia forma, perde il bagaglio!",
    "Perché il chierico ama i dadi? Non importa il risultato, è sempre benedetto!",
    "Come chiami un goblin che sa cucinare? Uno chef di basso livello!",
    "Perché i draghi non giocano a dadi? Hanno paura del critico!",
    "Cosa fa un paladino quando cade in un pozzo? Contempla la propria fede!",
    "Sai perché i nani non raccontano barzellette? Fanno sempre scendere la morale!",
    "Come si chiama un mago che non sa lanciare incantesimi? Un disoccupato!",
    "Un bardo entra in una taverna: «Offro un giro!» — Il barista: «Di dadi o di birra?»",
    "Il barbaro al chierico: «Curami!» — Il chierico: «Non sono quel tipo di dottore.»",
    "Perché il ranger parla con gli alberi? Perché nessun altro lo ascolta.",
    "Cosa dice un mimo a un mago del silenzio? Nulla. Vanno molto d'accordo.",
    "Un tiefling entra in una chiesa. I chierici vanno nel panico. Lui voleva solo un tè.",
    "Un necromante organizza una festa. Nessuno viene. Allora li rievoca.",
    "Qual è l'incantesimo preferito di un contabile? Contare i morti.",
    "Perché il warlock è sempre stanco? Ha fatto un patto con il riposo corto.",
    "Il ladro al guerriero: «Ho rubato il cuore della principessa.» — «Letteralmente?» — «...Vuoi davvero saperlo?»",
    "Come si chiama un elfo che racconta bugie? Un fakelfo.",
    "Quanti barbari servono per cambiare una torcia? Nessuno. I barbari non cambiano. Spaccano.",
    "Perché il mago ha smesso di usare Palla di Fuoco? Perché il DM gli ha detto di calmarsi.",
    "Un halfling entra in un dungeon. Non lo vede nessuno. Come al solito.",
    "Il druido al barbaro: «Rispetta la natura!» — Il barbaro: «La natura rispetti ME.»",
    "Perché lo stregone è andato dallo psicologo? Metamagia: problemi di identità.",
    "Un golem entra in taverna e ordina una birra. Il barista: «Non serviamo la tua razza.» Il golem: «Tecnicamente non ho una razza.»",
    "Cosa fa un chierico quando il Wi-Fi non funziona? Prega per una connessione divina.",
    "Il bardo: «Ho sedotto il drago.» — Il DM: «...Tira Persuasione.» — *20 naturale* — Il DM piange.",
    "Perché il ranger non usa mai il GPS? Preferisce il suo senso della natura-vigazione.",
    "Un nano e un elfo entrano in una biblioteca. Il nano prende un libro sugli scavi. L'elfo lo giudica silenziosamente per 300 anni.",
]

INDOVINELLI = [
    {
        "domanda": "Non ho gambe, ma viaggio ovunque. Non ho bocca, ma racconto storie. Cosa sono?",
        "risposta": "Un libro",
    },
    {
        "domanda": "Più mi togli, più divento grande. Cosa sono?",
        "risposta": "Un buco",
    },
    {
        "domanda": "Ho le chiavi ma non apro porte. Cosa sono?",
        "risposta": "Un pianoforte (o un liuto, se sei un bardo)",
    },
    {
        "domanda": "Cammino senza piedi, parlo senza bocca, non sono nulla ma posso uccidere. Cosa sono?",
        "risposta": "Il vento",
    },
    {
        "domanda": "Tutti mi possono aprire, ma nessuno mi può chiudere. Cosa sono?",
        "risposta": "Un uovo",
    },
    {
        "domanda": "Più sono scuro, più sono leggero. Cosa sono?",
        "risposta": "L'ombra",
    },
    {
        "domanda": "Ho una testa e una coda, ma non ho un corpo. Cosa sono?",
        "risposta": "Una moneta",
    },
    {
        "domanda": "Vivo senza respiro, freddo come la morte, mai assetato, mai bevo. Cosa sono?",
        "risposta": "Un pesce",
    },
]


class Jokes(commands.Cog):
    """Battute, freddure e indovinelli a tema D&D."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["battuta", "freddura"])
    async def joke(self, ctx):
        """Invia una battuta casuale a tema D&D."""
        joke = random.choice(BATTUTE)
        embed = discord.Embed(
            title="🤣 Freddura del tavolo",
            description=joke,
            color=0x9B59B6,
        )
        embed.set_footer(text="Grimory Bot • Divertiti al tavolo!")
        await ctx.send(embed=embed)

    @commands.command(aliases=["enigma"])
    async def riddle(self, ctx):
        """Propone un indovinello medievale. La risposta è nascosta sotto spoiler."""
        riddle = random.choice(INDOVINELLI)
        embed = discord.Embed(
            title="🧩 Indovinello dell'Oracolo",
            description=riddle["domanda"],
            color=0xE67E22,
        )
        embed.add_field(
            name="Risposta",
            value=f"||{riddle['risposta']}||",
            inline=False,
        )
        embed.set_footer(text="Clicca sullo spoiler per rivelare la risposta!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Jokes(bot))
