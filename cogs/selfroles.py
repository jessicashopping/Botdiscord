"""
Self-Roles System — Grimory Bot

Permette agli utenti di scegliere ruoli tramite embed interattivi:
  💎 Colori (Gemme) — cambia il colore del tuo nome
  ⚔️ Classi D&D     — scegli la tua classe
  🔓 Sblocco        — ottieni ruoli per accedere ad aree speciali

Gli admin/staff configurano tutto dal pannello !config → Self Roles.
"""

import discord
from discord.ext import commands
from discord import ui
from utils import config_manager

# ═══════════════════════════════════════════════════════════
# DATI PRESET — GEMME
# ═══════════════════════════════════════════════════════════

PRESET_COLORS = {
    "Rubino":        "e74c3c",
    "Zaffiro":       "3498db",
    "Smeraldo":      "2ecc71",
    "Topazio":       "f1c40f",
    "Ametista":      "9b59b6",
    "Ambra":         "e67e22",
    "Quarzo Rosa":   "e91e63",
    "Acquamarina":   "00bcd4",
    "Turchese":      "1abc9c",
    "Giada":         "00c853",
    "Diamante":      "ecf0f1",
    "Ossidiana":     "2c3e50",
    "Opale":         "fd79a8",
    "Lapislazzuli":  "0984e3",
}

COLOR_EMOJIS = {
    "Rubino":       "♦️",
    "Zaffiro":      "🔹",
    "Smeraldo":     "💚",
    "Topazio":      "💛",
    "Ametista":     "🔮",
    "Ambra":        "🧡",
    "Quarzo Rosa":  "💗",
    "Acquamarina":  "💎",
    "Turchese":     "🌊",
    "Giada":        "🍀",
    "Diamante":     "💠",
    "Ossidiana":    "🖤",
    "Opale":        "🩷",
    "Lapislazzuli": "💙",
}

