# ---------------
# Imports
# ---------------
from ArchonCode import *
import discord
from discord.ext import commands
import logging
import asyncio
from os import getenv

# ---------------
# Initialization/Setup
# ---------------
Intentions = discord.Intents.none()
Intentions.guilds = True
Intentions.members = True
Intentions.message_content = True
Intentions.messages = True

bot = commands.AutoShardedBot(
    owner_id=1394001075547148530,
    intents=Intentions,
    command_prefix="?",
    case_insensitive=True,
    help_command=None,
    description=None,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Activity(type=discord.ActivityType.watching, name="?help"),
    status=discord.Status.idle
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
init_logging()

# ---------------
# Events
# ---------------
@bot.event
async def on_ready():
    print(f"----------")
    print(f"{INFO_LOG} Bot user: \033[1;35m{bot.user}\033[0m")
    print(f"{INFO_LOG} Status: \033[1;37m{bot.status}\033[0m")

    await bot.tree.sync()
    print(f"{INFO_LOG} Synchronized application commands")

    for shard_id in range(bot.shard_count):
        print(f"{INFO_LOG} Shard \033[1;37m{shard_id}\033[0m is online")
    print("----------")

@bot.event
async def on_guild_join(guild):
    await add_guild(guild)

@bot.event
async def on_guild_remove(guild):
    await remove_guild(guild)

# ---------------
# Prefix Commands
# ---------------
@bot.command()
async def help(ctx):
    await ctx.send(embed=HelpEmbed)

@bot.command()
async def ping(ctx):
    await ctx.send(embed=PingEmbed)

@bot.command()
async def shutdown(ctx):
    if ctx.author.id != bot.owner_id:
        return await ctx.send(embed=ErrorForbidden)
    print(f"{WARN_LOG} Received shutdown signal...")
    await ctx.send(embed=ShutdownEmbed)
    return await bot.close()

# ---------------
# Slash Commands
# ---------------
@bot.tree.command(name="set_admin", description="Set the server-wide admin role", nsfw=False)
@discord.app_commands.describe(role="The role to set as admin")
async def set_admin(interaction: discord.Interaction, role: discord.Role):
    if interaction.guild is None:
        return await interaction.response.send_message(embed=ErrorGuildOnly, ephemeral=True)
    if interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message(embed=ErrorForbidden, ephemeral=True)
    await add_admin_role(role, interaction.guild)
    await interaction.response.send_message(embed=AdminRoleSetEmbed, ephemeral=True)

# ---------------
# Start Bot
# ---------------
async def main():
    await init_db()
    print(f"{INFO_LOG} Database initialized")
    token = getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set")
    try:
        await bot.start(token)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print(f"{WARN_LOG} Shutdown requested, cleaning up...")
    finally:
        if db:
            await db.close()
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{WARN_LOG} Forced shutdown with Ctrl+C")