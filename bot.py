import discord
from discord.ext import commands
import asyncio
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

# ── Intents ──────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessario per welcome/goodbye

# ── Help personalizzato ──────────────────────────────────
class GrimoryHelp(commands.HelpCommand):
    """Help command personalizzato con embed a tema D&D."""

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="📜 Grimorio dei Comandi",
            description=(
                "Benvenuto, avventuriero! Ecco tutti i comandi disponibili.\n"
                "Usa `!help <comando>` per dettagli su un comando specifico."
            ),
            color=0x8B4513,
        )

        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            if not filtered:
                continue
            cog_name = cog.qualified_name if cog else "Generali"
            cmd_list = " · ".join(f"`!{c.name}`" for c in filtered)
            embed.add_field(name=f"⚔️ {cog_name}", value=cmd_list, inline=False)

        embed.set_footer(text="Grimory Bot • Il tuo compagno di avventura")
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"📖 !{command.qualified_name}",
            description=command.help or "Nessuna descrizione disponibile.",
            color=0x8B4513,
        )
        if command.aliases:
            embed.add_field(
                name="Alias",
                value=", ".join(f"`!{a}`" for a in command.aliases),
                inline=False,
            )
        embed.set_footer(text="Grimory Bot • Il tuo compagno di avventura")
        channel = self.get_destination()
        await channel.send(embed=embed)


# ── Bot ──────────────────────────────────────────────────
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    case_insensitive=True,
    help_command=GrimoryHelp(),
)

# Lista di tutti i cog da caricare
EXTENSIONS = [
    "cogs.compendium",
    "cogs.dice",
    "cogs.npc",
    "cogs.jokes",
    "cogs.lore",
    "cogs.messaggi_divertenti",
    "cogs.coin",
    "cogs.taverna",
    "cogs.encounter",
    "cogs.welcome",
    "cogs.config",
]


@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="D&D 5e · !help",
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ {bot.user} avviato correttamente!")
    print(f"   Server collegati: {len(bot.guilds)}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando sconosciuto. Usa `!help` per la lista dei comandi.")
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Argomento mancante: `{error.param.name}`. Usa `!help {ctx.command}` per maggiori info.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"⚠️ Argomento non valido. Usa `!help {ctx.command}` per maggiori info.")
        return

    print(f"Errore nel comando {ctx.command}: {error}")
    traceback.print_exception(type(error), error, error.__traceback__)
    await ctx.send(f"⚠️ Errore imprevisto: {error}")


async def main():
    async with bot:
        for ext in EXTENSIONS:
            try:
                await bot.load_extension(ext)
                print(f"  ✔ {ext}")
            except Exception as e:
                print(f"  ✘ {ext} — {e}")

        print("Tutti i cog caricati!")
        await bot.start(os.getenv("TOKEN"))


asyncio.run(main())
