import discord
from discord.ext import commands

class Compendium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def classinfo(self, ctx, *, classe: str):
        classe = classe.lower().strip()

        # ======================
        # BARBARO
        # ======================
        if classe == "barbaro":
            embed = discord.Embed(
                title="Barbaro - Scheda Completa",
                description=(
                    "I barbari sono potenti guerrieri alimentati dalle forze primordiali del multiverso che si manifestano come rabbia. "
                    "Sono formidabili in combattimento corpo a corpo e sfruttano la loro furia per infliggere danni devastanti."
                ),
                color=0xAA0000
            )
            embed.add_field(
                name="🧠 Tratti principali del Barbaro",
                value=(
                    "- Forza come abilità primaria\n"
                    "- D12 punti vita per livello\n"
                    "- Tiri salvezza: Forza e Costituzione\n"
                    "- Competenze in 2 abilità tra: Gestione Animali, Atletica, Intimidazione, Natura, Percezione, Sopravvivenza\n"
                    "- Armi: Armi semplici e marziali\n"
                    "- Armatura: Leggera e media + scudi\n"
                    "- Equipaggiamento iniziale a scelta:\n"
                    "  A) Ascia grande, 4 asce da lancio, Kit dell'esploratore, 15 GP\n"
                    "  B) 75 GP"
                ),
                inline=False
            )
            embed.add_field(
                name="🔥 Furia",
                value=(
                    "Puoi infonderti di un potere primordiale chiamato Furia, che ti conferisce forza e resilienza straordinarie. "
                    "Puoi attivarla come azione bonus se non indossi armature pesanti.\n"
                    "- Resistenza ai danni contundenti, perforanti e da taglio\n"
                    "- Bonus al danno quando attacchi con Forza (arma o colpo senz'armi)\n"
                    "- Vantaggio alle prove di Forza e tiri salvezza su Forza\n"
                    "- Non puoi concentrare incantesimi né lanciarli\n"
                    "- Durata: fino alla fine del turno successivo, estendibile fino a 10 minuti"
                ),
                inline=False
            )
            embed.add_field(
                name="🛡️ Difesa senza armatura",
                value=(
                    "Se non indossi armature, la tua Classe Armatura base è 10 + modificatore di Destrezza + modificatore di Costituzione. "
                    "Puoi comunque usare uno scudo."
                ),
                inline=False
            )
            embed.add_field(
                name="⚔️ Padronanza delle armi",
                value=(
                    "La tua formazione con le armi ti permette di usare le proprietà di maestria di due tipi di armi corpo a corpo semplici o marziali a scelta. "
                    "Ogni riposo lungo puoi esercitarti e cambiare una di queste scelte."
                ),
                inline=False
            )
            embed.add_field(
                name="✨ Incantesimi",
                value="I barbari **non hanno incantesimi**, si concentrano sul combattimento corpo a corpo e sulla Furia.",
                inline=False
            )
            embed.add_field(
                name="🎒 Background consigliato",
                value="Esempi di background adatti: Selvaggio, Guerriero tribale, Avventuriero di confini.",
                inline=False
            )

        # ======================
        # BARDO
        # ======================
        elif classe == "bardo":
            embed = discord.Embed(
                title="Bardo - Scheda Completa",
                description=(
                    "I bardi sono maestri dell'ispirazione attraverso parole, musica o danza. "
                    "Usano la loro magia e abilità artistiche per supportare gli alleati, incantare nemici e manipolare il campo di battaglia."
                ),
                color=0x5500AA
            )
            embed.add_field(
                name="🧠 Tratti principali del Bardo",
                value=(
                    "- Carisma come abilità primaria\n"
                    "- D8 punti vita per livello\n"
                    "- Tiri salvezza: Destrezza e Carisma\n"
                    "- Competenze in 3 abilità a scelta\n"
                    "- Armi: Armi semplici\n"
                    "- Strumenti: 3 strumenti musicali a scelta\n"
                    "- Armatura: Leggera\n"
                    "- Equipaggiamento iniziale:\n"
                    "  A) Armatura di cuoio, 2 pugnali, strumento musicale a scelta, Kit dell'intrattenitore, 19 GP\n"
                    "  B) 90 GP"
                ),
                inline=False
            )
            embed.add_field(
                name="🎵 Ispirazione Bardica",
                value=(
                    "Puoi ispirare un alleato entro 60 piedi come Azione Bonus, concedendogli un dado di Ispirazione Bardica (d6 a livello 1).\n"
                    "Un alleato può usare questo dado entro 1 ora per aggiungerlo a un tiro di dado fallito.\n"
                    "- Numero di usi: pari al modificatore di Carisma (minimo 1), recuperati con riposo lungo\n"
                    "- A livelli più alti, il dado aumenta: d8 a livello 5, d10 a livello 10, d12 a livello 15"
                ),
                inline=False
            )
            embed.add_field(
                name="✨ Incantesimi",
                value=(
                    "- Conosci 2 trucchetti a scelta dalla lista incantesimi del Bardo\n"
                    "- A livelli 4 e 10 impari nuovi trucchetti\n"
                    "- Prepari incantesimi di livello 1+ (4 incantesimi a livello 1)\n"
                    "- Slot incantesimi recuperati con riposo lungo\n"
                    "- Carisma è la tua abilità di lancio\n"
                    "- Puoi usare strumenti musicali come focus per gli incantesimi"
                ),
                inline=False
            )
            embed.add_field(
                name="🎒 Background consigliato",
                value="Intrattenitore, Artista itinerante, Cantore di leggende, Maestro di corte.",
                inline=False
            )

        # ======================
        # CLASSE NON TROVATA
        # ======================
        else:
            await ctx.send(f"Classe '{classe}' non trovata. Al momento disponibili: **Barbaro**, **Bardo**.")
            return

        await ctx.send(embed=embed)


# Setup
async def setup(bot):
    await bot.add_cog(Compendium(bot))
