"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains the class for the CatsCradle bot.
Methods exist for the interactions between the user and the bot, as well as the generators the bot needs.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

from __future__ import annotations
from typing import Optional

import discord
from discord.ext import commands
import aiosqlite

from biome_generator import BiomeGenerator
from deserializer import TreeDeserializer
from user import User as GameUser

from quest import Quest

class CatsCradle(commands.Bot):
    """Main bot class for Cats Cradle. Initializes the discord bot.

    Instance Attributes:
    - game_user: GameUser object representing the user.
    - deserializer: Represents a TreeDeserializer object.
    - biome_generator: Represents a BiomeGenerator object.
    - _db: Represents the database connection with aiosqlite.
    """

    game_user: GameUser
    deserializer: TreeDeserializer
    biome_generator: BiomeGenerator
    _db: Optional[aiosqlite.Connection]

    ###############################################################################
    # Starter Code
    ###############################################################################

    def __init__(self, user: GameUser,
                 deserializer: TreeDeserializer,
                 b_generator: BiomeGenerator) -> None:

        intents = discord.Intents().default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix='!', intents=intents)

        self.game_user = user
        self.deserializer = deserializer
        self.biome_generator = b_generator
        self._db = None

    async def on_ready(self) -> None:
        """From the discord.py docs: "Called when the client is done preparing the data received from Discord.
        This usually happens after login is successful and the Client.guilds and co. are filled up." This function is
        not meant to be called by the user.

        In this function, we sync the bot slash commands and connect the bot to the database while creating a table.
        """
        self._db = await aiosqlite.connect("bot.db")
        async with self._db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS inventory (id INTEGER, cats TEXT)')
        await self._db.commit()

        await self.add_cog(Quest(self))

    ###############################################################################
    # Database Code
    ###############################################################################

    async def update_inventory(self, user_id: int, cat: str):
        """Updates the user's inventory in bot.db using aiosqlite.
        """
        async with self._db.cursor() as cursor:
            await cursor.execute('INSERT INTO inventory VALUES(?, ?)', (user_id, cat))
        await self._db.commit()
        return

    ###############################################################################
    # Returning Instance Attributes
    ###############################################################################

    def get_user(self) -> GameUser:
        """Returns self.gamer_user.
        """

        return self.game_user

    def get_deserializer(self) -> TreeDeserializer:
        """Returns self.deserializer.
        """
        return self.deserializer

    def get_biome_gen(self) -> BiomeGenerator:
        """Returns self.biome_generator.
        """
        return self.biome_generator

    def get_db(self) -> aiosqlite.Connection:
        """Returns self._db.
        """
        return self._db
