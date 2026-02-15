import discord
from discord.ext import commands
import asyncio
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print(f"{bot.user} avviato correttamente!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"Messaggio ricevuto da {message.author}: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(f"Errore nel comando {ctx.command}: {error}")
    traceback.print_exception(type(error), error, error.__traceback__)
    await ctx.send(f"⚠️ Errore nel comando: {error}")

async def main():
    async with bot:
        await bot.load_extension("cogs.compendium")
        await bot.load_extension("cogs.dice")
        await bot.load_extension("cogs.npc")
        await bot.load_extension("cogs.jokes")
        await bot.load_extension("cogs.lore")
        await bot.load_extension("cogs.messaggi_divertenti")

        print("Tutti i cog caricati!")

        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())