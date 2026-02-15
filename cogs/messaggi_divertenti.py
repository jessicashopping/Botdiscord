import discord
from discord.ext import commands
import random


PAROLE_BAN = [
    "dio", "porco", "madonna", "cristo", "porca madonna"
]

RISPOSTE = [
    "🧌 L'orco alza il boccale: Amen, fratello.",
    "😇 Il celestiale ti fulmina con lo sguardo: Misura le parole, mortale.",
    "🧙 Il mago segna qualcosa sul grimorio: 'Studio sul linguaggio degenerato - capitolo 4'.",
    "🐉 Il drago apre un occhio: Davvero interrompi il mio sonno per questo?",
    "⚔️ Il paladino perde 1 punto Fede. *Sistema morale aggiornato.*",
    "👹 Il demone annuisce soddisfatto.",
    "🪦 Uno scheletro applaude lentamente dal fondo della cripta.",
    "🧝 L'elfo sospira: Vivete così poco… e sprecate pure le parole.",
    "⛏️ Il nano borbotta: Ai miei tempi si bestemmiava con più dignità.",
    "🎲 Il dado d20 rotola da solo… ed esce 1. Fallimento critico nel parlare.",
    "📜 Un antico tomo si chiude di scatto: 'Linguaggio inappropriato rilevato.'",
    "🔥 Un tiefling sorride: Finalmente qualcuno che parla la mia lingua.",
    "🌿 La driade appassisce leggermente.",
    "🛡️ Il cavaliere dice: Questo non era nel codice d'onore.",
    "🕯️ Una candela si spegne misteriosamente.",
    "🧙‍♂️ L'arcimago sussurra: Le parole hanno potere. Anche quelle brutte.",
    "🐺 Un lupo ulula in segno di disapprovazione.",
    "🧛 Il vampiro commenta: Ho sentito maledizioni migliori nel XIV secolo.",
    "🪄 Una scintilla magica esplode: Incantesimo 'Parolaccia Minore' lanciato!",
    "📯 Una tromba celestiale suona in segno di protesta.",
    "🧞 Il genio emerge: Desideri riformulare?",
    "🗡️ Il ladro sussurra: Ehi… certe cose si dicono piano.",
    "🏰 Le mura del castello vibrano leggermente.",
    "🌩️ Un tuono lontano risponde.",
    "📖 Il narratore prende nota: 'E fu in quel momento che perse carisma.'",
    "⚰️ Un necromante approva con entusiasmo inquietante.",
    "🐲 Un cucciolo di drago ripete la parola. Ottimo esempio.",
    "🍺 Un barbaro urla: FINALMENTE UN PO' DI POESIA!",
    "🔮 La sfera di cristallo si incrina leggermente.",
    "🧙‍♀️ Una strega ride: Ah, linguaggio folkloristico.",
    "⛓️ Le catene eteree tintinnano.",
    "🛐 Un chierico lancia 'Silenzio'... ma fallisce.",
    "🎭 Un bardo applaude: Che drammaticità!",
    "🧱 Un golem registra: 'Input lessicale non ottimale.'",
    "🌌 Un portale si apre e si richiude per imbarazzo.",
    "🧟 Uno zombie mormora qualcosa di incomprensibile in risposta.",
    "🧝‍♂️ L'elfo oscuro sorride compiaciuto.",
    "📢 Una voce divina riecheggia: Moderazione, mortale.",
    "🪨 Un elementale della pietra resta in silenzio giudicante.",
    "🐐 Un diavolo prende appunti per un futuro contratto.",
    "🏹 L'arciere manca il bersaglio per distrazione linguistica.",
    "⚡ Un incantesimo 'Richiamo Educato' viene preparato.",
    "📚 Il bibliotecario arcano ti guarda malissimo.",
    "🪶 Una piuma angelica cade lentamente.",
    "🧊 Un lich commenta: Patetico. Prova con qualcosa di più creativo.",
]

class MessaggiDivertenti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        testo = message.content.lower()

        if any(parola in testo for parola in PAROLE_BAN):
            risposta = random.choice(RISPOSTE)
            await message.channel.send(risposta)


async def setup(bot):
    await bot.add_cog(MessaggiDivertenti(bot))
