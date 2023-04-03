from __future__ import annotations
from typing import Optional

import discord
from discord.ext import commands
import aiosqlite

from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue, DialogueGenerator
from constants import Biome, Context
from test_tree import p, r

from biome_generator import BiomeGenerator
from reward_generator import RewardGenerator
from deserializer import TreeDeserializer
from user import User as GameUser

import cogs.quest

class CatsCradle(commands.Bot):
    """
    """

    game_user: GameUser
    deserializer: TreeDeserializer
    biome_generator: BiomeGenerator
    _db: Optional[aiosqlite.Connection]

    def __init__(self, user: GameUser, 
                 deserializer: TreeDeserializer,
                 b_generator: BiomeGenerator) -> None:
        """
        """

        intents = discord.Intents().default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix='!', intents=intents)

        self.game_user = user
        self.deserializer = deserializer
        self.biome_generator = b_generator
        self._db = None

    async def on_ready(self) -> None:
        """
        """

        self._db = await aiosqlite.connect("bot.db")
        async with self._db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS inventory (id INTEGER, cats TEXT)')
        await self._db.commit()

        await self.add_cog(cogs.quest.Quest(self))

    async def update_inventory(self, user_id: int, cat: str):
        """
        """

        async with self._db.cursor() as cursor:
            await cursor.execute('INSERT INTO inventory VALUES(?, ?)', (user_id, cat))
        await self._db.commit()
        return

    def get_user(self) -> GameUser:
        """
        """

        return self.game_user
    
    def get_deserializer(self) -> TreeDeserializer:
        """
        """

        return self.deserializer
    
    def get_biome_gen(self) -> BiomeGenerator:
        """
        """

        return self.biome_generator
    
    def get_db(self) -> aiosqlite.Connection:
        """
        """

        return self._db
