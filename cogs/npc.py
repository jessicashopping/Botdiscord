import discord
from discord.ext import commands
import random


# ── Dati NPC ─────────────────────────────────────────────
NOMI_MASCHILI = [
    "Arin", "Brom", "Cedric", "Doran", "Elric", "Fendrel", "Garrick", "Haldor",
    "Irin", "Jareth", "Kael", "Loric", "Merrick", "Nolan", "Orrin", "Perrin",
    "Quentin", "Roderick", "Sylas", "Theron", "Ulric", "Varric", "Wendell",
    "Xander", "Yorick", "Zarek", "Alden", "Bastian", "Cassius", "Darius",
    "Edric", "Fabian", "Galen", "Hadrian", "Isidore", "Jasper", "Kieran",
    "Lucian", "Magnus", "Nevin", "Percival", "Rafferty", "Soren", "Tobias",
    "Urian", "Valen", "Wyatt", "Zev", "Aldric", "Branwen",
]

NOMI_FEMMINILI = [
    "Aelina", "Brienne", "Celeste", "Dahlia", "Elara", "Freya", "Gwendolyn",
    "Helena", "Isolde", "Jasmine", "Kira", "Lyra", "Miriel", "Nadia", "Ophelia",
    "Petra", "Quinn", "Rosalind", "Seraphina", "Thalia", "Ursula", "Vivienne",
    "Wren", "Xena", "Ysolde", "Zara", "Arianna", "Beatrix", "Cassandra",
    "Delia", "Elowen", "Fiora", "Guinevere", "Hestia", "Ingrid", "Joanna",
    "Katrine", "Lilith", "Morgana", "Niamh", "Oriana", "Phaedra", "Rowena",
    "Sigrid", "Tessa", "Undine", "Vespera", "Winona", "Ylva", "Zelda",
]

NOMI_NEUTRI = [
    "Ash", "Briar", "Corin", "Darcy", "Emery", "Finch", "Gale", "Haven",
    "Indigo", "Juniper", "Kai", "Lark", "Moss", "Nyx", "Onyx", "Phoenix",
    "Raven", "Sage", "Tempest", "Umber", "Vale", "Wynn", "Zephyr", "Rowan",
]

GENERI = ["Maschio", "Femmina", "Non-binario"]

RAZZE = [
    "Umano", "Elfo", "Nano", "Halfling", "Mezzelfo", "Dragonide",
    "Tiefling", "Gnomo", "Orco", "Mezzorco", "Aasimar", "Genasi",
]

CLASSI = [
    "Guerriero", "Mago", "Ladro", "Chierico", "Paladino", "Ranger",
    "Stregone", "Bardo", "Druido", "Monaco", "Warlock", "Barbaro",
]

PROFESSIONI = [
    "Mercante", "Guardia", "Contadino", "Artigiano", "Alchimista", "Cacciatore",
    "Sacerdote", "Insegnante", "Nobile", "Bandito", "Erborista", "Esploratore",
    "Guaritore", "Viaggiatore", "Sarto", "Cavaliere", "Bibliotecario",
    "Fabbro", "Carpentiere", "Astrologo", "Mendicante", "Pescatore",
    "Cartografo", "Cacciatore di mostri", "Cantastorie", "Mineratore",
    "Erudito", "Saggio", "Allevatore", "Arciere", "Messaggero",
    "Mercenario", "Spadaccino", "Custode", "Banchiere", "Navigatore",
    "Artista", "Vigilante", "Locandiere", "Oste", "Incantatore errante",
]

HOBBY = [
    "colleziona monete antiche", "suona il liuto", "cucina piatti esotici",
    "dipinge paesaggi", "giardinaggio di erbe magiche", "alchimia sperimentale",
    "lettura di tomi proibiti", "racconta storie al falò", "caccia di cervi",
    "pesca nel fiume", "scacchi con i locali", "scrittura di ballate",
    "artigianato del cuoio", "viaggi verso rovine", "danza popolare",
    "poesia in elfico", "canto di ballate epiche", "meditazione al mattino",
    "raccolta di gemme", "osservare le stelle", "risolvere enigmi antichi",
    "calligrafia runifica", "modellare argilla", "creare pozioni",
    "pasticceria medievale", "scultura in legno", "raccolta di erbe medicinali",
    "colleziona mappe", "addestra animali", "studia lingue antiche",
]

