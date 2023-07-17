from services.request_map import RequestMap, RequestMapResult, TransferablePosition

from cc_discord.view_data import ViewData

from discord.interactions import Interaction

class ViewMap:

    _positions: list[TransferablePosition]
    _interaction: Interaction

    def __init__(self, positions: list[TransferablePosition], interaction: Interaction) -> None:
        self._positions = positions
        self._interaction = interaction

    def display(self) -> None:
        self._interaction.response.edit_message(content="Map")