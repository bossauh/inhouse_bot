import os
import discord
from string import Template
from discord.ext import commands

from inhouse_bot.common_utils.get_server_config import get_server_config_by_key
from inhouse_bot.database_orm import Game

VOICE_CATEGORY = os.getenv('VOICE_CATEGORY', '▬▬ Team Voice Chat ▬▬')
VOICE_PUBLIC_CHANNEL = os.getenv('VOICE_PUBLIC_CHANNEL', '-- Game #$game_id --')
VOICE_TEAM_CHANNEL = os.getenv('VOICE_TEAM_CHANNEL', '--> $side Team #$game_id $color')
VOICE_ICONS = {
    "BLUE": "🔵",
    "RED": "🔴",
}


async def create_voice_channels(ctx: commands.Context, game: Game):
    """
    Creates a private voice channel for each team of players in a game and a public
    voice channel for all to join
    """

    if not get_server_config_by_key(server_id=ctx.guild.id, key="voice"):
        return

    category = discord.utils.get(ctx.guild.categories, name=VOICE_CATEGORY)
    # Creates the category for Team Voice Chat if it doesn't exist
    if category is None:
        category = await discord.Guild.create_category(ctx.guild, VOICE_CATEGORY)

    # Creates a public channel that also acts as a header for the team voice channels
    # Commented as not needed
    # await discord.Guild.create_voice_channel(
    #    ctx.guild,
    #    name=Template(VOICE_PUBLIC_CHANNEL).substitute(game_id=game.id),
    #    category=category,
    #)

    for side in ("BLUE", "RED"):
        await discord.Guild.create_voice_channel(
            ctx.guild,
            name=Template(VOICE_TEAM_CHANNEL).substitute(side=side.capitalize(), game_id=game.id, color=VOICE_ICONS[side]),
            category=category,
        )


async def remove_voice_channels(ctx: commands.Context, game_id: int):
    """
    Removes all voice channels associated with a game
    """

    if not get_server_config_by_key(server_id=ctx.guild.id, key="voice"):
        return

    for channel in [
        Template(VOICE_PUBLIC_CHANNEL).substitute(game_id=game_id),
        Template(VOICE_TEAM_CHANNEL).substitute(side="Blue", game_id=game_id, color=VOICE_ICONS["BLUE"]),
        Template(VOICE_TEAM_CHANNEL).substitute(side="Red", game_id=game_id, color=VOICE_ICONS["RED"]),
    ]:
        channel_to_del = discord.utils.get(ctx.guild.channels, name=channel)
        if channel_to_del is not None:
            await channel_to_del.delete()
