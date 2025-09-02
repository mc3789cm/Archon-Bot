"""
Database helpers for Archon.
"""
import discord
import aiosqlite

from .logging_labels import *
from unidecode import unidecode
from datetime import datetime

db_path = "/var/lib/Archon/Archon_Database.db"
db: aiosqlite.Connection | None = None

current_date = datetime.now().strftime("%Y-%m-%d")

async def init_db():
    global db
    db = await aiosqlite.connect(db_path)
    try:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS "Statistics" (
                "Server Name" TEXT,
                "Server ID" INTEGER NOT NULL UNIQUE,
                "Join Date" TEXT,
                PRIMARY KEY("Server ID")
            );
            
            CREATE TABLE IF NOT EXISTS "General Configuration" (
                "Server ID" INTEGER NOT NULL UNIQUE,
                "Admin Role ID" INTEGER,
                PRIMARY KEY("Server ID")
            );
        """)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"{EROR_LOG} Failed to initialize database: {e}")

async def add_guild(guild: discord.Guild):
    try:
        await db.execute(
            'INSERT INTO "Statistics" ("Server Name", "Server ID", "Join Date") VALUES (?, ?, ?)',
            (unidecode(guild.name), guild.id, current_date)
        )
        await db.execute(
            'INSERT INTO "General Configuration" ("Server ID") VALUES (?)',
            (guild.id,)
        )
        await db.commit()
        print(f"{INFO_LOG} Added guild {unidecode(guild.name)} to the database.")
    except Exception as e:
        await db.rollback()
        print(f"{EROR_LOG} Failed to add server {guild.name} ({guild.id}): {e}")

async def remove_guild(guild: discord.Guild):
    try:
        await db.execute(
            'DELETE FROM "Statistics" WHERE "Server ID" = ?',
            (guild.id,)
        )
        await db.execute(
            'DELETE FROM "General Configuration" WHERE "Server ID" = ?',
            (guild.id,)
        )
        await db.commit()
        print(f"{INFO_LOG} Removed guild {unidecode(guild.name)}.")
    except Exception as e:
        await db.rollback()
        print(f"{EROR_LOG} Failed to remove server {guild.name} ({guild.id}): {e}")

async def add_admin_role(role: discord.Role, guild: discord.Guild):
    assert db is not None, "Database is not initialized."
    try:
        await db.execute(
            'UPDATE "General Configuration" SET "Admin Role ID" = ? WHERE "Server ID" = ?',
            (role.id, guild.id)
        )
        await db.commit()
        print(f"{INFO_LOG} Set admin role for {guild.name} to {role.name}.")
    except Exception as e:
        await db.rollback()
        print(f"{EROR_LOG} Failed to set admin role: {e}")