TRATTI = [
    "arrogante", "gentile", "timido", "coraggioso", "ingenuo", "furbo",
    "sarcastico", "prudente", "impulsivo", "leale", "traditore", "curioso",
    "spiritoso", "paziente", "ambizioso", "scaltro", "studioso", "scontroso",
    "estroverso", "introverso", "ottimista", "pessimista", "sensibile",
    "distratto", "tenace", "avido", "giusto", "egoista", "misterioso",
    "affascinante", "cinico", "romantico", "lunatico", "pacifico",
    "vendicativo", "altruista", "giocoso", "riflessivo", "carismatico",
    "ribelle", "onesto", "stoico", "esuberante", "saggio", "pigro",
]

PAURE = [
    "ragni", "non morti", "altezze vertiginose", "l'oscurità più profonda",
    "annegare", "il fuoco incontrollato", "perdere il proprio potere",
    "la solitudine eterna", "il tradimento", "il fallimento pubblico",
    "i draghi", "i vampiri", "i serpenti", "le tempeste", "il sangue",
    "gli spettri", "perdere la memoria", "invecchiare", "la magia oscura",
    "essere dimenticato", "gli spazi chiusi", "le folle", "i demoni",
    "le maledizioni", "perdere le persone care",
]

OBIETTIVI = [
    "diventare ricco e rispettato", "trovare un artefatto leggendario",
    "salvare il regno dalla rovina", "scoprire un segreto antico",
    "vendicare un parente caduto", "diventare famoso in tutto il continente",
    "sconfiggere un nemico giurato", "trovare il vero amore",
    "ottenere un potere immenso", "proteggere un caro amico",
    "aprire una gilda di avventurieri", "diventare saggio tra i saggi",
    "viaggiare il mondo conosciuto", "guarire una maledizione",
    "scoprire la verità sulle proprie origini", "essere finalmente libero",
    "creare un incantesimo unico", "proteggere creature magiche",
    "trovare un mentore leggendario", "costruire una fortezza",
]

SEGRETI = [
    "è una spia per un regno straniero", "nasconde un tesoro sotto la sua casa",
    "ha un passato oscuro come assassino", "ha ucciso qualcuno per amore",
    "ha tradito un re in gioventù", "possiede un artefatto maledetto",
    "ha un legame segreto con un drago", "è inseguito da una gilda criminale",
    "nasconde un potere magico incontrollabile", "è stato imprigionato ingiustamente",
    "ha perso la memoria del proprio passato", "è un ladro redento",
    "è il custode di una profezia antica", "è maledetto da una strega",
    "ha un fratello gemello che nessuno conosce", "nasconde una doppia vita",
    "ha un debito con un demone", "ha vissuto in un altro piano di esistenza",
    "possiede conoscenze proibite", "ha un codice morale segreto",
    "è un discendente di una stirpe reale", "è stato tradito dal suo miglior amico",
]

CAPELLI = ["neri", "castani", "biondi", "rossi", "grigi", "bianchi", "argentei", "corvini", "ramati"]
OCCHI = ["azzurri", "verdi", "marroni", "neri", "grigi", "dorati", "viola", "ambrati"]
PELLE = ["chiara", "olivastra", "scura", "bronzea", "pallida", "ambrata", "rossastra"]
CORPORATURA = ["snella", "muscolosa", "robusta", "alta e slanciata", "bassa e tarchiata", "media", "longilinea"]
SEGNI = [
    "cicatrice sul volto", "occhio di vetro", "dente mancante",
    "bruciatura sul braccio", "tatuaggio tribale", "cicatrice sulle mani",
    "neo vistoso", "orecchio mozzato", "segno di artiglio sulla guancia",
    "voglia a forma di stella", "capelli con una ciocca bianca",
]
VESTITI = [
    "tunica di lino logora", "mantello di pelle scura", "armatura leggera borchiata",
    "vestito elegante di seta", "mantello strappato e rattoppato", "giacca di cuoio",
    "cotta di maglia", "camicia di seta con ricami", "tunica colorata con cappuccio",
    "abito da viaggio in lana", "tonaca monacale",
]
ACCESSORI = [
    "anello d'oro con sigillo", "collana con gemma incastonata", "bracciale runico",
    "orecchini d'argento", "cintura con fibbia decorata", "stivali alti",
    "cappello a tesa larga", "mantello con cappuccio", "amuleto misterioso",
    "borsello di cuoio", "fascia sulla fronte",
]
ARMI = [
    "spada lunga", "ascia bipenne", "pugnale elfico", "arco lungo", "bastone da viaggio",
    "martello da guerra", "lancia con pennacchio", "frusta", "bastone magico",
    "spadone a due mani", "balestra leggera", "mazza ferrata", "falcetto druidico",
]

