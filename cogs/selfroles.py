"""
Self-Roles System — Grimory Bot

Permette agli utenti di scegliere ruoli tramite embed interattivi:
  🎨 Colori  — cambia il colore del tuo nome
  ⚔️ Classi  — scegli la tua classe D&D
  🔓 Sblocco — ottieni ruoli per accedere ad aree speciali

Gli admin configurano tutto dal pannello !config → Self Roles.
"""

import discord
from discord.ext import commands
from discord import ui
from utils import config_manager

# ═══════════════════════════════════════════════════════════
# DATI PRESET
# ═══════════════════════════════════════════════════════════

PRESET_COLORS = {
    "Rosso":     "e74c3c",
    "Blu":       "3498db",
    "Verde":     "2ecc71",
    "Oro":       "f1c40f",
    "Viola":     "9b59b6",
    "Arancione": "e67e22",
    "Rosa":      "e91e63",
    "Celeste":   "00bcd4",
    "Turchese":  "1abc9c",
    "Smeraldo":  "00c853",
    "Bianco":    "ecf0f1",
    "Grigio":    "95a5a6",
}

COLOR_EMOJIS = {
    "Rosso": "🔴", "Blu": "🔵", "Verde": "🟢", "Oro": "🟡",
    "Viola": "🟣", "Arancione": "🟠", "Rosa": "💗", "Celeste": "💎",
    "Turchese": "🌊", "Smeraldo": "💚", "Bianco": "⚪", "Grigio": "🩶",
}

DND_CLASSES = [
    "Barbaro", "Bardo", "Chierico", "Druido", "Guerriero", "Ladro",
    "Mago", "Monaco", "Paladino", "Ranger", "Stregone", "Warlock",
]

CLASS_EMOJIS = {
    "Barbaro": "🪓", "Bardo": "🎵", "Chierico": "✝️", "Druido": "🌿",
    "Guerriero": "⚔️", "Ladro": "🗡️", "Mago": "🔮", "Monaco": "☯️",
    "Paladino": "🛡️", "Ranger": "🏹", "Stregone": "🌀", "Warlock": "👁️",
}


# ═══════════════════════════════════════════════════════════
# VISTE PERSISTENTI (utenti — sopravvivono al riavvio)
# ═══════════════════════════════════════════════════════════

