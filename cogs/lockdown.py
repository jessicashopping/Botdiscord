"""
Lockdown System — Grimory Bot

Canali protetti: i messaggi di utenti non-bot vengono eliminati istantaneamente.
Solo i bot possono scrivere nei canali configurati.
Configurabile dal pannello !config → 🔒 Canali Protetti.
"""

import discord
from discord.ext import commands
from discord import ui
from utils import config_manager


class Lockdown(commands.Cog):
    """Protegge i canali — solo i bot possono scrivere."""

    def __init__(self, bot):
        self.bot = bot
        # Cache per velocizzare il check (evita di leggere il JSON ad ogni messaggio)
        self._cache: dict[int, set[int]] = {}  # guild_id -> set di channel_id

    def _get_locked(self, guild_id: int) -> set[int]:
        """Restituisce l'insieme dei canali bloccati (con cache)."""
        if guild_id not in self._cache:
            self.refresh_cache(guild_id)
        return self._cache.get(guild_id, set())

    def refresh_cache(self, guild_id: int):
        """Ricarica la cache dal config."""
        config = config_manager.get_guild_config(guild_id)
        raw = config.get("locked_channels", [])
        self._cache[guild_id] = {int(ch) for ch in raw}

    def is_locked(self, guild_id: int, channel_id: int) -> bool:
        return channel_id in self._get_locked(guild_id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignora DM
        if message.guild is None:
            return
        # I bot possono scrivere ovunque
        if message.author.bot:
            return
        # Controlla se il canale è protetto
        if not self.is_locked(message.guild.id, message.channel.id):
            return

        # Elimina il messaggio istantaneamente
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass  # già eliminato

    def get_config_view(self, ctx, parent_view=None):
        """Restituisce la view di configurazione (usata da config.py)."""
        return LockdownConfigView(ctx, parent_view)


# ═══════════════════════════════════════════════════════════
# CONFIG VIEW
# ═══════════════════════════════════════════════════════════

class LockdownConfigView(ui.View):
    """Pannello configurazione canali protetti."""

    def __init__(self, ctx, parent_view=None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(LockdownChannelAdd())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        locked = config.get("locked_channels", [])

        embed = discord.Embed(
            title="🔒 Canali Protetti",
            description=(
                "I canali protetti eliminano **istantaneamente** qualsiasi messaggio inviato da utenti.\n"
                "Solo i **bot** possono scrivere in questi canali.\n\n"
                "Perfetto per: canali regole, canali self-roles, canali annunci."
            ),
            color=0xE74C3C,
        )

        if locked:
            ch_list = "\n".join(f"🔒 <#{ch_id}>" for ch_id in locked)
            embed.add_field(name=f"Canali protetti ({len(locked)})", value=ch_list, inline=False)
        else:
            embed.add_field(name="Canali protetti", value="*Nessun canale protetto*", inline=False)

        embed.add_field(
            name="💡 Come funziona",
            value=(
                "• Aggiungi un canale con il menu a tendina sotto\n"
                "• Rimuovilo con il bottone 🔓 Sblocca\n"
                "• I messaggi dei bot vengono **sempre** mantenuti\n"
                "• Funziona anche contro l'owner del server"
            ),
            inline=False,
        )
        embed.set_footer(text="⚠️ Il bot necessita del permesso 'Gestisci Messaggi' per eliminare")
        return embed

    @ui.button(label="🔓 Sblocca Canale", style=discord.ButtonStyle.danger, row=1)
    async def unlock_channel(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        locked = config.get("locked_channels", [])

        if not locked:
            await interaction.response.send_message("⚠️ Non ci sono canali da sbloccare!", ephemeral=True)
            return

        view = UnlockSelectView(self.ctx, self, locked)
        await interaction.response.edit_message(view=view)

    @ui.button(label="🔒 Blocca Tutti i Self-Roles", style=discord.ButtonStyle.secondary, row=1)
    async def lock_selfroles(self, interaction: discord.Interaction, button: ui.Button):
        """Shortcut: blocca automaticamente il canale dei self-roles."""
        config = config_manager.get_guild_config(self.ctx.guild.id)
        sr_channel = config.get("selfroles_channel_id")

        if not sr_channel:
            await interaction.response.send_message("⚠️ Nessun canale self-roles configurato!", ephemeral=True)
            return

        locked = config.get("locked_channels", [])
        sr_channel = int(sr_channel)

        if sr_channel in locked:
            await interaction.response.send_message("ℹ️ Il canale self-roles è già protetto.", ephemeral=True)
            return

        locked.append(sr_channel)
        config_manager.update_guild_config(self.ctx.guild.id, locked_channels=locked)
        self._refresh_cog_cache()

        embed = self.build_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.secondary, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        if self.parent_view:
            embed = self.parent_view._build_main_embed()
            await interaction.response.edit_message(embed=embed, view=self.parent_view)
        else:
            await interaction.response.edit_message(view=None)

    def _refresh_cog_cache(self):
        """Aggiorna la cache del cog Lockdown."""
        cog = self.ctx.bot.get_cog("Lockdown")
        if cog:
            cog.refresh_cache(self.ctx.guild.id)


class LockdownChannelAdd(ui.ChannelSelect):
    """Dropdown per aggiungere un canale protetto."""

    def __init__(self):
        super().__init__(
            placeholder="➕ Seleziona un canale da proteggere…",
            channel_types=[discord.ChannelType.text],
            min_values=1, max_values=1, row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        config = config_manager.get_guild_config(interaction.guild.id)
        locked = config.get("locked_channels", [])

        if channel.id in locked:
            await interaction.response.send_message(
                f"ℹ️ {channel.mention} è già protetto.", ephemeral=True
            )
            return

        locked.append(channel.id)
        config_manager.update_guild_config(interaction.guild.id, locked_channels=locked)

        # Aggiorna cache
        cog = interaction.client.get_cog("Lockdown")
        if cog:
            cog.refresh_cache(interaction.guild.id)

        embed = self.view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.view)


class UnlockSelectView(ui.View):
    """Vista per scegliere quale canale sbloccare."""

    def __init__(self, ctx, parent_view, locked_channels):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.parent_view = parent_view

        options = []
        for ch_id in locked_channels:
            channel = ctx.guild.get_channel(int(ch_id))
            name = f"#{channel.name}" if channel else f"ID: {ch_id}"
            options.append(discord.SelectOption(
                label=name, value=str(ch_id), emoji="🔒",
            ))

        # Max 25 opzioni per un Select
        options = options[:25]

        select = ui.Select(
            placeholder="Seleziona il canale da sbloccare…",
            options=options, row=0,
        )
        select.callback = self._on_unlock
        self.add_item(select)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.ctx.author.id

    async def _on_unlock(self, interaction: discord.Interaction):
        ch_id = int(interaction.data["values"][0])
        config = config_manager.get_guild_config(self.ctx.guild.id)
        locked = config.get("locked_channels", [])

        if ch_id in locked:
            locked.remove(ch_id)
            config_manager.update_guild_config(self.ctx.guild.id, locked_channels=locked)

        # Aggiorna cache
        cog = interaction.client.get_cog("Lockdown")
        if cog:
            cog.refresh_cache(self.ctx.guild.id)

        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


async def setup(bot):
    await bot.add_cog(Lockdown(bot))
