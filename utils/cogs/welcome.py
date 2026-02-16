import discord
from discord.ext import commands
from utils import config_manager


class Welcome(commands.Cog):
    """Sistema di benvenuto e addio automatico."""

    def __init__(self, bot):
        self.bot = bot

    def _format_message(self, template: str, member: discord.Member) -> str:
        """Sostituisce i placeholder nel messaggio."""
        return template.format(
            member=member.mention,
            name=member.display_name,
            server=member.guild.name,
            count=member.guild.member_count,
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Invia messaggio di benvenuto quando un membro entra."""
        config = config_manager.get_guild_config(member.guild.id)

        if not config["welcome_enabled"]:
            return

        channel_id = config["welcome_channel_id"]
        if channel_id is None:
            return

        channel = member.guild.get_channel(int(channel_id))
        if channel is None:
            return

        msg = self._format_message(config["welcome_message"], member)

        if config["welcome_embed"]:
            color = int(config.get("welcome_color", "8B4513"), 16)
            embed = discord.Embed(
                title="⚔️ Un nuovo avventuriero è arrivato!",
                description=msg,
                color=color,
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(
                name="📊 Membro n°",
                value=f"**#{member.guild.member_count}**",
                inline=True,
            )
            embed.set_footer(text=f"Benvenuto su {member.guild.name}!")
            await channel.send(embed=embed)
        else:
            await channel.send(msg)

        # Auto-ruolo
        role_id = config.get("auto_role_id")
        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    await member.add_roles(role, reason="Auto-ruolo Grimory Bot")
                except discord.Forbidden:
                    pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Invia messaggio di addio quando un membro esce."""
        config = config_manager.get_guild_config(member.guild.id)

        if not config["goodbye_enabled"]:
            return

        channel_id = config.get("goodbye_channel_id") or config.get("welcome_channel_id")
        if channel_id is None:
            return

        channel = member.guild.get_channel(int(channel_id))
        if channel is None:
            return

        msg = self._format_message(config["goodbye_message"], member)

        embed = discord.Embed(
            title="🚪 Un avventuriero ci ha lasciato…",
            description=msg,
            color=0x95A5A6,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
