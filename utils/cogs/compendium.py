import discord
from discord.ext import commands

# ── Dati delle classi ────────────────────────────────────
# Ogni classe è un dizionario con campi standard.
# Per aggiungerne una nuova basta copiare il template.

CLASSI = {
    "barbaro": {
        "titolo": "Barbaro",
        "colore": 0xAA0000,
        "descrizione": (
            "I barbari sono potenti guerrieri alimentati dalle forze primordiali del multiverso "
            "che si manifestano come rabbia. Formidabili in corpo a corpo, sfruttano la loro "
            "furia per infliggere danni devastanti."
        ),
        "tratti": (
            "• Abilità primaria: Forza\n"
            "• Dado vita: d12\n"
            "• Tiri salvezza: Forza e Costituzione\n"
            "• Competenze: 2 tra Gestione Animali, Atletica, Intimidazione, Natura, Percezione, Sopravvivenza\n"
            "• Armi: Semplici e marziali\n"
            "• Armatura: Leggera, media + scudi\n"
            "• Equip. A) Ascia grande, 4 asce da lancio, Kit esploratore, 15 GP\n"
            "• Equip. B) 75 GP"
        ),
        "abilita_chiave": {
            "🔥 Furia": (
                "Azione bonus — resistenza a danni contundenti/perforanti/da taglio, bonus al danno "
                "con Forza, vantaggio a prove e TS di Forza. Non puoi lanciare o concentrare incantesimi. "
                "Dura fino a 10 minuti."
            ),
            "🛡️ Difesa senza armatura": (
                "CA base = 10 + mod. Destrezza + mod. Costituzione. Puoi usare uno scudo."
            ),
            "⚔️ Padronanza delle armi": (
                "Puoi usare le proprietà di maestria di 2 armi corpo a corpo. "
                "Cambiabili dopo ogni riposo lungo."
            ),
        },
        "incantesimi": "I barbari **non hanno incantesimi**; si concentrano sul combattimento e sulla Furia.",
        "background": "Selvaggio, Guerriero tribale, Avventuriero di confini.",
    },
    "bardo": {
        "titolo": "Bardo",
        "colore": 0x5500AA,
        "descrizione": (
            "I bardi sono maestri dell'ispirazione attraverso parole, musica o danza. "
            "Supportano gli alleati, incantano nemici e manipolano il campo di battaglia."
        ),
        "tratti": (
            "• Abilità primaria: Carisma\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Destrezza e Carisma\n"
            "• Competenze: 3 abilità a scelta\n"
            "• Armi: Semplici\n"
            "• Strumenti: 3 strumenti musicali a scelta\n"
            "• Armatura: Leggera\n"
            "• Equip. A) Cuoio, 2 pugnali, strumento musicale, Kit intrattenitore, 19 GP\n"
            "• Equip. B) 90 GP"
        ),
        "abilita_chiave": {
            "🎵 Ispirazione Bardica": (
                "Azione bonus — concedi un d6 a un alleato entro 60 piedi (usabile entro 1 h). "
                "Usi = mod. Carisma; recuperati con riposo lungo. "
                "Il dado cresce: d8 (lv 5), d10 (lv 10), d12 (lv 15)."
            ),
        },
        "incantesimi": (
            "2 trucchetti + 4 incantesimi preparati (lv 1). Carisma come abilità di lancio. "
            "Slot recuperati con riposo lungo. Strumenti musicali come focus."
        ),
        "background": "Intrattenitore, Artista itinerante, Cantore di leggende.",
    },
    "chierico": {
        "titolo": "Chierico",
        "colore": 0xF0E68C,
        "descrizione": (
            "I chierici sono intermediari tra il mondo mortale e i piani divini. "
            "Canalizzano il potere della loro divinità per curare, proteggere e punire."
        ),
        "tratti": (
            "• Abilità primaria: Saggezza\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Saggezza e Carisma\n"
            "• Competenze: 2 tra Storia, Intuizione, Medicina, Persuasione, Religione\n"
            "• Armi: Semplici\n"
            "• Armatura: Leggera, media + scudi\n"
            "• Equip. A) Mazza, cotta di maglia, scudo, simbolo sacro, Kit sacerdotale, 7 GP\n"
            "• Equip. B) 110 GP"
        ),
        "abilita_chiave": {
            "✝️ Canalizzare Divinità": (
                "Puoi incanalare energia divina per produrre effetti speciali. "
                "Usi recuperati con riposo corto o lungo."
            ),
            "✨ Scacciare non-morti": (
                "Ogni non morto entro 30 piedi deve superare un TS Saggezza o essere scacciato per 1 minuto."
            ),
        },
        "incantesimi": (
            "3 trucchetti + incantesimi preparati dalla lista del Chierico. "
            "Saggezza come abilità di lancio. Slot recuperati con riposo lungo."
        ),
        "background": "Accolito, Eremita, Sacerdote di frontiera.",
    },
    "druido": {
        "titolo": "Druido",
        "colore": 0x228B22,
        "descrizione": (
            "I druidi sono custodi della natura; attingono alle forze elementali "
            "e alla magia del mondo naturale per proteggere l'equilibrio."
        ),
        "tratti": (
            "• Abilità primaria: Saggezza\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Intelligenza e Saggezza\n"
            "• Competenze: 2 tra Arcano, Gestione Animali, Intuizione, Medicina, Natura, Percezione, Religione, Sopravvivenza\n"
            "• Armi: Semplici\n"
            "• Armatura: Leggera + scudi (no metallo)\n"
            "• Equip. A) Scudo, falcetto, focus druidico, Kit esploratore, 9 GP\n"
            "• Equip. B) 50 GP"
        ),
        "abilita_chiave": {
            "🐾 Forma Selvatica": (
                "Puoi trasformarti in una bestia che hai visto. Durata e CR massimo aumentano con il livello."
            ),
            "🌿 Linguaggio Druidico": (
                "Conosci il linguaggio segreto dei druidi. Puoi lasciare messaggi nascosti nella natura."
            ),
        },
        "incantesimi": (
            "2 trucchetti + incantesimi preparati. Saggezza come abilità di lancio. "
            "Puoi usare un focus druidico."
        ),
        "background": "Eremita, Straniero, Custode della foresta.",
    },
    "guerriero": {
        "titolo": "Guerriero",
        "colore": 0x8B0000,
        "descrizione": (
            "I guerrieri sono maestri del combattimento marziale. "
            "Esperti con ogni tipo di arma e armatura, eccellono in qualsiasi campo di battaglia."
        ),
        "tratti": (
            "• Abilità primaria: Forza o Destrezza\n"
            "• Dado vita: d10\n"
            "• Tiri salvezza: Forza e Costituzione\n"
            "• Competenze: 2 tra Acrobazia, Atletica, Gestione Animali, Intimidazione, Intuizione, Percezione, Sopravvivenza, Storia\n"
            "• Armi: Semplici e marziali\n"
            "• Armatura: Tutte + scudi\n"
            "• Equip. A) Cotta di maglia, scudo, spada lunga, 8 balestre e 20 dardi, Kit avventuriero, 11 GP\n"
            "• Equip. B) 175 GP"
        ),
        "abilita_chiave": {
            "⚔️ Stile di Combattimento": (
                "Scegli uno stile: Difesa (+1 CA), Duellare (+2 danno), Arma grande (rilancia 1/2 danno), "
                "Tiro con l'arco (+2 al tiro), ecc."
            ),
            "💪 Recupero Energetico": (
                "Una volta per riposo corto, recuperi PF pari a 1d10 + livello da guerriero."
            ),
            "🗡️ Azione Impetuosa": (
                "Dal lv 2: una volta per riposo corto, puoi compiere un'azione extra nel tuo turno."
            ),
        },
        "incantesimi": "I guerrieri base **non hanno incantesimi** (il sotto-classe Cavaliere Mistico li ottiene al lv 3).",
        "background": "Soldato, Mercenario, Cavaliere errante.",
    },
    "ladro": {
        "titolo": "Ladro",
        "colore": 0x2F4F4F,
        "descrizione": (
            "I ladri si affidano ad astuzia, furtività e abilità per superare ogni ostacolo. "
            "Colpiscono dove fa più male e scompaiono prima della reazione."
        ),
        "tratti": (
            "• Abilità primaria: Destrezza\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Destrezza e Intelligenza\n"
            "• Competenze: 4 tra Acrobazia, Atletica, Furtività, Indagare, Inganno, Intimidazione, Intuizione, Percezione, Persuasione, Rapidità di Mano\n"
            "• Armi: Semplici + balestre a mano, spade corte, stocchi\n"
            "• Armatura: Leggera\n"
            "• Equip. A) Cuoio, 2 pugnali, arnesi da scasso, Kit esploratore, 8 GP\n"
            "• Equip. B) 110 GP"
        ),
        "abilita_chiave": {
            "🗡️ Attacco Furtivo": (
                "Una volta per turno, +1d6 danni (aumenta con il livello) quando hai vantaggio "
                "o un alleato è entro 5 piedi dal bersaglio."
            ),
            "🗣️ Gergo dei Ladri": (
                "Conosci un linguaggio segreto dei criminali. Puoi lasciare messaggi nascosti."
            ),
            "🏃 Azione Scaltra": (
                "Dal lv 2: azione bonus per Scattare, Disimpegnarti o Nasconderti."
            ),
        },
        "incantesimi": "I ladri base **non hanno incantesimi** (il sotto-classe Mistificatore Arcano li ottiene al lv 3).",
        "background": "Criminale, Spia, Orfano di strada.",
    },
    "mago": {
        "titolo": "Mago",
        "colore": 0x4169E1,
        "descrizione": (
            "I maghi sono studiosi delle arti arcane. Attraverso studio e pratica, "
            "padroneggiano gli incantesimi più potenti del multiverso."
        ),
        "tratti": (
            "• Abilità primaria: Intelligenza\n"
            "• Dado vita: d6\n"
            "• Tiri salvezza: Intelligenza e Saggezza\n"
            "• Competenze: 2 tra Arcano, Indagare, Intuizione, Medicina, Religione, Storia\n"
            "• Armi: Semplici\n"
            "• Armatura: Nessuna\n"
            "• Equip. A) 2 pugnali, focus arcano, libro degli incantesimi, Kit studioso, 5 GP\n"
            "• Equip. B) 55 GP"
        ),
        "abilita_chiave": {
            "📖 Libro degli Incantesimi": (
                "Contiene tutti gli incantesimi che conosci. Puoi copiare nuovi incantesimi trovati "
                "durante le avventure (2 ore + 50 GP per livello di incantesimo)."
            ),
            "🔮 Recupero Arcano": (
                "Una volta al giorno con un riposo corto, recuperi slot pari a metà del tuo livello da mago (arrotondato per eccesso)."
            ),
        },
        "incantesimi": (
            "3 trucchetti + libro con 6 incantesimi di lv 1. Intelligenza come abilità di lancio. "
            "Prepari un numero di incantesimi pari a mod. Intelligenza + livello da mago (minimo 1)."
        ),
        "background": "Saggio, Studioso, Apprendista arcano.",
    },
    "monaco": {
        "titolo": "Monaco",
        "colore": 0xDAA520,
        "descrizione": (
            "I monaci canalizzano l'energia interiore — il Ki — "
            "per compiere imprese fisiche straordinarie e colpi devastanti."
        ),
        "tratti": (
            "• Abilità primaria: Destrezza e Saggezza\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Forza e Destrezza\n"
            "• Competenze: 2 tra Acrobazia, Atletica, Furtività, Intuizione, Religione, Storia\n"
            "• Armi: Semplici + spade corte\n"
            "• Armatura: Nessuna\n"
            "• Equip. A) Spada corta, Kit esploratore, 11 GP\n"
            "• Equip. B) 50 GP"
        ),
        "abilita_chiave": {
            "☯️ Ki": (
                "Punti Ki = livello da monaco. Usi: Raffica di colpi (2 colpi senz'armi bonus), "
                "Difesa Paziente (+2 CA per un turno), Passo del Vento (Scattare/Disimpegnarti come bonus)."
            ),
            "🛡️ Difesa senza armatura": (
                "CA base = 10 + mod. Destrezza + mod. Saggezza."
            ),
            "🏃 Movimento senza armatura": (
                "La tua velocità aumenta di +10 piedi al lv 2, e continua a crescere."
            ),
        },
        "incantesimi": "I monaci base **non hanno incantesimi** (il sotto-classe Via dei Quattro Elementi li ottiene).",
        "background": "Eremita, Accolito, Vagabondo.",
    },
    "paladino": {
        "titolo": "Paladino",
        "colore": 0xFFD700,
        "descrizione": (
            "I paladini sono guerrieri sacri vincolati da un giuramento. "
            "Uniscono la forza delle armi con il potere divino."
        ),
        "tratti": (
            "• Abilità primaria: Forza e Carisma\n"
            "• Dado vita: d10\n"
            "• Tiri salvezza: Saggezza e Carisma\n"
            "• Competenze: 2 tra Atletica, Intimidazione, Intuizione, Medicina, Persuasione, Religione\n"
            "• Armi: Semplici e marziali\n"
            "• Armatura: Tutte + scudi\n"
            "• Equip. A) Cotta di maglia, scudo, spada lunga, 6 giavellotti, Kit sacerdotale, simbolo sacro, 9 GP\n"
            "• Equip. B) 150 GP"
        ),
        "abilita_chiave": {
            "✋ Imposizione delle mani": (
                "Guarisci un totale di PF pari a livello × 5 al giorno. "
                "Puoi anche spendere 5 punti per curare una malattia o un veleno."
            ),
            "⚔️ Punizione Divina": (
                "Quando colpisci, puoi spendere uno slot per infliggere +2d8 danni radianti "
                "(+1d8 per ogni slot superiore al 1°, +1d8 contro non morti/immondi)."
            ),
        },
        "incantesimi": (
            "Incantesimi dal lv 2. Carisma come abilità di lancio. "
            "Prepari incantesimi pari a mod. Carisma + metà livello da paladino."
        ),
        "background": "Cavaliere, Nobile, Accolito.",
    },
    "ranger": {
        "titolo": "Ranger",
        "colore": 0x006400,
        "descrizione": (
            "I ranger sono guerrieri della natura, abili cacciatori ed esploratori. "
            "Combinano abilità marziali e magia naturale per proteggere i confini della civiltà."
        ),
        "tratti": (
            "• Abilità primaria: Destrezza e Saggezza\n"
            "• Dado vita: d10\n"
            "• Tiri salvezza: Forza e Destrezza\n"
            "• Competenze: 3 tra Atletica, Furtività, Gestione Animali, Indagare, Intuizione, Natura, Percezione, Sopravvivenza\n"
            "• Armi: Semplici e marziali\n"
            "• Armatura: Leggera e media + scudi\n"
            "• Equip. A) Cuoio borchiato, 2 spade corte, arco lungo e faretra con 20 frecce, Kit esploratore, 7 GP\n"
            "• Equip. B) 150 GP"
        ),
        "abilita_chiave": {
            "🎯 Nemico Prescelto": (
                "Scegli un tipo di nemico: hai vantaggio alle prove per seguirne le tracce "
                "e bonus alle prove di Intelligenza per ricordare informazioni su di esso."
            ),
            "🌲 Esploratore Nato": (
                "Scegli un terreno prediletto. Il tuo gruppo non può perdersi, "
                "trova il doppio del cibo e ha vantaggio alle prove di Iniziativa."
            ),
        },
        "incantesimi": (
            "Incantesimi dal lv 2. Saggezza come abilità di lancio. "
            "Prepari un numero limitato di incantesimi naturali."
        ),
        "background": "Straniero, Cacciatore, Guardia di frontiera.",
    },
    "stregone": {
        "titolo": "Stregone",
        "colore": 0xFF4500,
        "descrizione": (
            "Gli stregoni possiedono magia innata ereditata dal sangue, "
            "da un evento cosmico o da un patto ancestrale. Non studiano: la magia è nel loro essere."
        ),
        "tratti": (
            "• Abilità primaria: Carisma\n"
            "• Dado vita: d6\n"
            "• Tiri salvezza: Costituzione e Carisma\n"
            "• Competenze: 2 tra Arcano, Inganno, Intimidazione, Intuizione, Persuasione, Religione\n"
            "• Armi: Semplici\n"
            "• Armatura: Nessuna\n"
            "• Equip. A) 2 pugnali, focus arcano, Kit avventuriero, 28 GP\n"
            "• Equip. B) 50 GP"
        ),
        "abilita_chiave": {
            "🌀 Punti Stregoneria": (
                "Punti = livello da stregone. Puoi convertirli in slot o spenderli per Metamagia."
            ),
            "✨ Metamagia": (
                "Dal lv 2: modifica i tuoi incantesimi — Incantesimo Potenziato, Sottile, Esteso, ecc."
            ),
        },
        "incantesimi": (
            "4 trucchetti + 2 incantesimi conosciuti (lv 1). Carisma come abilità di lancio. "
            "Incantesimi conosciuti (non preparati): impari nuovi incantesimi a ogni livello."
        ),
        "background": "Eremita, Nobile decaduto, Selvaggio.",
    },
    "warlock": {
        "titolo": "Warlock",
        "colore": 0x800080,
        "descrizione": (
            "I warlock ottengono magia da un patto con un'entità superiore: "
            "un signore fatato, un immondo o un Grande Antico. Il potere ha sempre un prezzo."
        ),
        "tratti": (
            "• Abilità primaria: Carisma\n"
            "• Dado vita: d8\n"
            "• Tiri salvezza: Saggezza e Carisma\n"
            "• Competenze: 2 tra Arcano, Inganno, Intimidazione, Indagare, Natura, Religione, Storia\n"
            "• Armi: Semplici\n"
            "• Armatura: Leggera\n"
            "• Equip. A) Cuoio, 2 pugnali, focus arcano, Kit studioso, 15 GP\n"
            "• Equip. B) 100 GP"
        ),
        "abilita_chiave": {
            "📜 Magia del Patto": (
                "Pochi slot ma si recuperano con riposo corto. "
                "Gli slot sono sempre al livello massimo disponibile."
            ),
            "🎁 Dono del Patrono": (
                "Al lv 1 ricevi un privilegio unico dal tuo patrono. "
                "Invocazioni mistiche (lv 2) aggiungono poteri extra."
            ),
        },
        "incantesimi": (
            "2 trucchetti + 2 incantesimi conosciuti (lv 1). Carisma come abilità di lancio. "
            "Slot recuperati con riposo corto."
        ),
        "background": "Ciarlatano, Eremita, Haunted one.",
    },
}


