import discord
from discord.ext import commands
import random
import re


class Dice(commands.Cog):
    """Tira dadi di ogni tipo per le tue avventure."""

    def __init__(self, bot):
        self.bot = bot

    # ── Utility ──────────────────────────────────────────
    @staticmethod
    def _parse_and_roll(dice_str: str):
        """Parsa una stringa tipo '2d6+1d4+3' e restituisce risultati e totale."""
        dice_str = dice_str.replace(" ", "")

        dice_pattern = r"(\d*)d(\d+)"
        dice_matches = re.findall(dice_pattern, dice_str)
        dice_cleaned = re.sub(dice_pattern, "", dice_str)

        mod_pattern = r"([+-]\d+)"
        mod_matches = re.findall(mod_pattern, dice_cleaned)
        mod_total = sum(int(m) for m in mod_matches)

        if not dice_matches and not mod_matches:
            return None, None, None

        results = []
        total = mod_total
        for count, sides in dice_matches:
            count = int(count) if count else 1
            sides = int(sides)
            rolls = [random.randint(1, sides) for _ in range(count)]
            results.append((f"{count}d{sides}", rolls))
            total += sum(rolls)

        return results, mod_matches, total

    # ── !roll ────────────────────────────────────────────
    @commands.command()
    async def roll(self, ctx, *, dice: str):
        """Tira dadi con modificatori.
        Uso: !roll 1d20+5  ·  !roll 2d6+1d4+3"""
        results, mods, total = self._parse_and_roll(dice)

        if results is None:
            await ctx.send("⚠️ Formato non valido. Usa ad esempio `!roll 1d20+3` o `!roll 2d6`.")
            return

        embed = discord.Embed(title="🎲 Tiro di dadi", color=0x1ABC9C)
        for dtype, rolls in results:
            embed.add_field(name=dtype, value=" + ".join(map(str, rolls)), inline=True)
        if mods:
            embed.add_field(name="Modificatori", value=", ".join(mods), inline=True)
        embed.add_field(name="🏆 Totale", value=f"**{total}**", inline=False)

        await ctx.send(embed=embed)

    # ── !adv / !dis ──────────────────────────────────────
    @commands.command(aliases=["vantaggio"])
    async def adv(self, ctx, mod: int = 0):
        """Tiro con vantaggio (2d20, prendi il più alto) + modificatore opzionale.
        Uso: !adv   ·   !adv 5"""
        r1, r2 = random.randint(1, 20), random.randint(1, 20)
        best = max(r1, r2)
        total = best + mod

        embed = discord.Embed(title="🎲 Tiro con Vantaggio", color=0x2ECC71)
        embed.add_field(name="Dadi", value=f"**{r1}**  |  **{r2}**", inline=True)
        embed.add_field(name="Scelto", value=f"**{best}**", inline=True)
        if mod:
            embed.add_field(name="Mod", value=f"{mod:+}", inline=True)
        embed.add_field(name="🏆 Totale", value=f"**{total}**", inline=False)
        if best == 20:
            embed.set_footer(text="⭐ CRITICO NATURALE!")
        elif best == 1:
            embed.set_footer(text="💀 Fallimento critico!")

        await ctx.send(embed=embed)

    @commands.command(aliases=["svantaggio"])
    async def dis(self, ctx, mod: int = 0):
        """Tiro con svantaggio (2d20, prendi il più basso) + modificatore opzionale.
        Uso: !dis   ·   !dis -2"""
        r1, r2 = random.randint(1, 20), random.randint(1, 20)
        worst = min(r1, r2)
        total = worst + mod

        embed = discord.Embed(title="🎲 Tiro con Svantaggio", color=0xE74C3C)
        embed.add_field(name="Dadi", value=f"**{r1}**  |  **{r2}**", inline=True)
        embed.add_field(name="Scelto", value=f"**{worst}**", inline=True)
        if mod:
            embed.add_field(name="Mod", value=f"{mod:+}", inline=True)
        embed.add_field(name="🏆 Totale", value=f"**{total}**", inline=False)
        if worst == 1:
            embed.set_footer(text="💀 Fallimento critico!")

        await ctx.send(embed=embed)

    # ── !stats ───────────────────────────────────────────
    @commands.command(aliases=["rollstats", "statistiche"])
    async def stats(self, ctx):
        """Genera 6 statistiche con il metodo 4d6 drop lowest."""
        abilities = []
        details = []
        for _ in range(6):
            rolls = sorted([random.randint(1, 6) for _ in range(4)])
            dropped = rolls[0]
            kept = rolls[1:]
            total = sum(kept)
            abilities.append(total)
            details.append(f"~~{dropped}~~ {' + '.join(map(str, kept))} = **{total}**")

        embed = discord.Embed(
            title="📊 Generazione Statistiche (4d6 drop lowest)",
            color=0x9B59B6,
        )
        nomi_stat = ["FOR", "DES", "COS", "INT", "SAG", "CAR"]
        for nome, det in zip(nomi_stat, details):
            embed.add_field(name=nome, value=det, inline=True)
        embed.add_field(
            name="📈 Riepilogo",
            value=f"Valori: **{', '.join(map(str, sorted(abilities, reverse=True)))}** — Totale: **{sum(abilities)}**",
            inline=False,
        )
        embed.set_footer(text="Assegna i valori alle abilità come preferisci!")
        await ctx.send(embed=embed)

    # ── !init ────────────────────────────────────────────
    @commands.command(aliases=["iniziativa"])
    async def init(self, ctx, mod: int = 0):
        """Tira per l'iniziativa (1d20 + modificatore).
        Uso: !init   ·   !init 3"""
        roll = random.randint(1, 20)
        total = roll + mod

        embed = discord.Embed(title="⚡ Tiro Iniziativa", color=0xF39C12)
        embed.add_field(name="d20", value=f"**{roll}**", inline=True)
        if mod:
            embed.add_field(name="Mod", value=f"{mod:+}", inline=True)
        embed.add_field(name="🏆 Iniziativa", value=f"**{total}**", inline=False)

        if roll == 20:
            embed.set_footer(text="⭐ Primo in battaglia!")
        elif roll == 1:
            embed.set_footer(text="🐌 Ultimo in fila...")

        await ctx.send(embed=embed)

    # ── !perc ────────────────────────────────────────────
    @commands.command(aliases=["percentuale", "d100"])
    async def perc(self, ctx):
        """Tira un dado percentuale (1-100).
        Uso: !perc"""
        roll = random.randint(1, 100)

        embed = discord.Embed(title="🎯 Dado Percentuale", color=0x3498DB)
        embed.add_field(name="d100", value=f"**{roll}%**", inline=False)

        if roll <= 5:
            embed.set_footer(text="💀 Fallimento catastrofico!")
        elif roll >= 96:
            embed.set_footer(text="⭐ Successo spettacolare!")

        await ctx.send(embed=embed)

    # ── !ts (tiro salvezza) ──────────────────────────────
    @commands.command(aliases=["salvezza"])
    async def ts(self, ctx, mod: int = 0, cd: int = None):
        """Tiro salvezza con modificatore e CD opzionale.
        Uso: !ts 3   ·   !ts 5 15"""
        roll = random.randint(1, 20)
        total = roll + mod

        embed = discord.Embed(title="🛡️ Tiro Salvezza", color=0xE67E22)
        embed.add_field(name="d20", value=f"**{roll}**", inline=True)
        if mod:
            embed.add_field(name="Mod", value=f"{mod:+}", inline=True)
        embed.add_field(name="Totale", value=f"**{total}**", inline=True)

        if cd is not None:
            successo = total >= cd
            emoji = "✅ Successo!" if successo else "❌ Fallito!"
            embed.add_field(name=f"CD {cd}", value=emoji, inline=False)

        if roll == 20:
            embed.set_footer(text="⭐ 20 naturale — successo automatico!")
        elif roll == 1:
            embed.set_footer(text="💀 1 naturale — fallimento automatico!")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dice(bot))
