from core.interfaces.user_abc import UserABC
from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

class Game:
    

    _map: MapABC


    def __init__(self, map: MapABC) -> None:
        self._map = map

    def get_map(self) -> list[PositionABC]:
        return [position for position in self._map]