class PersistentColorView(ui.View):
    """Dropdown colori — registrata come view persistente."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PersistentColorSelect())


class PersistentColorSelect(ui.Select):
    def __init__(self):
        super().__init__(
            custom_id="grimory:color_select",
            placeholder="🎨 Scegli il tuo colore...",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="caricamento", value="0")],
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        guild = interaction.guild
        member = interaction.user
        config = config_manager.get_guild_config(guild.id)

        # Rimuovi tutti i color roles esistenti
        all_color_ids = {int(v["role_id"]) for v in config.get("color_roles", {}).values()}
        roles_to_remove = [r for r in member.roles if r.id in all_color_ids]
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        role = guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Ruolo non trovato.", ephemeral=True)
            return

        # Se aveva già questo colore → lo rimuove e basta
        if role in roles_to_remove:
            await interaction.response.send_message(f"🎨 Colore **{role.name}** rimosso!", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.send_message(f"🎨 Colore impostato: **{role.name}**!", ephemeral=True)


class PersistentClassView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PersistentClassSelect())


class PersistentClassSelect(ui.Select):
    def __init__(self):
        super().__init__(
            custom_id="grimory:class_select",
            placeholder="⚔️ Scegli la tua classe...",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="caricamento", value="0")],
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        guild = interaction.guild
        member = interaction.user
        config = config_manager.get_guild_config(guild.id)

        all_class_ids = {int(v["role_id"]) for v in config.get("class_roles", {}).values()}
        roles_to_remove = [r for r in member.roles if r.id in all_class_ids]
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        role = guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Ruolo non trovato.", ephemeral=True)
            return

        if role in roles_to_remove:
            await interaction.response.send_message(f"⚔️ Classe **{role.name}** rimossa!", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.send_message(f"⚔️ Classe impostata: **{role.name}**!", ephemeral=True)


class PersistentUnlockView(ui.View):
    """Bottoni per i ruoli di sblocco — persistente."""
    def __init__(self):
        super().__init__(timeout=None)


class PersistentUnlockButton(ui.Button):
    def __init__(self, role_id: int, label: str, emoji: str = None):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=label,
            emoji=emoji,
            custom_id=f"grimory:unlock:{role_id}",
        )
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Ruolo non trovato.", ephemeral=True)
            return

        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"🔓 Ruolo **{role.name}** rimosso!", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"🔓 Ruolo **{role.name}** ottenuto!", ephemeral=True)


# ═══════════════════════════════════════════════════════════
# VISTE CONFIG ADMIN — Pannello Self Roles
# ═══════════════════════════════════════════════════════════

class SelfRolesConfigView(ui.View):
    """Pannello principale configurazione self-roles."""

    def __init__(self, ctx, parent_view=None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(SelfRolesChannelSelect())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        ch = f"<#{config['selfroles_channel_id']}>" if config.get("selfroles_channel_id") else "⚠️ Non impostato"

        n_colors = len(config.get("color_roles", {}))
        n_classes = len(config.get("class_roles", {}))
        n_unlock = len(config.get("unlock_roles", {}))

        # Colori attivi
        color_names = list(config.get("color_roles", {}).keys())
        color_str = ", ".join(f"{COLOR_EMOJIS.get(c, '🎨')} {c}" for c in color_names[:8])
        if len(color_names) > 8:
            color_str += f" +{len(color_names) - 8} altri"
        if not color_str:
            color_str = "Nessuno"

        # Classi attive
        class_names = list(config.get("class_roles", {}).keys())
        class_str = ", ".join(f"{CLASS_EMOJIS.get(c, '⚔️')} {c}" for c in class_names[:8])
        if len(class_names) > 8:
            class_str += f" +{len(class_names) - 8} altri"
        if not class_str:
            class_str = "Nessuna"

        # Unlock
        unlock_names = list(config.get("unlock_roles", {}).keys())
        unlock_str = ", ".join(unlock_names[:6]) or "Nessuno"

        embed = discord.Embed(
            title="🎨 Configurazione Self Roles",
            description=(
                "Configura i ruoli che gli utenti possono assegnarsi da soli.\n"
                "Il bot creerà automaticamente i ruoli nel server."
            ),
            color=0xE91E63,
        )
        embed.add_field(name="📌 Canale", value=ch, inline=True)
        embed.add_field(name="📊 Totale", value=f"{n_colors} colori · {n_classes} classi · {n_unlock} sblocco", inline=True)
        embed.add_field(name="🎨 Colori attivi", value=color_str, inline=False)
        embed.add_field(name="⚔️ Classi attive", value=class_str, inline=False)
        embed.add_field(name="🔓 Ruoli sblocco", value=unlock_str, inline=False)
        embed.set_footer(text="Usa i bottoni sotto per modificare · Le modifiche sono salvate automaticamente")
        return embed

    @ui.button(label="🎨 Colori", style=discord.ButtonStyle.primary, row=0)
    async def manage_colors(self, interaction: discord.Interaction, button: ui.Button):
        view = ColorConfigView(self.ctx, self)
        embed = view.build_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="⚔️ Classi", style=discord.ButtonStyle.primary, row=0)
    async def manage_classes(self, interaction: discord.Interaction, button: ui.Button):
        view = ClassConfigView(self.ctx, self)
        embed = view.build_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="🔓 Sblocco", style=discord.ButtonStyle.primary, row=0)
    async def manage_unlock(self, interaction: discord.Interaction, button: ui.Button):
        view = UnlockConfigView(self.ctx, self)
        embed = view.build_embed()
        await interaction.response.edit_message(embed=embed, view=view)

    @ui.button(label="✏️ Testi Embed", style=discord.ButtonStyle.secondary, row=1)
    async def edit_texts(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        modal = EmbedTextsModal(self.ctx, self, config)
        await interaction.response.send_modal(modal)

    @ui.button(label="📨 Invia / Aggiorna Embed", style=discord.ButtonStyle.success, row=1)
    async def send_embeds(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        ch_id = config.get("selfroles_channel_id")
        if not ch_id:
            await interaction.response.send_message("⚠️ Imposta prima un canale!", ephemeral=True)
            return

        channel = self.ctx.guild.get_channel(int(ch_id))
        if not channel:
            await interaction.response.send_message("⚠️ Canale non trovato!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        cog = self.ctx.bot.get_cog("SelfRoles")
        if cog:
            await cog.send_role_embeds(self.ctx.guild, channel)

        await interaction.followup.send(f"✅ Embed inviati/aggiornati in {channel.mention}!", ephemeral=True)
        embed = self.build_embed()
        await interaction.message.edit(embed=embed, view=self)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        if self.parent_view:
            embed = self.parent_view._build_main_embed()
            await interaction.response.edit_message(embed=embed, view=self.parent_view)
        else:
            await interaction.response.edit_message(view=None)


class SelfRolesChannelSelect(ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="📌 Seleziona il canale per i self-roles…",
            channel_types=[discord.ChannelType.text],
            min_values=1, max_values=1, row=3,
        )

    async def callback(self, interaction: discord.Interaction):
        ch = self.values[0]
        config_manager.update_guild_config(interaction.guild.id, selfroles_channel_id=ch.id)
        embed = self.view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.view)


class EmbedTextsModal(ui.Modal, title="✏️ Modifica Testi Embed"):
    color_title = ui.TextInput(label="Titolo Embed Colori", max_length=100, row=0)
    color_desc  = ui.TextInput(label="Descrizione Embed Colori", style=discord.TextStyle.paragraph, max_length=300, row=1)
    class_title = ui.TextInput(label="Titolo Embed Classi", max_length=100, row=2)
    class_desc  = ui.TextInput(label="Descrizione Embed Classi", style=discord.TextStyle.paragraph, max_length=300, row=3)

    def __init__(self, ctx, parent_view, config):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view
        titles = config.get("selfroles_titles", {})
        descs = config.get("selfroles_descriptions", {})
        self.color_title.default = titles.get("color", "")
        self.color_desc.default = descs.get("color", "")
        self.class_title.default = titles.get("class", "")
        self.class_desc.default = descs.get("class", "")

    async def on_submit(self, interaction: discord.Interaction):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        titles = config.get("selfroles_titles", {})
        descs = config.get("selfroles_descriptions", {})
        titles["color"] = self.color_title.value
        titles["class"] = self.class_title.value
        descs["color"] = self.color_desc.value
        descs["class"] = self.class_desc.value
        config_manager.update_guild_config(
            self.ctx.guild.id,
            selfroles_titles=titles,
            selfroles_descriptions=descs,
        )
        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# CONFIG COLORI
# ═══════════════════════════════════════════════════════════

class ColorConfigView(ui.View):
    """Gestione dei colori con selezione multipla."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self._add_color_select()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def _add_color_select(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        enabled = set(config.get("color_roles", {}).keys())

        options = []
        for name, hex_code in PRESET_COLORS.items():
            emoji = COLOR_EMOJIS.get(name, "🎨")
            options.append(discord.SelectOption(
                label=name,
                value=name,
                emoji=emoji,
                description=f"#{hex_code.upper()}",
                default=(name in enabled),
            ))

        select = ui.Select(
            placeholder="Seleziona i colori da attivare…",
            options=options,
            min_values=0,
            max_values=len(options),
            row=0,
        )
        select.callback = self._on_select
        self.add_item(select)

    async def _on_select(self, interaction: discord.Interaction):
        selected = set(interaction.data.get("values", []))
        config = config_manager.get_guild_config(self.ctx.guild.id)
        current = config.get("color_roles", {})
        guild = interaction.guild

        await interaction.response.defer()

        # Aggiungi nuovi colori
        for name in selected:
            if name not in current:
                hex_code = PRESET_COLORS.get(name, "95a5a6")
                color = discord.Color(int(hex_code, 16))
                try:
                    role = await guild.create_role(
                        name=f"🎨 {name}",
                        color=color,
                        reason=f"Grimory Bot — Self Role colore: {name}",
                    )
                    current[name] = {"role_id": role.id, "hex": hex_code}
                except discord.Forbidden:
                    pass

        # Rimuovi colori deselezionati
        to_remove = [n for n in current if n not in selected and n in PRESET_COLORS]
        for name in to_remove:
            role_id = current[name].get("role_id")
            if role_id:
                role = guild.get_role(int(role_id))
                if role:
                    try:
                        await role.delete(reason="Grimory Bot — Colore rimosso dalla config")
                    except discord.Forbidden:
                        pass
            del current[name]

        config_manager.update_guild_config(guild.id, color_roles=current)

        # Ricostruisci la view con lo stato aggiornato
        new_view = ColorConfigView(self.ctx, self.parent_view)
        embed = new_view.build_embed()
        await interaction.message.edit(embed=embed, view=new_view)

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        enabled = config.get("color_roles", {})

        lines = []
        for name in PRESET_COLORS:
            emoji = COLOR_EMOJIS.get(name, "🎨")
            status = "✅" if name in enabled else "❌"
            lines.append(f"{emoji} {name} {status}")

        # Colori custom
        custom = [n for n in enabled if n not in PRESET_COLORS]
        if custom:
            lines.append("\n**Colori personalizzati:**")
            for name in custom:
                lines.append(f"🎨 {name} ✅")

        embed = discord.Embed(
            title="🎨 Gestione Colori",
            description="Seleziona i colori nel menu sotto. Il bot creerà/rimuoverà i ruoli automaticamente.",
            color=0xE91E63,
        )
        embed.add_field(name="Stato colori", value="\n".join(lines), inline=False)
        embed.set_footer(text="I ruoli vengono creati/eliminati automaticamente nel server")
        return embed

    @ui.button(label="➕ Colore Personalizzato", style=discord.ButtonStyle.primary, row=1)
    async def add_custom(self, interaction: discord.Interaction, button: ui.Button):
        modal = CustomColorModal(self.ctx, self)
        await interaction.response.send_modal(modal)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class CustomColorModal(ui.Modal, title="➕ Aggiungi Colore Personalizzato"):
    name_input = ui.TextInput(label="Nome del colore", placeholder="es. Indaco", max_length=30, row=0)
    hex_input = ui.TextInput(label="Codice HEX (senza #)", placeholder="es. 4B0082", max_length=6, min_length=6, row=1)

    def __init__(self, ctx, parent_view):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name_input.value.strip()
        hex_code = self.hex_input.value.strip().replace("#", "")

        try:
            color_int = int(hex_code, 16)
        except ValueError:
            await interaction.response.send_message("⚠️ Codice HEX non valido!", ephemeral=True)
            return

        guild = interaction.guild
        config = config_manager.get_guild_config(guild.id)
        current = config.get("color_roles", {})

        if name in current:
            await interaction.response.send_message(f"⚠️ Il colore '{name}' esiste già!", ephemeral=True)
            return

        await interaction.response.defer()

        try:
            role = await guild.create_role(
                name=f"🎨 {name}",
                color=discord.Color(color_int),
                reason=f"Grimory Bot — Colore personalizzato: {name}",
            )
            current[name] = {"role_id": role.id, "hex": hex_code}
            config_manager.update_guild_config(guild.id, color_roles=current)
        except discord.Forbidden:
            await interaction.followup.send("⚠️ Non ho i permessi per creare ruoli!", ephemeral=True)
            return

        new_view = ColorConfigView(self.ctx, self.parent_view.parent_view)
        embed = new_view.build_embed()
        await interaction.message.edit(embed=embed, view=new_view)


