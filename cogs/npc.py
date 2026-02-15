import discord
from discord.ext import commands
import random

class NPC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ✅ Liste dettagliate
        self.names = [
            "Arin","Brom","Cedric","Doran","Elric","Fendrel","Garrick","Haldor","Irin","Jareth",
            "Kael","Loric","Merrick","Nolan","Orrin","Perrin","Quentin","Roderick","Sylas","Theron",
            "Ulric","Varric","Wendell","Xander","Yorick","Zarek","Alden","Bastian","Cassius","Darius",
            "Edric","Fabian","Galen","Hadrian","Isidore","Jasper","Kieran","Lucian","Magnus","Nevin",
            "Orin","Percival","Quillon","Rafferty","Soren","Tobias","Urian","Valen","Wyatt","Zev"
        ]
        self.genders = [
            "Maschio","Femmina","Non-binario","Transmaschile","Transfemminile","Agender"
        ]
        self.races = [
            "Umano","Elfo","Nano","Halfling","Mezzelfo","Dragonide","Tiefling","Gnomo","Orco","Mezzorco"
        ]
        self.classes = [
            "Guerriero","Mago","Ladro","Chierico","Paladino","Ranger","Stregone","Bardo","Druido","Monaco"
        ]
        self.jobs = [
            "Mercante","Guardia","Contadino","Artigiano","Alchimista","Cacciatore","Sacerdote","Insegnante",
            "Nobile","Bandito","Erborista","Esploratore","Marettino","Guaritore","Viaggiatore","Avventuriero",
            "Sarto","Cavaliere","Bibliotecario","Mastro fabbro","Carpentiere","Astrologo","Guerriero errante",
            "Mendicante","Pescatore","Fabbro","Cartografo","Cacciatore di mostri","Maestro di spade",
            "Cantastorie","Mineratore","Erudito","Guida","Saggio","Allevatore","Monaco errante","Alchimista pazzo",
            "Arciere","Messaggero","Guerriero mercenario","Contadino ricco","Curatore","Spadaccino","Custode",
            "Banchiere","Maestro d'armi","Pastore","Navigatore","Artista","Vigilante"
        ]
        self.hobbies = [
            "colleziona monete","suona il liuto","cucina","pittura","giardinaggio","alchimia","lettura",
            "racconta storie","caccia","pescare","scacchi","scrittura","artigianato","viaggiare",
            "ballo","poesia","cantare","escursionismo","meditazione","apicoltura","artigianato del legno",
            "caccia al tesoro","yoga","equitazione","colleziona gemme","sci","artigianato magico","allevare animali",
            "osservare stelle","astronomia","giocoleria","puzzle","risolvere enigmi","calligrafia","modellismo",
            "pittura a olio","modellare argilla","creare pozioni","pasticceria","cucito","acquerello","caccia fotografica",
            "scultura","raccolta erbe","corsetta","ciclismo","musica","scrittura di diario","decorazione","escursioni"
        ]
        self.traits = [
            "arrogante","gentile","timido","coraggioso","ingenuo","furbo","sarcastico","prudente","impulsivo",
            "leale","traditore","curioso","spiritoso","paziente","ambizioso","scaltro","studioso","scontroso",
            "estroverso","introverso","ottimista","pessimista","sensibile","distratto","tenace","avidità","giusto",
            "egoista","misterioso","affascinante","cinico","romantico","lunatico","polemico","pacifico","leale agli amici",
            "vendicativo","malizioso","altruista","giocoso","ipercritico","riflessivo","furioso","innocente","carismatico",
            "timoroso","ribelle","onesto","ingannevole","stoico","esuberante","saggio","pigrone","attento"
        ]
        self.fears = [
            "ragni","non morti","altezza","oscurità","acqua","fuoco","perdere potere","solitudine","tradimento",
            "fallire","mostri","cimiteri","streghe","draghi","vampiri","serpenti","fulmini","tempeste","trappole",
            "sangue","insetti","spettri","pirati","perdere i genitori","crollo morale","perdere memoria","povertà",
            "malattie","ostacoli","violenza","perdere amici","fallimento pubblico","guerre","mostri marini",
            "crollo casa","uccelli","cani","gatti","mostri alati","fuochi fatui","fantasmi","maghi malvagi",
            "dimenticare incantesimi","invecchiare","cadere","bucare","freddo","caldo","affogare","perdere ricchezze",
            "essere catturato"
        ]
        self.goals = [
            "diventare ricco","trovare un artefatto","salvare il regno","scoprire un segreto","vendicare un parente",
            "diventare famoso","sconfiggere un nemico","trovare amore","essere potente","proteggere un amico",
            "diventare maestro d'armi","trovare un tesoro","imparare un incantesimo","diventare nobile",
            "aprire una gilda","scoprire una reliquia","diventare saggio","inseguire un sogno","viaggiare il mondo",
            "guarire un malato","salvare una città","essere rispettato","conquistare un castello","difendere una fortezza",
            "ritrovare un amico","scoprire la verità","essere libero","ottenere vendetta","imparare l'alchimia",
            "scoprire misteri","allenarsi duramente","ottenere fama","difendere innocenti","viaggiare in terre lontane",
            "riscoprire antichi tesori","superare prove","ottenere conoscenza","proteggere creature magiche",
            "sconfiggere mostri","trovare un mentor","curare malattie","creare incantesimi","ottenere ricchezze",
            "viaggiare con animali","addestrare guerrieri","scoprire la magia","ottenere artefatti"
        ]
        self.secrets = [
            "è una spia","nasconde un tesoro","ha un passato oscuro","ha ucciso per amore",
            "ha tradito un re","ha una malattia","è il figlio di un nobile","ha mentito a un amico",
            "possiede un oggetto magico","ha un legame con un drago","è inseguito da criminali",
            "nasconde un potere magico","ha una maledizione","è stato imprigionato ingiustamente",
            "è un sopravvissuto di guerra","ha perso la memoria","ha un segreto di famiglia","è un ladro redento",
            "è un assassino","è un custode di conoscenza","ha un fratello gemello","è stato tradito",
            "ha un passato criminale","nasconde una profezia","è maledetto","ha un nemico potente",
            "ha incontrato creature leggendarie","è stato maltrattato","ha un debito","nasconde un amore",
            "ha un talento nascosto","è stato esiliato","ha un potere oscuro","ha un artefatto",
            "ha un passato romantico","nasconde un incantesimo","è un alleato segreto","ha un tesoro nascosto",
            "è un esploratore","ha un compagno animale","ha una debolezza","ha una paura profonda",
            "ha un destino speciale","ha un dono","è sotto un incantesimo","nasconde una doppia vita",
            "ha un passato misterioso","ha vissuto in terre lontane","ha conoscenze proibite",
            "è un guerriero leggendario","ha un codice morale unico","nasconde un legame divino"
        ]

        self.hair_colors = ["neri","castani","biondi","rossi","grigi","bianchi","argentei","azzurri"]
        self.eye_colors = ["azzurri","verdi","marroni","neri","grigi","dorati","viola","celesti"]
        self.skin_colors = ["chiara","olivastra","scura","bronzea","pallida","ambrata","rossastra","tintarella"]
        self.builds = ["snella","muscolosa","robusta","alta","bassa","media","longilinea","tonica"]
        self.face_flaws = ["cicatrice sul volto","occhio di vetro","dente mancante","macchia sulla pelle","bruciatura","tattoo tribale","occhi asimmetrici","orecchie a punta"]
        self.clothes = ["tunica di lino","mantello di pelle","armatura leggera","vestito elegante","mantello strappato","giacca di pelle","armatura completa","camicia di seta","pantaloni di lino","tunica colorata"]
        self.accessories = ["anello d'oro","collana con gemma","bracciale","orecchini","cintura","stivali","cappello","mantello","fascia magica","amuleto"]
        self.weapons = ["spada lunga","ascia bipenne","pugnale","arco","bastone","martello da guerra","lancia","katana","frusta","bastone magico"]

    @commands.command()
    async def npc(self, ctx):
        # Genera casualmente
        nome = random.choice(self.names)
        sesso = random.choice(self.genders)
        razza = random.choice(self.races)
        classe = random.choice(self.classes)
        lavoro = random.choice(self.jobs)
        hobby = random.choice(self.hobbies)
        tratto = random.choice(self.traits)
        paura = random.choice(self.fears)
        obiettivo = random.choice(self.goals)
        segreto = random.choice(self.secrets)

        capelli = random.choice(self.hair_colors)
        occhi = random.choice(self.eye_colors)
        pelle = random.choice(self.skin_colors)
        corporatura = random.choice(self.builds)
        difetto = random.choice(self.face_flaws)
        vestito = random.choice(self.clothes)
        accessorio = random.choice(self.accessories)
        arma = random.choice(self.weapons)

        descrizione_aspetto = (
            f"Capelli: {capelli}\n"
            f"Occhi: {occhi}\n"
            f"Pelle: {pelle}\n"
            f"Corporatura: {corporatura}\n"
            f"Difetti viso/corpo: {difetto}\n"
            f"Vestiti: {vestito}\n"
            f"Accessori: {accessorio}\n"
            f"Arma: {arma}"
        )

        embed = discord.Embed(
            title=f"🧙 NPC • {nome}",
            description="Scheda NPC",
            color=discord.Color.dark_gold()
        )

        embed.add_field(
            name="📜 Identità",
            value=f"Sesso: {sesso}\nRazza: {razza}\nClasse: {classe}\nProfessione: {lavoro}",
            inline=False
        )

        embed.add_field(
            name="🧠 Personalità",
            value=f"Tratto: {tratto}\nHobby: {hobby}\nPaura: {paura}\nObiettivo: {obiettivo}\nSegreto: {segreto}",
            inline=False
        )

        embed.add_field(
            name="🎨 Aspetto Completo",
            value=descrizione_aspetto,
            inline=False
        )

        embed.set_footer(text="NPC Generator • Grimory Bot")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NPC(bot))