class Compendium(commands.Cog):
    """Compendio delle classi di D&D 5e."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["classe", "class"])
    async def classinfo(self, ctx, *, classe: str = None):
        """Mostra la scheda completa di una classe D&D.
        Uso: !classinfo <nome classe>
        Esempio: !classinfo guerriero"""

        if classe is None:
            nomi = ", ".join(f"**{v['titolo']}**" for v in CLASSI.values())
            await ctx.send(f"📚 Classi disponibili: {nomi}\nUsa `!classinfo <classe>` per i dettagli.")
            return

        key = classe.lower().strip()
        data = CLASSI.get(key)

        if data is None:
            nomi = ", ".join(f"**{v['titolo']}**" for v in CLASSI.values())
            await ctx.send(f"❌ Classe '{classe}' non trovata.\n📚 Disponibili: {nomi}")
            return

        embed = discord.Embed(
            title=f"{data['titolo']} — Scheda Completa",
            description=data["descrizione"],
            color=data["colore"],
        )
        embed.add_field(name="🧠 Tratti principali", value=data["tratti"], inline=False)

        for nome, desc in data["abilita_chiave"].items():
            embed.add_field(name=nome, value=desc, inline=False)

        embed.add_field(name="✨ Incantesimi", value=data["incantesimi"], inline=False)
        embed.add_field(name="🎒 Background consigliato", value=data["background"], inline=False)
        embed.set_footer(text="Grimory Bot • Compendio D&D 5e")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Compendium(bot))