COLOR_DESCRIPTIONS = {
    "Rubino":       "Gemma di fuoco — rosso ardente",
    "Zaffiro":      "Gemma del cielo — blu reale",
    "Smeraldo":     "Gemma della foresta — verde profondo",
    "Topazio":      "Gemma del sole — oro brillante",
    "Ametista":     "Gemma dell'arcano — viola mistico",
    "Ambra":        "Gemma della terra — arancione caldo",
    "Quarzo Rosa":  "Gemma dell'amore — rosa delicato",
    "Acquamarina":  "Gemma del mare — celeste cristallino",
    "Turchese":     "Gemma del vento — verde acqua",
    "Giada":        "Gemma dell'equilibrio — verde smeraldo",
    "Diamante":     "Gemma della luce — bianco puro",
    "Ossidiana":    "Gemma dell'ombra — nero profondo",
    "Opale":        "Gemma dei sogni — rosa cangiante",
    "Lapislazzuli": "Gemma della saggezza — blu intenso",
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

# Valore speciale per l'opzione "Rimuovi"
REMOVE_VALUE = "remove_role"


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
            placeholder="💎 Scegli la tua gemma...",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="caricamento", value="0")],
        )

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        guild = interaction.guild
        member = interaction.user
        config = config_manager.get_guild_config(guild.id)

        all_color_ids = {int(v["role_id"]) for v in config.get("color_roles", {}).values()}
        roles_to_remove = [r for r in member.roles if r.id in all_color_ids]

        # Opzione "Rimuovi" — rimuove e basta
        if value == REMOVE_VALUE:
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                await interaction.response.send_message("💎 Gemma rimossa! Torni ai colori base.", ephemeral=True)
            else:
                await interaction.response.send_message("💎 Non hai nessuna gemma equipaggiata.", ephemeral=True)
            return

        role_id = int(value)

        # Rimuovi gemma attuale
        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        role = guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Ruolo non trovato.", ephemeral=True)
            return

        # Se aveva già questa gemma → l'ha rimossa sopra, non la rimette
        if role in roles_to_remove and len(roles_to_remove) == 1 and roles_to_remove[0].id == role_id:
            await interaction.response.send_message(f"💎 Gemma **{role.name}** rimossa!", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.send_message(f"💎 Gemma equipaggiata: **{role.name}**!", ephemeral=True)


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
        value = self.values[0]
        guild = interaction.guild
        member = interaction.user
        config = config_manager.get_guild_config(guild.id)

        all_class_ids = {int(v["role_id"]) for v in config.get("class_roles", {}).values()}
        roles_to_remove = [r for r in member.roles if r.id in all_class_ids]

        # Opzione "Rimuovi"
        if value == REMOVE_VALUE:
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                await interaction.response.send_message("⚔️ Classe rimossa! Sei tornato un avventuriero senza classe.", ephemeral=True)
            else:
                await interaction.response.send_message("⚔️ Non hai nessuna classe equipaggiata.", ephemeral=True)
            return

        role_id = int(value)

        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

        role = guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Ruolo non trovato.", ephemeral=True)
            return

        if role in roles_to_remove and len(roles_to_remove) == 1 and roles_to_remove[0].id == role_id:
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
# HELPER STAFF CHECK
# ═══════════════════════════════════════════════════════════

def _is_staff(ctx: commands.Context) -> bool:
    """Controlla se l'utente è admin o ha il ruolo staff."""
    if ctx.author.guild_permissions.administrator:
        return True
    config = config_manager.get_guild_config(ctx.guild.id)
    staff_role_id = config.get("staff_role_id")
    if staff_role_id:
        return any(r.id == int(staff_role_id) for r in ctx.author.roles)
    return False


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

        color_names = list(config.get("color_roles", {}).keys())
        color_str = ", ".join(f"{COLOR_EMOJIS.get(c, '💎')} {c}" for c in color_names[:8])
        if len(color_names) > 8:
            color_str += f" +{len(color_names) - 8} altre"
        if not color_str:
            color_str = "Nessuna"

        class_names = list(config.get("class_roles", {}).keys())
        class_str = ", ".join(f"{CLASS_EMOJIS.get(c, '⚔️')} {c}" for c in class_names[:8])
        if len(class_names) > 8:
            class_str += f" +{len(class_names) - 8} altre"
        if not class_str:
            class_str = "Nessuna"

        unlock_names = list(config.get("unlock_roles", {}).keys())
        unlock_str = ", ".join(unlock_names[:6]) or "Nessuno"

        embed = discord.Embed(
            title="💎 Configurazione Self Roles",
            description=(
                "Configura i ruoli che gli utenti possono assegnarsi da soli.\n"
                "Il bot creerà automaticamente i ruoli nel server."
            ),
            color=0xE91E63,
        )
        embed.add_field(name="📌 Canale", value=ch, inline=True)
        embed.add_field(name="📊 Totale", value=f"{n_colors} gemme · {n_classes} classi · {n_unlock} sblocco", inline=True)
        embed.add_field(name="💎 Gemme attive", value=color_str, inline=False)
        embed.add_field(name="⚔️ Classi attive", value=class_str, inline=False)
        embed.add_field(name="🔓 Ruoli sblocco", value=unlock_str, inline=False)
        embed.set_footer(text="Usa i bottoni sotto per modificare · Le modifiche sono salvate automaticamente")
        return embed

    @ui.button(label="💎 Gemme / Colori", style=discord.ButtonStyle.primary, row=0)
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
    color_title = ui.TextInput(label="Titolo Embed Gemme", max_length=100, row=0)
    color_desc  = ui.TextInput(label="Descrizione Embed Gemme", style=discord.TextStyle.paragraph, max_length=300, row=1)
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
# CONFIG GEMME / COLORI
# ═══════════════════════════════════════════════════════════

class ColorConfigView(ui.View):
    """Gestione delle gemme con selezione multipla."""

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
            emoji = COLOR_EMOJIS.get(name, "💎")
            desc = COLOR_DESCRIPTIONS.get(name, f"#{hex_code.upper()}")
            options.append(discord.SelectOption(
                label=name, value=name, emoji=emoji,
                description=desc,
                default=(name in enabled),
            ))

        select = ui.Select(
            placeholder="Seleziona le gemme da attivare…",
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

        for name in selected:
            if name not in current:
                hex_code = PRESET_COLORS.get(name, "95a5a6")
                color = discord.Color(int(hex_code, 16))
                emoji = COLOR_EMOJIS.get(name, "💎")
                try:
                    role = await guild.create_role(
                        name=f"{emoji} {name}",
                        color=color,
                        reason=f"Grimory Bot — Gemma: {name}",
                    )
                    current[name] = {"role_id": role.id, "hex": hex_code}
                except discord.Forbidden:
                    pass

        to_remove = [n for n in current if n not in selected and n in PRESET_COLORS]
        for name in to_remove:
            role_id = current[name].get("role_id")
            if role_id:
                role = guild.get_role(int(role_id))
                if role:
                    try:
                        await role.delete(reason="Grimory Bot — Gemma rimossa dalla config")
                    except discord.Forbidden:
                        pass
            del current[name]

        config_manager.update_guild_config(guild.id, color_roles=current)

        new_view = ColorConfigView(self.ctx, self.parent_view)
        embed = new_view.build_embed()
        await interaction.message.edit(embed=embed, view=new_view)

    def build_embed(self):
        config = config_manager.get_guild_config(self.ctx.guild.id)
        enabled = config.get("color_roles", {})

        lines = []
        for name in PRESET_COLORS:
            emoji = COLOR_EMOJIS.get(name, "💎")
            status = "✅" if name in enabled else "❌"
            desc = COLOR_DESCRIPTIONS.get(name, "")
            lines.append(f"{emoji} **{name}** — *{desc}* {status}")

        custom = [n for n in enabled if n not in PRESET_COLORS]
        if custom:
            lines.append("\n**Gemme personalizzate:**")
            for name in custom:
                hex_code = enabled[name].get("hex", "000000")
                lines.append(f"💎 **{name}** — #{hex_code.upper()} ✅")

        embed = discord.Embed(
            title="💎 Gestione Gemme",
            description="Seleziona le gemme nel menu sotto. Il bot creerà/rimuoverà i ruoli automaticamente.",
            color=0xE91E63,
        )
        embed.add_field(name="Gemme disponibili", value="\n".join(lines), inline=False)
        embed.set_footer(text="I ruoli vengono creati/eliminati automaticamente nel server")
        return embed

    @ui.button(label="➕ Gemma Personalizzata", style=discord.ButtonStyle.primary, row=1)
    async def add_custom(self, interaction: discord.Interaction, button: ui.Button):
        modal = CustomColorModal(self.ctx, self)
        await interaction.response.send_modal(modal)

    @ui.button(label="⬅️ Indietro", style=discord.ButtonStyle.danger, row=2)
    async def go_back(self, interaction: discord.Interaction, button: ui.Button):
        embed = self.parent_view.build_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class CustomColorModal(ui.Modal, title="➕ Aggiungi Gemma Personalizzata"):
    name_input = ui.TextInput(label="Nome della gemma", placeholder="es. Granato, Perla, Corallo", max_length=30, row=0)
    hex_input = ui.TextInput(label="Codice HEX (senza #)", placeholder="es. 4B0082", max_length=6, min_length=6, row=1)
    emoji_input = ui.TextInput(label="Emoji (opzionale)", placeholder="es. 💜 🪨 ✨", required=False, max_length=5, row=2)

    def __init__(self, ctx, parent_view):
        super().__init__()
        self.ctx = ctx
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name_input.value.strip()
        hex_code = self.hex_input.value.strip().replace("#", "")
        emoji = self.emoji_input.value.strip() or "💎"

        try:
            color_int = int(hex_code, 16)
        except ValueError:
            await interaction.response.send_message("⚠️ Codice HEX non valido!", ephemeral=True)
            return

        guild = interaction.guild
        config = config_manager.get_guild_config(guild.id)
        current = config.get("color_roles", {})

        if name in current:
            await interaction.response.send_message(f"⚠️ La gemma '{name}' esiste già!", ephemeral=True)
            return

        await interaction.response.defer()

        try:
            role = await guild.create_role(
                name=f"{emoji} {name}",
                color=discord.Color(color_int),
                reason=f"Grimory Bot — Gemma personalizzata: {name}",
            )
            current[name] = {"role_id": role.id, "hex": hex_code, "emoji": emoji}
            # Salva anche l'emoji custom
            COLOR_EMOJIS[name] = emoji
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
                label=name, value=name, emoji=emoji,
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
                        reason=f"Grimory Bot — Classe: {name}",
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
    def __init__(self):
        super().__init__(
            placeholder="➕ Seleziona un ruolo da aggiungere…",
            min_values=1, max_values=1, row=0,
        )

    async def callback(self, interaction: discord.Interaction):
        role = self.values[0]
        config = config_manager.get_guild_config(interaction.guild.id)
        unlock = config.get("unlock_roles", {})

        for data in unlock.values():
            if int(data["role_id"]) == role.id:
                await interaction.response.send_message(f"⚠️ Il ruolo {role.mention} è già configurato!", ephemeral=True)
                return

        if len(unlock) >= 20:
            await interaction.response.send_message("⚠️ Massimo 20 ruoli di sblocco!", ephemeral=True)
            return

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
        self.bot.add_view(PersistentColorView())
        self.bot.add_view(PersistentClassView())

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

        # ── EMBED GEMME ──────────────────────────────────
        color_roles = config.get("color_roles", {})
        if color_roles:
            # Opzione "Rimuovi" in cima
            options = [
                discord.SelectOption(
                    label="❌ Rimuovi Gemma",
                    value=REMOVE_VALUE,
                    emoji="❌",
                    description="Rimuovi la gemma equipaggiata",
                ),
            ]
            for name, data in color_roles.items():
                emoji = data.get("emoji", COLOR_EMOJIS.get(name, "💎"))
                desc = COLOR_DESCRIPTIONS.get(name, f"Colore: #{data.get('hex', '000000').upper()}")
                options.append(discord.SelectOption(
                    label=name, value=str(data["role_id"]),
                    emoji=emoji, description=desc[:100],
                ))

            view = PersistentColorView()
            view.clear_items()
            select = PersistentColorSelect()
            select.options = options
            view.add_item(select)

            embed = discord.Embed(
                title=titles.get("color", "💎 Scegli la tua Gemma"),
                description=descs.get("color", "Seleziona una gemma per cambiare il colore del tuo nome!\nOgni gemma rappresenta un potere diverso."),
                color=0xE91E63,
            )
            color_preview = "\n".join(
                f"{data.get('emoji', COLOR_EMOJIS.get(n, '💎'))} **{n}** — *{COLOR_DESCRIPTIONS.get(n, '')}*"
                for n, data in color_roles.items()
            )
            embed.add_field(name="Gemme disponibili", value=color_preview, inline=False)
            embed.set_footer(text="💎 Seleziona una gemma · ❌ Rimuovi per togliere il colore")

            msg_id = message_ids.get("color")
            msg = await self._send_or_edit(channel, msg_id, embed=embed, view=view)
            message_ids["color"] = msg.id

        # ── EMBED CLASSI ─────────────────────────────────
        class_roles = config.get("class_roles", {})
        if class_roles:
            options = [
                discord.SelectOption(
                    label="❌ Rimuovi Classe",
                    value=REMOVE_VALUE,
                    emoji="❌",
                    description="Rimuovi la classe equipaggiata",
                ),
            ]
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
                description=descs.get("class", "Scegli la classe del tuo personaggio per mostrare a tutti chi sei!"),
                color=0xE67E22,
            )
            class_preview = "  ".join(f"{CLASS_EMOJIS.get(n, '⚔️')} {n}" for n in class_roles)
            embed.add_field(name="Classi disponibili", value=class_preview, inline=False)
            embed.set_footer(text="⚔️ Seleziona una classe · ❌ Rimuovi per togliere la classe")

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
                description=descs.get("unlock", "Clicca i bottoni per ottenere o rimuovere ruoli speciali!"),
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
            embed.set_footer(text="🔓 Clicca per ottenere · Clicca di nuovo per rimuovere")

            msg_id = message_ids.get("unlock")
            msg = await self._send_or_edit(channel, msg_id, embed=embed, view=view)
            message_ids["unlock"] = msg.id

        config_manager.update_guild_config(guild.id, selfroles_message_ids=message_ids)

    async def _send_or_edit(self, channel, message_id, **kwargs):
        if message_id:
            try:
                msg = await channel.fetch_message(int(message_id))
                await msg.edit(**kwargs)
                return msg
            except (discord.NotFound, discord.HTTPException):
                pass
        return await channel.send(**kwargs)

    @commands.command(aliases=["ruoli"])
    async def roles(self, ctx):
        """Apre il pannello di configurazione dei self-roles (admin/staff)."""
        if not _is_staff(ctx):
            await ctx.send("❌ Solo gli **amministratori** o lo **staff** possono configurare i ruoli.")
            return
        view = SelfRolesConfigView(ctx)
        embed = view.build_embed()
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(SelfRoles(bot))
