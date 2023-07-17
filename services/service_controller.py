from core.game import Game

from services.interfaces.controller_abc import ControllerABC
from services.request_map import RequestMap, RequestMapResult

class ServiceController(ControllerABC):

    _game: Game

    def __init__(self, game: Game) -> None:
        self._game = game

    def request_map(self) -> RequestMapResult:
        return RequestMap(self._game).execute()