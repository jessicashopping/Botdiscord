import discord
from discord.ext import commands


LORE_DATA = {
    # ── Classi ───────────────────────────────────────────
    "barbaro": {
        "title": "Barbaro",
        "description": (
            "I barbari sono potenti guerrieri alimentati dalle forze primordiali del multiverso.\n\n"
            "**Origine:** provengono spesso da tribù ai margini della civiltà, "
            "dove la forza bruta è l'unica legge. La loro Furia è un dono ancestrale "
            "che li rende quasi inarrestabili in combattimento."
        ),
    },
    "bardo": {
        "title": "Bardo",
        "description": (
            "I bardi tessono magia attraverso parole, musica e danza.\n\n"
            "**Origine:** le prime scuole bardiche nacquero nelle corti elfiche, "
            "dove la musica era considerata la forma più pura di magia. "
            "Oggi i bardi sono narratori, spie e diplomatici."
        ),
    },
    "chierico": {
        "title": "Chierico",
        "description": (
            "I chierici sono il tramite tra i mortali e le divinità.\n\n"
            "**Origine:** ogni chierico risponde a una divinità del pantheon. "
            "Il loro potere non viene dallo studio ma dalla fede e dal servizio devoto."
        ),
    },
    "druido": {
        "title": "Druido",
        "description": (
            "I druidi sono custodi della natura e dell'equilibrio del mondo.\n\n"
            "**Origine:** i primi druidi appresero i segreti della Forma Selvatica "
            "dai circoli fatati della Selva Fatata. Parlano il Druidico, un linguaggio segreto."
        ),
    },
    "guerriero": {
        "title": "Guerriero",
        "description": (
            "Maestri d'armi e strateghi, i guerrieri eccellono in ogni forma di combattimento.\n\n"
            "**Origine:** dai cavalieri delle grandi casate ai mercenari di frontiera, "
            "il guerriero è la spina dorsale di ogni esercito."
        ),
    },
    "mago": {
        "title": "Mago",
        "description": (
            "I maghi studiano le leggi arcane che governano il multiverso.\n\n"
            "**Origine:** le grandi accademie di magia formano i maghi attraverso anni di studio. "
            "Il loro potere è nel libro degli incantesimi, custodito gelosamente."
        ),
    },
    "paladino": {
        "title": "Paladino",
        "description": (
            "I paladini sono guerrieri sacri legati da un giuramento inviolabile.\n\n"
            "**Origine:** il loro potere non viene solo dalla divinità, "
            "ma dalla forza della promessa stessa. Rompere il giuramento significa perdere tutto."
        ),
    },

    # ── Razze ────────────────────────────────────────────
    "elfo": {
        "title": "Elfo",
        "description": (
            "Gli elfi sono creature agili e longeve, famose per grazia e conoscenza arcana.\n\n"
            "**Durata della vita:** fino a 750 anni\n"
            "**Tratti:** Visione crepuscolare, resistenza a charme, trance invece del sonno\n"
            "**Sotto-razze:** Elfo alto (bonus Int), Elfo dei boschi (bonus Sag), Drow (bonus Car)"
        ),
    },
    "nano": {
        "title": "Nano",
        "description": (
            "I nani sono robusti e ostinati, maestri nella lavorazione della pietra e dei metalli.\n\n"
            "**Durata della vita:** fino a 400 anni\n"
            "**Tratti:** Visione crepuscolare, resistenza al veleno, competenza con ascia e martello\n"
            "**Sotto-razze:** Nano delle colline (bonus Sag), Nano delle montagne (bonus For)"
        ),
    },
    "umano": {
        "title": "Umano",
        "description": (
            "Gli umani sono la razza più diffusa e adattabile del multiverso.\n\n"
            "**Durata della vita:** circa 80 anni\n"
            "**Tratti:** +1 a tutte le abilità (variante: un talento extra)\n"
            "**Cultura:** estremamente varia — dai regni feudali alle città-stato mercantili."
        ),
    },
    "tiefling": {
        "title": "Tiefling",
        "description": (
            "I tiefling portano il marchio di un'eredità infernale nel loro sangue.\n\n"
            "**Tratti:** Visione crepuscolare, resistenza al fuoco, incantesimi innati\n"
            "**Aspetto:** corna, coda, occhi senza pupilla, pelle rossastra o viola\n"
            "**Società:** spesso discriminati, trovano rifugio nelle città cosmopolite."
        ),
    },
    "dragonide": {
        "title": "Dragonide",
        "description": (
            "I dragonidi sono discendenti dei draghi, fieri e onorevoli.\n\n"
            "**Tratti:** soffio del drago (tipo di danno legato all'ascendenza), resistenza al tipo associato\n"
            "**Ascendenze:** Nero (acido), Blu (fulmine), Rosso (fuoco), Bianco (freddo), Verde (veleno) e altre.\n"
            "**Cultura:** basata su clan e onore."
        ),
    },
    "halfling": {
        "title": "Halfling",
        "description": (
            "Gli halfling sono piccoli, agili e incredibilmente fortunati.\n\n"
            "**Tratti:** Fortunato (rilancia gli 1 naturali), Coraggioso (vantaggio vs paura), Agile\n"
            "**Sotto-razze:** Piedelesto (bonus Car, furtività naturale), Tozzo (bonus Cos, resistenza al veleno)"
        ),
    },

    # ── Creature ─────────────────────────────────────────
    "drago": {
        "title": "Draghi",
        "description": (
            "I draghi sono le creature più potenti e temute del multiverso.\n\n"
            "**Draghi cromatici** (malvagi): Rosso (fuoco), Nero (acido), Blu (fulmine), Verde (veleno), Bianco (freddo)\n"
            "**Draghi metallici** (buoni): Oro (fuoco), Argento (freddo), Bronzo (fulmine), Rame (acido), Ottone (fuoco)\n\n"
            "I draghi crescono in potere con l'età: cucciolo → giovane → adulto → antico → grande dragone."
        ),
    },
    "beholder": {
        "title": "Beholder",
        "description": (
            "Sfere fluttuanti dotate di un grande occhio centrale e tentacoli oculari.\n\n"
            "**Grado sfida:** 13\n"
            "**Raggio anti-magia** dal suo occhio centrale annulla ogni magia nel cono.\n"
            "**Raggi oculari:** Charme, Paralisi, Paura, Rallentamento, Disintegrazione e altri.\n"
            "Creature supremamente paranoiche — ogni beholder crede di essere perfetto."
        ),
    },
    "lich": {
        "title": "Lich",
        "description": (
            "Un lich è un mago così potente da aver sconfitto la morte stessa.\n\n"
            "**Filatterio:** l'oggetto che contiene la sua anima. Finché esiste, il lich non può morire.\n"
            "**Poteri:** incantesimi di alto livello, aura di paura, tocco paralizzante.\n"
            "**Cultura:** i lich sono spesso ossessionati dalla conoscenza e dal controllo."
        ),
    },
    "mimic": {
        "title": "Mimic",
        "description": (
            "I mimic sono creature mutaforma che si camuffano da oggetti inanimati, "
            "tipicamente bauli del tesoro.\n\n"
            "**Grado sfida:** 2\n"
            "**Tattiche:** attendono pazientemente che una preda si avvicini, "
            "poi la afferrano con un adesivo naturale. Sono l'incubo di ogni avventuriero."
        ),
    },

    # ── Piani di esistenza ───────────────────────────────
    "feywild": {
        "title": "Selva Fatata (Feywild)",
        "description": (
            "Un riflesso magico del mondo materiale, pieno di meraviglie e pericoli.\n\n"
            "**Abitanti:** fate, eladrin, satiri, driadi, arci-fate\n"
            "**Caratteristiche:** colori vividi, emozioni amplificate, il tempo scorre diversamente.\n"
            "Chi vi entra può uscire scoprendo che sono passati anni… o secoli."
        ),
    },
    "shadowfell": {
        "title": "Shadowfell",
        "description": (
            "L'oscuro riflesso del mondo materiale, un piano di decadenza e disperazione.\n\n"
            "**Abitanti:** non morti, ombre, il Corvo della Mezzanotte\n"
            "**Caratteristiche:** colori sbiaditi, tristezza pervasiva, confine sottile con la morte."
        ),
    },
}