# ═══════════════════════════════════════════════════════════
# CONFIG CLASSI
# ═══════════════════════════════════════════════════════════

class ClassConfigView(ui.View):
    """Gestione delle classi D&D."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self._add_class_select()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def _add_class_select(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        enabled = set(config.get("class_roles", {}).keys())

        options = []
        for name in DND_CLASSES:
            emoji = CLASS_EMOJIS.get(name, "⚔️")
            options.append(discord.SelectOption(
                label=name,
                value=name,
                emoji=emoji,
                default=(name in enabled),
            ))

        select = ui.Select(
            placeholder="Seleziona le classi da attivare…",
            options=options,
            min_values=0,
            max_values=len(options),
            row=0,
        )
        select.callback = self._on_select
        self.add_item(select)

    async def _on_select(self, interaction: discord.Interaction):
        selected = set(interaction.data.get("values", []))
        config = config_manager.get_guild_config(self.ctx.guild.id)
        current = config.get("class_roles", {})
        guild = interaction.guild

        await interaction.response.defer()

        for name in selected:
            if name not in current:
                emoji = CLASS_EMOJIS.get(name, "⚔️")
                try:
                    role = await guild.create_role(
                        name=f"{emoji} {name}",
                        reason=f"Grimory Bot — Self Role classe: {name}",
                    )
                    current[name] = {"role_id": role.id}
                except discord.Forbidden:
                    pass

        to_remove = [n for n in current if n not in selected]
        for name in to_remove:
            role_id = current[name].get("role_id")
            if role_id:
                role = guild.get_role(int(role_id))
                if role:
                    try:
                        await role.delete(reason="Grimory Bot — Classe rimossa dalla config")
                    except discord.Forbidden:
                        pass
            del current[name]

        config_manager.update_guild_config(guild.id, class_roles=current)

        new_view = ClassConfigView(self.ctx, self.parent_view)
        embed = new_view.build_embed()
        await interaction.message.edit(embed=embed, view=new_view)

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        enabled = config.get("class_roles", {})

        lines = []
        for name in DND_CLASSES:
            emoji = CLASS_EMOJIS.get(name, "⚔️")
            status = "✅" if name in enabled else "❌"
            lines.append(f"{emoji} {name} {status}")

        embed = discord.Embed(
            title="⚔️ Gestione Classi D&D",
            description="Seleziona le classi nel menu sotto. Il bot creerà/rimuoverà i ruoli automaticamente.",
            color=0xE67E22,
        )
        embed.add_field(name="Stato classi", value="\n".join(lines), inline=False)
        embed.set_footer(text="I ruoli vengono creati/eliminati automaticamente nel server")
        return embed

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=1)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# CONFIG RUOLI SBLOCCO
# ═══════════════════════════════════════════════════════════

class UnlockConfigView(ui.View):
    """Gestione dei ruoli di sblocco."""

    def __init__(self, ctx, parent_view):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.parent_view = parent_view
        self.add_item(UnlockRoleAddSelect())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Solo chi ha aperto il pannello può usarlo.", ephemeral=True)
            return False
        return True

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        unlock = config.get("unlock_roles", {})

        embed = discord.Embed(
            title="🔓 Gestione Ruoli Sblocco",
            description=(
                "Questi ruoli permettono agli utenti di sbloccare aree del server.\n"
                "**Aggiungi:** seleziona un ruolo esistente dal menu a tendina sotto.\n"
                "**Rimuovi:** usa il bottone 🗑️."
            ),
            color=0x9B59B6,
        )

        if unlock:
            lines = []
            for name, data in unlock.items():
                emoji = data.get("emoji", "🔓")
                desc = data.get("description", "")
                role_id = data.get("role_id")
                lines.append(f"{emoji} **{name}** (<@&{role_id}>)\n  ↳ {desc or 'Nessuna descrizione'}")
            embed.add_field(name="Ruoli configurati", value="\n".join(lines), inline=False)
        else:
            embed.add_field(name="Ruoli configurati", value="*Nessun ruolo aggiunto*", inline=False)

        embed.set_footer(text="Seleziona un ruolo dal menu per aggiungerlo · I ruoli devono già esistere nel server")
        return embed

    @ui.button(label="✏️ Modifica Descrizioni", style=discord.ButtonStyle.primary, row=1)
    async def edit_descriptions(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        unlock = config.get("unlock_roles", {})
        if not unlock:
            await interaction.response.send_message("⚠️ Aggiungi prima un ruolo!", ephemeral=True)
            return
        # Mostra dropdown per scegliere quale modificare
        view = UnlockEditSelectView(self.ctx, self, unlock)
        await interaction.response.edit_message(view=view)

    @ui.button(label="🗑️ Rimuovi Ruolo", style=discord.ButtonStyle.danger, row=1)
    async def remove_role(self, interaction: discord.Interaction, button: ui.Button):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        unlock = config.get("unlock_roles", {})
        if not unlock:
            await interaction.response.send_message("⚠️ Non ci sono ruoli da rimuovere!", ephemeral=True)
            return
        view = UnlockRemoveView(self.ctx, self, unlock)
        await interaction.response.edit_message(view=view)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.secondary, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class UnlockRoleAddSelect(ui.RoleSelect):
    """Dropdown per aggiungere un ruolo di sblocco."""
    def __init__(self):
        super().__init__(
            placeholder="➕ Seleziona un ruolo da aggiungere…",
            min_values=1, max_values=1, row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        role = self.values[0]
        config = config_manager.get_guild_config(interaction.guild.id)
        unlock = config.get("unlock_roles", {})

        # Controlla se esiste già
        for data in unlock.values():
            if int(data["role_id"]) == role.id:
                await interaction.response.send_message(f"⚠️ Il ruolo {role.mention} è già configurato!", ephemeral=True)
                return

        if len(unlock) >= 20:
            await interaction.response.send_message("⚠️ Massimo 20 ruoli di sblocco!", ephemeral=True)
            return

        # Apri modal per descrizione
        modal = UnlockDescriptionModal(interaction.guild.id, role, self.view)
        await interaction.response.send_modal(modal)


class UnlockDescriptionModal(ui.Modal, title="🔓 Configura Ruolo Sblocco"):
    desc_input = ui.TextInput(
        label="Descrizione (opzionale)",
        placeholder="es. Sblocca il canale #quest-avanzate",
        required=False, max_length=100, row=0,
    )
    emoji_input = ui.TextInput(
        label="Emoji (opzionale)",
        placeholder="es. ⚔️ 🏰 🎮",
        required=False, max_length=5, row=1,
    )

    def __init__(self, guild_id, role, parent_view):
        super().__init__()
        self.guild_id = guild_id
        self.role = role
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        config = config_manager.get_guild_config(self.guild_id)
        unlock = config.get("unlock_roles", {})

        unlock[self.role.name] = {
            "role_id": self.role.id,
            "description": self.desc_input.value or "",
            "emoji": self.emoji_input.value.strip() or "🔓",
        }
        config_manager.update_guild_config(self.guild_id, unlock_roles=unlock)

        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class UnlockRemoveView(ui.View):
    """Vista per rimuovere un ruolo di sblocco."""
    def __init__(self, ctx, parent_view, unlock_roles):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.parent_view = parent_view

        options = [
            discord.SelectOption(label=name, value=name, emoji=data.get("emoji", "🔓"))
            for name, data in unlock_roles.items()
        ]
        select = ui.Select(placeholder="Seleziona il ruolo da rimuovere…", options=options, row=0)
        select.callback = self._on_remove
        self.add_item(select)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.ctx.author.id

    async def _on_remove(self, interaction: discord.Interaction):
        name = interaction.data["values"][0]
        config = config_manager.get_guild_config(self.ctx.guild.id)
        unlock = config.get("unlock_roles", {})
        if name in unlock:
            del unlock[name]
            config_manager.update_guild_config(self.ctx.guild.id, unlock_roles=unlock)

        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class UnlockEditSelectView(ui.View):
    """Vista per scegliere quale ruolo sblocco modificare."""
    def __init__(self, ctx, parent_view, unlock_roles):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.parent_view = parent_view

        options = [
            discord.SelectOption(label=name, value=name, emoji=data.get("emoji", "🔓"))
            for name, data in unlock_roles.items()
        ]
        select = ui.Select(placeholder="Seleziona il ruolo da modificare…", options=options, row=0)
        select.callback = self._on_select
        self.add_item(select)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.ctx.author.id

    async def _on_select(self, interaction: discord.Interaction):
        name = interaction.data["values"][0]
        config = config_manager.get_guild_config(self.ctx.guild.id)
        unlock = config.get("unlock_roles", {})
        data = unlock.get(name, {})

        modal = UnlockEditModal(self.ctx.guild.id, name, data, self.parent_view)
        await interaction.response.send_modal(modal)


class UnlockEditModal(ui.Modal, title="✏️ Modifica Ruolo Sblocco"):
    desc_input = ui.TextInput(label="Descrizione", required=False, max_length=100, row=0)
    emoji_input = ui.TextInput(label="Emoji", required=False, max_length=5, row=1)

    def __init__(self, guild_id, role_name, data, parent_view):
        super().__init__()
        self.guild_id = guild_id
        self.role_name = role_name
        self.parent_view = parent_view
        self.desc_input.default = data.get("description", "")
        self.emoji_input.default = data.get("emoji", "🔓")

    async def on_submit(self, interaction: discord.Interaction):
        config = config_manager.get_guild_config(self.guild_id)
        unlock = config.get("unlock_roles", {})
        if self.role_name in unlock:
            unlock[self.role_name]["description"] = self.desc_input.value or ""
            unlock[self.role_name]["emoji"] = self.emoji_input.value.strip() or "🔓"
            config_manager.update_guild_config(self.guild_id, unlock_roles=unlock)

        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


# ═══════════════════════════════════════════════════════════
# COG PRINCIPALE
# ═══════════════════════════════════════════════════════════

class SelfRoles(commands.Cog):
    """Sistema self-roles — gli utenti si assegnano ruoli da soli."""

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Registra le view persistenti al caricamento del cog."""
        # View template persistenti — il custom_id fa il match con i messaggi inviati
        self.bot.add_view(PersistentColorView())
        self.bot.add_view(PersistentClassView())

        # Registra view persistenti per i bottoni unlock di tutti i server
        all_configs = config_manager.load_all()
        for guild_id, config in all_configs.items():
            unlock = config.get("unlock_roles", {})
            if unlock:
                view = PersistentUnlockView()
                for name, data in unlock.items():
                    role_id = int(data["role_id"])
                    emoji = data.get("emoji", "🔓")
                    view.add_item(PersistentUnlockButton(role_id, name, emoji))
                self.bot.add_view(view)

    def get_config_view(self, ctx, parent_view=None):
        """Restituisce la view di configurazione (usata da config.py)."""
        return SelfRolesConfigView(ctx, parent_view)

    async def send_role_embeds(self, guild: discord.Guild, channel: discord.TextChannel):
        """Invia o aggiorna i 3 embed di selezione ruoli."""
        config = config_manager.get_guild_config(guild.id)
        titles = config.get("selfroles_titles", {})
        descs = config.get("selfroles_descriptions", {})
        message_ids = config.get("selfroles_message_ids", {})

        # ── EMBED COLORI ─────────────────────────────────
        color_roles = config.get("color_roles", {})
        if color_roles:
            options = []
            for name, data in color_roles.items():
                emoji = COLOR_EMOJIS.get(name, "🎨")
                options.append(discord.SelectOption(
                    label=name, value=str(data["role_id"]),
                    emoji=emoji, description=f"Colore: #{data.get('hex', '000000').upper()}",
                ))

            view = PersistentColorView()
            view.clear_items()
            select = PersistentColorSelect()
            select.options = options
            view.add_item(select)

            embed = discord.Embed(
                title=titles.get("color", "🎨 Scegli il tuo Colore"),
                description=descs.get("color", "Seleziona un colore per il tuo nome!"),
                color=0xE91E63,
            )
            color_preview = "  ".join(f"{COLOR_EMOJIS.get(n, '🎨')} {n}" for n in color_roles)
            embed.add_field(name="Colori disponibili", value=color_preview, inline=False)
            embed.set_footer(text="Seleziona di nuovo lo stesso colore per rimuoverlo")

            msg_id = message_ids.get("color")
            msg = await self._send_or_edit(channel, msg_id, embed=embed, view=view)
            message_ids["color"] = msg.id

        # ── EMBED CLASSI ─────────────────────────────────
        class_roles = config.get("class_roles", {})
        if class_roles:
            options = []
            for name, data in class_roles.items():
                emoji = CLASS_EMOJIS.get(name, "⚔️")
                options.append(discord.SelectOption(
                    label=name, value=str(data["role_id"]), emoji=emoji,
                ))

            view = PersistentClassView()
            view.clear_items()
            select = PersistentClassSelect()
            select.options = options
            view.add_item(select)

            embed = discord.Embed(
                title=titles.get("class", "⚔️ Scegli la tua Classe"),
                description=descs.get("class", "Scegli la classe del tuo personaggio!"),
                color=0xE67E22,
            )
            class_preview = "  ".join(f"{CLASS_EMOJIS.get(n, '⚔️')} {n}" for n in class_roles)
            embed.add_field(name="Classi disponibili", value=class_preview, inline=False)
            embed.set_footer(text="Seleziona di nuovo la stessa classe per rimuoverla")

            msg_id = message_ids.get("class")
            msg = await self._send_or_edit(channel, msg_id, embed=embed, view=view)
            message_ids["class"] = msg.id

        # ── EMBED UNLOCK ─────────────────────────────────
        unlock_roles = config.get("unlock_roles", {})
        if unlock_roles:
            view = PersistentUnlockView()
            for name, data in unlock_roles.items():
                role_id = int(data["role_id"])
                emoji = data.get("emoji", "🔓")
                view.add_item(PersistentUnlockButton(role_id, name, emoji))

            embed = discord.Embed(
                title=titles.get("unlock", "🔓 Ruoli Speciali"),
                description=descs.get("unlock", "Clicca per ottenere o rimuovere un ruolo!"),
                color=0x9B59B6,
            )
            for name, data in unlock_roles.items():
                emoji = data.get("emoji", "🔓")
                desc = data.get("description", "")
                embed.add_field(
                    name=f"{emoji} {name}",
                    value=desc or "Clicca il bottone per ottenere questo ruolo",
                    inline=True,
                )
            embed.set_footer(text="Clicca di nuovo per rimuovere il ruolo")

            msg_id = message_ids.get("unlock")
            msg = await self._send_or_edit(channel, msg_id, embed=embed, view=view)
            message_ids["unlock"] = msg.id

        # Salva gli ID dei messaggi
        config_manager.update_guild_config(guild.id, selfroles_message_ids=message_ids)

    async def _send_or_edit(self, channel, message_id, **kwargs):
        """Modifica il messaggio esistente o ne invia uno nuovo."""
        if message_id:
            try:
                msg = await channel.fetch_message(int(message_id))
                await msg.edit(**kwargs)
                return msg
            except (discord.NotFound, discord.HTTPException):
                pass
        return await channel.send(**kwargs)

    @commands.command(aliases=["ruoli"])
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx):
        """Apre il pannello di configurazione dei self-roles (admin)."""
        view = SelfRolesConfigView(ctx)
        embed = view.build_embed()
        await ctx.send(embed=embed, view=view)

    @roles.error
    async def roles_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Solo gli **amministratori** possono configurare i ruoli.")


async def setup(bot):
    await bot.add_cog(SelfRoles(bot))