FRASI_TIPICHE = [
    "«Non fidarti mai di un sorriso gratuito.»",
    "«La birra calda è un crimine, come la magia oscura.»",
    "«Ho visto cose che non crederesti… e alcune le ho causate io.»",
    "«Ogni cicatrice racconta una storia. Questa? Meglio non chiederlo.»",
    "«Il mondo è pieno di tesori. E di trappole.»",
    "«Un giorno sarò ricordato. O dimenticato. Entrambe le cose vanno bene.»",
    "«Se vuoi sapere la verità, paga il primo giro.»",
    "«La vita è un tiro di d20. Spera di non fare 1.»",
    "«Non sono un eroe. Ma i miei prezzi sono ragionevoli.»",
    "«Le stelle non mentono mai. Gli uomini, sempre.»",
    "«Ho un brutto presentimento… e di solito ho ragione.»",
    "«Preferisco i draghi alla gente. Almeno i draghi sono onesti.»",
]


class NPC(commands.Cog):
    """Generatore casuale di NPC per le tue sessioni."""

    def __init__(self, bot):
        self.bot = bot

    def _pick_name(self, genere: str) -> str:
        if genere == "Maschio":
            return random.choice(NOMI_MASCHILI)
        elif genere == "Femmina":
            return random.choice(NOMI_FEMMINILI)
        else:
            return random.choice(NOMI_NEUTRI)

    @commands.command()
    async def npc(self, ctx):
        """Genera un NPC casuale con identità, personalità, aspetto e frase tipica."""

        genere = random.choice(GENERI)
        nome = self._pick_name(genere)
        razza = random.choice(RAZZE)
        classe = random.choice(CLASSI)
        lavoro = random.choice(PROFESSIONI)
        hobby = random.choice(HOBBY)
        tratto = random.choice(TRATTI)
        paura = random.choice(PAURE)
        obiettivo = random.choice(OBIETTIVI)
        segreto = random.choice(SEGRETI)
        frase = random.choice(FRASI_TIPICHE)

        capelli = random.choice(CAPELLI)
        occhi = random.choice(OCCHI)
        pelle = random.choice(PELLE)
        corporatura = random.choice(CORPORATURA)
        segno = random.choice(SEGNI)
        vestito = random.choice(VESTITI)
        accessorio = random.choice(ACCESSORI)
        arma = random.choice(ARMI)

        eta = random.randint(18, 350) if razza in ("Elfo", "Mezzelfo") else random.randint(18, 80)

        embed = discord.Embed(
            title=f"🧙 {nome}",
            description=f"*{frase}*",
            color=discord.Color.dark_gold(),
        )

        embed.add_field(
            name="📜 Identità",
            value=(
                f"**Genere:** {genere}\n"
                f"**Razza:** {razza}\n"
                f"**Età:** {eta} anni\n"
                f"**Classe:** {classe}\n"
                f"**Professione:** {lavoro}"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧠 Personalità",
            value=(
                f"**Tratto:** {tratto}\n"
                f"**Hobby:** {hobby}\n"
                f"**Paura:** {paura}\n"
                f"**Obiettivo:** {obiettivo}"
            ),
            inline=True,
        )

        embed.add_field(name="\u200b", value="\u200b", inline=False)  # spacer

        embed.add_field(
            name="🎨 Aspetto",
            value=(
                f"**Capelli:** {capelli}\n"
                f"**Occhi:** {occhi}\n"
                f"**Pelle:** {pelle}\n"
                f"**Corporatura:** {corporatura}\n"
                f"**Segno distintivo:** {segno}"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚔️ Equipaggiamento",
            value=(
                f"**Vestiti:** {vestito}\n"
                f"**Accessorio:** {accessorio}\n"
                f"**Arma:** {arma}"
            ),
            inline=True,
        )

        embed.add_field(
            name="🤫 Segreto",
            value=f"||{segreto}||",
            inline=False,
        )

        embed.set_footer(text="Grimory Bot • Generatore NPC")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(NPC(bot))
