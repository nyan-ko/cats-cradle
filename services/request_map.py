from __future__ import annotations

from core.game import Game
from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

from services.abstract_service import AbstractService


class TransferablePosition:
    """ Wrapper
    """

    _position: PositionABC

    def __init__(self, position: PositionABC) -> None:
        self._position = position
    
    def get_identifier(self) -> str:
        return self._position.get_identifier()
    
    def get_neighbours(self) -> list[str]:
        return [pos.get_identifier() for pos in self._position.get_neighbours()]
    
    def get_occupants(self) -> list[str]:
        return [user.get_identifier() for user in self._position.get_occupants()]
    
    def get_rewards(self) -> list[str]:
        return self._position.get_rewards()
    

class RequestMapResult:
    """
    """

    _positions: list[PositionABC]

    def __init__(self, positions: list[PositionABC]) -> None:
        self._positions = positions
    
    def get_positions(self) -> list[TransferablePosition]:
        return [TransferablePosition(pos) for pos in self._positions]


class RequestMap(AbstractService):
    """
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def execute(self) -> RequestMapResult:
        return RequestMapResult(self.game.get_map())