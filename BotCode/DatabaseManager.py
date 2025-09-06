import discord
import aiosqlite

from .LoggingPrefixes import *
from unidecode import unidecode
from datetime import datetime
from typing import Optional

class DatabaseManager:
    """
    Manages all interactions with the SQLite database for storing and managing guild-specific data.

    Attributes:
        db_path (str): The path to the SQLite database file.
        db (Optional[aiosqlite.Connection]): The database connection instance.
        current_date (str): The current date in YYYY-MM-DD format, used for guild join date.
    """
    def __init__(self, db_path: str = "/var/lib/discord_bot/database.db"):
        self.db_path = db_path
        self.db: Optional[aiosqlite.Connection] = None
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    async def initialize(self):
        """
        Initializes the SQLite database by establishing a connection and creating the necessary tables
        if they do not already exist.

        The tables created are:
            - "Statistics": Stores guild statistics.
            - "General Configuration": Stores guild-specific configuration data.

        If the database is already initialized, no changes are made.

        Raises:
            Exception: If an error occurs during the table creation or database commit.
        """
        self.db = await aiosqlite.connect(self.db_path)
        try:
            await self.db.executescript(
            """
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
            """
            )
            await self.db.commit()
            print(f"{INFO_LOG} Database successfully initialized.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to initialize database: {error}")

    async def add_guild(self, guild: discord.Guild):
        """
        Adds a new guild to the "Statistics" and "General Configuration" tables in the database.

        Args:
            guild (discord.Guild): The Discord guild object to be added to the database.

        Raises:
            Exception: If an error occurs while adding the guild to the database.
        """
        try:
            await self.db.execute(
                'INSERT INTO "Statistics" ("Server Name", "Server ID", "Join Date") VALUES (?, ?, ?)',
                (unidecode(guild.name), guild.id, self.current_date)
            )
            await self.db.execute(
                'INSERT INTO "General Configuration" ("Server ID") VALUES (?)',
                (guild.id,)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Added guild '{unidecode(guild.name)}' to the database.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to add guild '{unidecode(guild.name)}'/({guild.id}) to the database: {error}")

    async def remove_guild(self, guild: discord.Guild):
        """
        Removes a guild from both the "Statistics" and "General Configuration" tables in the database.

        Args:
            guild (discord.Guild): The Discord guild object to be removed from the database.

        Raises:
            Exception: If an error occurs while removing the guild from the database.
        """
        try:
            await self.db.execute(
                'DELETE FROM "Statistics" WHERE "Server ID" = ?',
                (guild.id,)
            )
            await self.db.execute(
                'DELETE FROM "General Configuration" WHERE "Server ID" = ?',
                (guild.id,)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Removed guild '{unidecode(guild.name)}' from the database.")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to remove guild '{guild.name}'/({guild.id}) from the database: {error}")
    async def set_admin_role(self, role: discord.Role, guild: discord.Guild):
        """
        Sets the admin role ID for a specific guild in the "General Configuration" table.

        Args:
            role (discord.Role): The role object representing the admin role to be set.
            guild (discord.Guild): The Discord guild object where the admin role will be set.

        Raises:
            Exception: If an error occurs while updating the admin role in the database.
        """
        try:
            await self.db.execute(
                'UPDATE "General Configuration" SET "Admin Role ID" = ? WHERE "Server ID" = ?',
                (role.id, guild.id)
            )
            await self.db.commit()
            print(f"{INFO_LOG} Set admin role for '{guild.name}'/({guild.id}).")

        except Exception as error:
            await self.db.rollback()
            print(f"{EROR_LOG} Failed to set admin role for '{guild.name}'/({guild.id}): {error}")

    async def close(self):
        """
        Closes the database connection.

        This method should be called when the database is no longer needed to release resources.

        Raises:
            Exception: If an error occurs while closing the database connection.
        """
        if self.db:
            await self.db.close()
            self.db = None
            print(f"{INFO_LOG} Database connection closed.")