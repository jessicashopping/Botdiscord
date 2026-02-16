import discord
from discord.ext import commands
from discord import ui
from utils import config_manager


# ═══════════════════════════════════════════════════════════
# PANNELLO PRINCIPALE
# ═══════════════════════════════════════════════════════════

class ConfigMainView(ui.View):
    """Pannello principale di configurazione con bottoni per ogni sezione."""

    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=300)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True
            )
            return False
        return True

    def _build_main_embed(self) -> discord.Embed:
        config = config_manager.get_guild_config(self.ctx.guild.id)

        welcome_status = "✅ Attivo" if config["welcome_enabled"] else "❌ Disattivato"
        goodbye_status = "✅ Attivo" if config["goodbye_enabled"] else "❌ Disattivato"
        fun_status = "✅ Attivo" if config["fun_replies_enabled"] else "❌ Disattivato"

        welcome_ch = f"<#{config['welcome_channel_id']}>" if config["welcome_channel_id"] else "Non impostato"
        goodbye_ch = f"<#{config['goodbye_channel_id']}>" if config["goodbye_channel_id"] else "Non impostato"
        auto_role = f"<@&{config['auto_role_id']}>" if config.get("auto_role_id") else "Nessuno"

        # Self roles stats
        n_colors = len(config.get("color_roles", {}))
        n_classes = len(config.get("class_roles", {}))
        n_unlock = len(config.get("unlock_roles", {}))
        sr_ch = f"<#{config['selfroles_channel_id']}>" if config.get("selfroles_channel_id") else "Non impostato"

        embed = discord.Embed(
            title="⚙️ Pannello di Configurazione — Grimory Bot",
            description="Usa i bottoni qui sotto per configurare il bot.\nSolo gli **amministratori** possono modificare le impostazioni.",
            color=0x8B4513,
        )
        embed.add_field(
            name="👋 Benvenuto",
            value=(
                f"**Stato:** {welcome_status}\n"
                f"**Canale:** {welcome_ch}\n"
                f"**Formato:** {'Embed' if config['welcome_embed'] else 'Testo semplice'}"
            ),
            inline=True,
        )
        embed.add_field(
            name="🚪 Addio",
            value=(
                f"**Stato:** {goodbye_status}\n"
                f"**Canale:** {goodbye_ch}"
            ),
            inline=True,
        )
        staff_display = f"<@&{config['staff_role_id']}>" if config.get("staff_role_id") else "Solo Admin"

        embed.add_field(
            name="🎭 Altro",
            value=(
                f"**Risposte divertenti:** {fun_status} ({config['fun_replies_chance']}%)\n"
                f"**Auto-ruolo:** {auto_role}\n"
                f"**Ruolo Staff:** {staff_display}"
            ),
            inline=True,
        )
        embed.add_field(
            name="🎨 Self Roles",
            value=(
                f"**Canale:** {sr_ch}\n"
                f"**Colori:** {n_colors} · **Classi:** {n_classes} · **Sblocco:** {n_unlock}"
            ),
            inline=False,
        )
        embed.set_footer(text="Le impostazioni vengono salvate automaticamente.")
        return embed

    @ui.button(label="👋 Benvenuto", style=discord.ButtonStyle.primary, row=0)
    async def welcome_settings(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        view = WelcomeSettingsView(self.ctx, self)
        embed = view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="🚪 Addio", style=discord.ButtonStyle.primary, row=0)
    async def goodbye_settings(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        view = GoodbyeSettingsView(self.ctx, self)
        embed = view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="🎭 Risposte & Ruoli", style=discord.ButtonStyle.primary, row=0)
    async def fun_settings(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        view = FunSettingsView(self.ctx, self)
        embed = view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="🎨 Self Roles", style=discord.ButtonStyle.primary, row=1)
    async def selfroles_settings(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.ctx.bot.get_cog("SelfRoles")
        if cog is None:
            await interaction.response.send_message(
                "⚠️ Il modulo Self Roles non è caricato.\n"
                "Assicurati che `cogs/selfroles.py` sia presente nel progetto.",
                ephemeral=True,
            )
            return
        view = cog.get_config_view(self.ctx, self)
        embed = view.build_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="📋 Riepilogo", style=discord.ButtonStyle.secondary, row=2)
    async def show_config(self, interaction: discord.Interaction, button: ui.Button):
        embed = self._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="🔄 Reset", style=discord.ButtonStyle.danger, row=2)
    async def reset_config(self, interaction: discord.Interaction, button: ui.Button):
        view = ConfirmResetView(self.ctx, self)
        embed = discord.Embed(
            title="⚠️ Conferma Reset",
            description="Sei sicuro di voler ripristinare **tutte** le impostazioni ai valori predefiniti?",
            color=0xE74C3C,
        )
        await interaction.response.edit_message(embed=embed, view=view)


