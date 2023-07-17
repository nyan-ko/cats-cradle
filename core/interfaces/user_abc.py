
from abc import ABC, abstractmethod

from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

from core.structs.move_permissions import MovePermissions

class UserABC(ABC):
    """ Interface for defining a user.
    """
    
    @abstractmethod
    def try_move(self, position_identifier: str) -> bool:
        pass

    @abstractmethod
    def move(self, position_identifier: str) -> None:
        pass

    @abstractmethod
    def get_position(self) -> PositionABC:
        pass

    @abstractmethod
    def get_identifier(self) -> str:
        pass