class Lore(commands.Cog):
    """Enciclopedia del mondo di D&D."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["enciclopedia"])
    async def lore(self, ctx, *, topic: str = None):
        """Mostra informazioni lore su classi, razze, creature e piani.
        Uso: !lore <argomento>
        Esempio: !lore drago"""

        if topic is None:
            # raggruppa per categoria
            classi = ["barbaro", "bardo", "chierico", "druido", "guerriero", "mago", "paladino"]
            razze = ["elfo", "nano", "umano", "tiefling", "dragonide", "halfling"]
            creature = ["drago", "beholder", "lich", "mimic"]
            piani = ["feywild", "shadowfell"]

            embed = discord.Embed(
                title="📚 Enciclopedia di Grimory",
                description="Usa `!lore <argomento>` per saperne di più.",
                color=0x3498DB,
            )
            embed.add_field(name="⚔️ Classi", value=", ".join(classi), inline=False)
            embed.add_field(name="🧝 Razze", value=", ".join(razze), inline=False)
            embed.add_field(name="🐉 Creature", value=", ".join(creature), inline=False)
            embed.add_field(name="🌌 Piani", value=", ".join(piani), inline=False)
            embed.set_footer(text="Grimory Bot • Scopri il mondo di D&D")
            await ctx.send(embed=embed)
            return

        key = topic.lower().strip().replace(" ", "_")
        data = LORE_DATA.get(key)

        if data is None:
            available = ", ".join(sorted(LORE_DATA.keys()))
            await ctx.send(f"❌ Nessuna voce per '{topic}'.\n📚 Argomenti disponibili: {available}")
            return

        embed = discord.Embed(
            title=f"📖 {data['title']}",
            description=data["description"],
            color=0x3498DB,
        )
        embed.set_footer(text="Grimory Bot • Enciclopedia D&D")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Lore(bot))
