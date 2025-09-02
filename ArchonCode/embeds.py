"""
Embedded content for Archon.
"""
from pydoc import describe

import discord

primary_color = 1545169
error_color = 8388608

# ---------------
# Information
# ---------------
HelpEmbed = discord.Embed(
    title="Help Menu",
    description="This is the help menu.",
    color=primary_color,
)

PingEmbed = discord.Embed(
    title="Ping",
    description="",
    color=primary_color,
)

ShutdownEmbed = discord.Embed(
    title="Shutting down...",
    description="The bot is going to shutdown now.",
    color=primary_color,
)

AdminRoleSetEmbed = discord.Embed(
    title="Admin Role Is Set",
    description=f"The admin role is set to",
    color=primary_color,
)

# ---------------
# Errors
# ---------------
ErrorForbidden = discord.Embed(
    title="Error: Forbidden",
    description="You do not have the required permissions to run this command.",
    color=error_color,
)

ErrorGuildOnly = discord.Embed(
    title="Error: Guild Only",
    description="You can only run this command in a guild (server).",
    color=error_color,
)