# ═══════════════════════════════════════════════════════════
# SEZIONE BENVENUTO
# ═══════════════════════════════════════════════════════════

class WelcomeChannelSelect(ui.ChannelSelect):
    """Dropdown per selezionare il canale di benvenuto."""

    def __init__(self):
        super().__init__(
            placeholder="Seleziona il canale di benvenuto…",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        config_manager.update_guild_config(
            interaction.guild.id, welcome_channel_id=channel.id
        )
        config = config_manager.get_guild_config(interaction.guild.id)
        embed = self.view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.view)


class WelcomeSettingsView(ui.View):
    """Impostazioni benvenuto."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(WelcomeChannelSelect())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self, config):
        status = "✅ Attivo" if config["welcome_enabled"] else "❌ Disattivato"
        ch = f"<#{config['welcome_channel_id']}>" if config["welcome_channel_id"] else "⚠️ Non impostato"
        fmt = "Embed" if config["welcome_embed"] else "Testo semplice"

        embed = discord.Embed(
            title="👋 Impostazioni Benvenuto",
            color=0x2ECC71,
        )
        embed.add_field(name="Stato", value=status, inline=True)
        embed.add_field(name="Canale", value=ch, inline=True)
        embed.add_field(name="Formato", value=fmt, inline=True)
        embed.add_field(
            name="📝 Messaggio attuale",
            value=f"```{config['welcome_message'][:500]}```",
            inline=False,
        )
        embed.add_field(
            name="💡 Placeholder disponibili",
            value="`{member}` = menzione · `{name}` = nome · `{server}` = server · `{count}` = n° membri",
            inline=False,
        )
        embed.set_footer(text="Usa il menu a tendina per scegliere il canale, i bottoni per le altre opzioni.")
        return embed

    @ui.button(label="Attiva/Disattiva", style=discord.ButtonStyle.success, row=0)
    async def toggle_welcome(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        new_state = not config["welcome_enabled"]
        config_manager.update_guild_config(self.ctx.guild.id, welcome_enabled=new_state)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="Embed / Testo", style=discord.ButtonStyle.secondary, row=0)
    async def toggle_embed(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        new_state = not config["welcome_embed"]
        config_manager.update_guild_config(self.ctx.guild.id, welcome_embed=new_state)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="✏️ Modifica Messaggio", style=discord.ButtonStyle.primary, row=0)
    async def edit_message(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        modal = WelcomeMessageModal(self.ctx, self, config["welcome_message"])
        await interaction.response.send_modal(modal)

    @ui.button(label="🧪 Testa", style=discord.ButtonStyle.secondary, row=0)
    async def test_welcome(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        ch_id = config["welcome_channel_id"]
        if not ch_id:
            await interaction.response.send_message("⚠️ Imposta prima un canale!", ephemeral=True)
            return

        channel = interaction.guild.get_channel(int(ch_id))
        if not channel:
            await interaction.response.send_message("⚠️ Canale non trovato!", ephemeral=True)
            return

        member = interaction.user
        msg = config["welcome_message"].format(
            member=member.mention,
            name=member.display_name,
            server=member.guild.name,
            count=member.guild.member_count,
        )

        if config["welcome_embed"]:
            color = int(config.get("welcome_color", "8B4513"), 16)
            test_embed = discord.Embed(
                title="⚔️ Un nuovo avventuriero è arrivato!",
                description=msg,
                color=color,
            )
            test_embed.set_thumbnail(url=member.display_avatar.url)
            test_embed.add_field(name="📊 Membro n°", value=f"**#{member.guild.member_count}**", inline=True)
            test_embed.set_footer(text=f"⚠️ MESSAGGIO DI TEST — Benvenuto su {member.guild.name}!")
            await channel.send(embed=test_embed)
        else:
            await channel.send(f"⚠️ **[TEST]** {msg}")

        await interaction.response.send_message(f"✅ Messaggio di test inviato in {channel.mention}!", ephemeral=True)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class WelcomeMessageModal(ui.Modal, title="✏️ Modifica Messaggio di Benvenuto"):
    """Modal per modificare il messaggio di benvenuto."""

    message_input = ui.TextInput(
        label="Messaggio di benvenuto",
        style=discord.TextStyle.paragraph,
        placeholder="Benvenuto {member}! Usa {name}, {server}, {count}...",
        max_length=1000,
        row=0,
    )

    def __init__(self, ctx, parent_view, current_message):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view
        self.message_input.default = current_message

    async def on_submit(self, interaction: discord.Interaction):
        config_manager.update_guild_config(
            self.ctx.guild.id, welcome_message=self.message_input.value
        )
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.parent_view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# SEZIONE ADDIO
# ═══════════════════════════════════════════════════════════

class GoodbyeChannelSelect(ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Seleziona il canale per gli addii…",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]
        config_manager.update_guild_config(
            interaction.guild.id, goodbye_channel_id=channel.id
        )
        config = config_manager.get_guild_config(interaction.guild.id)
        embed = self.view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.view)


class GoodbyeSettingsView(ui.View):
    """Impostazioni messaggio di addio."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(GoodbyeChannelSelect())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self, config):
        status = "✅ Attivo" if config["goodbye_enabled"] else "❌ Disattivato"
        ch = f"<#{config['goodbye_channel_id']}>" if config["goodbye_channel_id"] else "⚠️ Non impostato"

        embed = discord.Embed(title="🚪 Impostazioni Addio", color=0x95A5A6)
        embed.add_field(name="Stato", value=status, inline=True)
        embed.add_field(name="Canale", value=ch, inline=True)
        embed.add_field(
            name="📝 Messaggio attuale",
            value=f"```{config['goodbye_message'][:500]}```",
            inline=False,
        )
        embed.add_field(
            name="💡 Placeholder",
            value="`{member}` = menzione · `{name}` = nome · `{server}` = server",
            inline=False,
        )
        return embed

    @ui.button(label="Attiva/Disattiva", style=discord.ButtonStyle.success, row=0)
    async def toggle_goodbye(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        new_state = not config["goodbye_enabled"]
        config_manager.update_guild_config(self.ctx.guild.id, goodbye_enabled=new_state)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="✏️ Modifica Messaggio", style=discord.ButtonStyle.primary, row=0)
    async def edit_message(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        modal = GoodbyeMessageModal(self.ctx, self, config["goodbye_message"])
        await interaction.response.send_modal(modal)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class GoodbyeMessageModal(ui.Modal, title="✏️ Modifica Messaggio di Addio"):
    message_input = ui.TextInput(
        label="Messaggio di addio",
        style=discord.TextStyle.paragraph,
        placeholder="{member} ha lasciato la taverna...",
        max_length=1000,
        row=0,
    )

    def __init__(self, ctx, parent_view, current_message):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view
        self.message_input.default = current_message

    async def on_submit(self, interaction: discord.Interaction):
        config_manager.update_guild_config(
            self.ctx.guild.id, goodbye_message=self.message_input.value
        )
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.parent_view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# SEZIONE RISPOSTE DIVERTENTI & RUOLI
# ═══════════════════════════════════════════════════════════

class AutoRoleSelect(ui.RoleSelect):
    def __init__(self):
        super().__init__(
            placeholder="Seleziona il ruolo automatico per i nuovi membri…",
            min_values=0,
            max_values=1,
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = self.values[0].id if self.values else None
        config_manager.update_guild_config(interaction.guild.id, auto_role_id=role_id)
        config = config_manager.get_guild_config(interaction.guild.id)
        embed = self.view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.view)


class StaffRoleSelect(ui.RoleSelect):
    def __init__(self):
        super().__init__(
            placeholder="Seleziona il ruolo Staff (può usare !config)…",
            min_values=0,
            max_values=1,
            row=2,
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = self.values[0].id if self.values else None
        config_manager.update_guild_config(interaction.guild.id, staff_role_id=role_id)
        config = config_manager.get_guild_config(interaction.guild.id)
        embed = self.view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.view)


class FunSettingsView(ui.View):
    """Impostazioni risposte divertenti, auto-ruolo e ruolo staff."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(AutoRoleSelect())
        self.add_item(StaffRoleSelect())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self, config):
        fun_status = "✅ Attivo" if config["fun_replies_enabled"] else "❌ Disattivato"
        auto_role = f"<@&{config['auto_role_id']}>" if config.get("auto_role_id") else "Nessuno"
        staff_role = f"<@&{config['staff_role_id']}>" if config.get("staff_role_id") else "Solo Admin"
        chance = config.get("fun_replies_chance", 20)

        embed = discord.Embed(title="🎭 Risposte, Ruoli & Staff", color=0x9B59B6)
        embed.add_field(name="Risposte divertenti", value=fun_status, inline=True)
        embed.add_field(name="Probabilità saluti", value=f"{chance}%", inline=True)
        embed.add_field(name="Auto-ruolo", value=auto_role, inline=True)
        embed.add_field(name="👑 Ruolo Staff", value=staff_role, inline=True)
        embed.add_field(
            name="ℹ️ Info",
            value=(
                "**Risposte divertenti:** il bot reagisce alle parolacce con risposte a tema D&D "
                "e saluta i nuovi messaggi con una probabilità configurabile.\n"
                "**Auto-ruolo:** assegna automaticamente un ruolo a chi entra nel server.\n"
                "**Ruolo Staff:** chi ha questo ruolo può usare `!config` e `!roles` anche senza essere Admin."
            ),
            inline=False,
        )
        return embed

    @ui.button(label="Attiva/Disattiva Risposte", style=discord.ButtonStyle.success, row=0)
    async def toggle_fun(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        new_state = not config["fun_replies_enabled"]
        config_manager.update_guild_config(self.ctx.guild.id, fun_replies_enabled=new_state)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="📊 Cambia Probabilità", style=discord.ButtonStyle.primary, row=0)
    async def change_chance(self, interaction: discord.Interaction, button: ui.Button):
        modal = ChanceModal(self.ctx, self)
        await interaction.response.send_modal(modal)

    @ui.button(label="🗑️ Rimuovi Auto-ruolo", style=discord.ButtonStyle.secondary, row=0)
    async def remove_autorole(self, interaction: discord.Interaction, button: ui.Button):
        config_manager.update_guild_config(self.ctx.guild.id, auto_role_id=None)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class ChanceModal(ui.Modal, title="📊 Probabilità Risposte Saluto"):
    chance_input = ui.TextInput(
        label="Probabilità (0-100)",
        placeholder="20",
        max_length=3,
        row=0,
    )

    def __init__(self, ctx, parent_view):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            value = int(self.chance_input.value)
            value = max(0, min(100, value))
        except ValueError:
            await interaction.response.send_message("⚠️ Inserisci un numero tra 0 e 100.", ephemeral=True)
            return

        config_manager.update_guild_config(self.ctx.guild.id, fun_replies_chance=value)
        config = config_manager.get_guild_config(self.ctx.guild.id)
        embed = self.parent_view.build_embed(config)
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# CONFERMA RESET
# ═══════════════════════════════════════════════════════════

class ConfirmResetView(ui.View):
    def __init__(self, ctx, parent_view):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.parent_view = parent_view

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    @ui.button(label="✅ Sì, resetta tutto", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):
        config_manager.reset_guild_config(self.ctx.guild.id)
        embed = self.parent_view._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)

    @ui.button(label="❌ Annulla", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view._build_main_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# COG PRINCIPALE
# ═══════════════════════════════════════════════════════════

def _is_staff(ctx: commands.Context) -> bool:
    """Controlla se l'utente è admin o ha il ruolo staff configurato."""
    if ctx.author.guild_permissions.administrator:
        return True
    config = config_manager.get_guild_config(ctx.guild.id)
    staff_role_id = config.get("staff_role_id")
    if staff_role_id:
        return any(r.id == int(staff_role_id) for r in ctx.author.roles)
    return False


class Config(commands.Cog):
    """Pannello di configurazione interattivo del bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["settings", "setup", "impostazioni", "pannello"])
    async def config(self, ctx):
        """Apre il pannello di configurazione del bot.
        Accessibile ad admin e staff."""
        if not _is_staff(ctx):
            await ctx.send("❌ Solo gli **amministratori** o lo **staff** possono accedere alla configurazione.")
            return
        view = ConfigMainView(ctx)
        embed = view._build_main_embed()
        await ctx.send(embed=embed, view=view)

    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Solo gli **amministratori** o lo **staff** possono accedere alla configurazione.")


async def setup(bot):
    await bot.add_cog(Config(bot))
