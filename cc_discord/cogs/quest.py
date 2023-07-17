from __future__ import annotations

from cc_discord.adapter import Adapter
from cc_discord.view_data import ViewData

from cc_discord.view_map import ViewMap

from discord import Color, Embed, Interaction, ButtonStyle
from discord.ui import View, button, Button
from discord.ext.commands import Cog, Context

from discord.app_commands import command

class Quest(Cog):

    _adapter: Adapter
    _data: ViewData

    def __init__(self) -> None:
        super().__init__()

    @command(name="view map")
    async def request_map(self, interaction: Interaction):
        self._adapter.request_map()
        response = ViewMap(self._data.get_map(), interaction)
        await response.display()

