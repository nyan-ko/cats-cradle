
from core.interfaces.user_abc import UserABC
from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

class Planet(PositionABC):
    """ TODO
    """

    # Start private attributes
    _identifier: str
    _neighbours: dict[str, PositionABC]
    _occupants: dict[str, UserABC]
    _rewards: list[str]
    # End private attributes

    def get_identifier(self) -> str:
        return self._identifier
    
    def get_neighbours(self) -> list[PositionABC]:
        return self._neighbours
    
    def get_occupants(self) -> list[UserABC]:
        return self._occupants
    
    def get_rewards(self) -> list[str]:
        return self._rewards