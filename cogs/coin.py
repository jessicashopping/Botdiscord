@bot.command()
async def coin(ctx):
    msg = await ctx.send("🪙 Lancio la moneta...")
    await asyncio.sleep(1.5)

    risultato = random.choice(["Testa", "Croce"])

    embed = discord.Embed(
        title="🪙 Lancio completato",
        description=f"È uscito: **{risultato}**",
        color=discord.Color.gold()
    )

    await msg.edit(content=None, embed=embed)
