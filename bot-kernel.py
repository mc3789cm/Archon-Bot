from discord.ext.commands import AutoShardedBot
from time import monotonic
from os import getenv
from sys import exit

import discord
import logging
import asyncio

from BotCode.DatabaseManager import DatabaseManager
dbmgr = DatabaseManager(db_path="/var/lib/discord_bot/database.db")

from BotCode.EmbedManager import EmbedManager
ebmgr = None

from BotCode.LoggingPrefixes import QSTN_LOG, INFO_LOG, WARN_LOG, EROR_LOG, CRIT_LOG
print(f"{QSTN_LOG} | {INFO_LOG} | {WARN_LOG} | {EROR_LOG} | {CRIT_LOG}")

Intentions = discord.Intents.none()
Intentions.guilds = True
Intentions.members = True
Intentions.message_content = True
Intentions.messages = True

bot = AutoShardedBot(
    owner_ids={1117890340867809340, 1394001075547148530},
    intents=Intentions,
    command_prefix="?",
    case_insensitive=True,
    help_command=None,
    description=None,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="?help"),
    status=discord.Status.online
)

def init_logging(default_level=30):
    log_levels = {
        10: logging.DEBUG,
        20: logging.INFO,
        30: logging.WARNING,
        40: logging.ERROR,
        50: logging.CRITICAL
    }

    log_level = None

    while log_level is None:
        user_input = input(f"{QSTN_LOG} Select log level (10-50): ").strip()
        if user_input == "":
            log_level = default_level
            break
        try:
            log_level = int(user_input)
            if log_level not in log_levels:
                print(f"{EROR_LOG}: RangeError: Select a number (10-50)")
                log_level = None
        except ValueError:
            print(f"{EROR_LOG}: ValueError: Select a number (10-50)")

    logging.basicConfig(level=log_level)

    discord_loggers = ["discord.client", "discord.gateway", "discord.http"]
    for logger_type in discord_loggers:
        logging.getLogger(logger_type).setLevel(log_level)

    print(f"{INFO_LOG} Logging set to {logging.getLevelName(log_level)}")

# -------
# Events
# -------
@bot.event
async def on_ready():
    print(f"----------")
    print(f"{INFO_LOG} Bot user: {bot.user}")
    print(f"{INFO_LOG} Status: {bot.status}")

    await bot.tree.sync()
    print(f"{INFO_LOG} Synchronized application commands")

    for shard_id in range(bot.shard_count):
        print(f"{INFO_LOG} Shard {shard_id} is online")
    print("----------")

    global ebmgr

    ebmgr = EmbedManager(primary_color="#1793d1",
                error_color="#dc143c",
                bot_name=bot.user.name)

@bot.event
async def on_guild_join(guild: discord.Guild):
    await dbmgr.add_guild(guild)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=ebmgr.join_embed())
            break

@bot.event
async def on_guild_remove(guild: discord.Guild):
    await dbmgr.remove_guild(guild)

# ----------------
# Prefix Commands
# ----------------
context = discord.ext.commands.Context

@bot.command()
async def help(ctx: context):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    msg = await ctx.send(embed=ebmgr.help_embed())

    await asyncio.sleep(120)
    try:
        await msg.delete()
    except discord.Forbidden:
        pass

@bot.command()
async def ping(ctx: context):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    ws_latency = round(bot.latency * 1000)

    before = monotonic()
    msg = await ctx.send(embed=ebmgr.ping_embed())
    after = monotonic()
    api_latency = round((after - before) * 1000)

    await msg.edit(embed=ebmgr.pong_embed(
        ws_latency=ws_latency,
        api_latency=api_latency,
        sent_by=ctx.author)
    )

    await asyncio.sleep(30)
    try:
        await msg.delete()
    except discord.Forbidden:
        pass

@bot.command()
async def shutdown(ctx: context):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    if ctx.author.id not in bot.owner_ids:
        await ctx.send(embed=ebmgr.error_forbidden())
        return print(f"{WARN_LOG} Shutdown command called by unauthorized user: {ctx.author}")

    print(f"{INFO_LOG} Received shutdown signal from {ctx.author}.")
    await ctx.send(embed=ebmgr.shutdown_embed(sent_by=ctx.author))
    return await stop_bot()

# ---------------
# Slash Commands
# ---------------
@bot.tree.command(name="set_admin", description="Set the server-wide admin role.", nsfw=False)
@discord.app_commands.describe(role="The role to set as admin.")
async def set_admin(interaction: discord.Interaction, role: discord.Role):
    if interaction.guild is None:
        return await interaction.response.send_message(embed=ebmgr.error_guild_only(), ephemeral=True)
    if interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message(embed=ebmgr.error_forbidden(), ephemeral=True)
    await dbmgr.set_admin_role(role=role, guild=interaction.guild)
    return await interaction.response.send_message(embed=ebmgr.admin_role_set(role=role.mention), ephemeral=True)

# ---------------
# Runtime Handling
# ---------------
async def start_bot():
    token = getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError(f"{EROR_LOG} DISCORD_TOKEN environment variable is not set.")
    try:
        init_logging()
        await dbmgr.initialize()
        await bot.start(token)
    except (KeyboardInterrupt, asyncio.CancelledError):
        await stop_bot()

async def stop_bot():
    print(f"{INFO_LOG} Stopping bot...")
    await bot.close()
    await dbmgr.close()
    exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print(f"{WARN_LOG} Forced shutdown with Ctrl+C.")