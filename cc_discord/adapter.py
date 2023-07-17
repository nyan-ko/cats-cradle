from services.interfaces.controller_abc import ControllerABC
from services.request_map import RequestMap, RequestMapResult

from cc_discord.view_data import ViewData

class Adapter:

    _controller: ControllerABC
    _data: ViewData

    def __init__(self, data: ViewData, controller: ControllerABC) -> None:
        self._data = data
        self._controller = controller
        

    def request_map(self) -> None:
        map = self._controller.request_map()
        self._data.set_map(map)