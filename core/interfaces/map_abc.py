from abc import ABC, abstractmethod

from core.interfaces.position_abc import PositionABC, UserABC

from core.structs.move_attempt import MoveAttempt
from core.structs.move_permissions import MovePermissions

class MapABC(ABC):
    """
    """

    @abstractmethod
    def get_position_by_identifier(self, id: str) -> PositionABC:
        pass

    @abstractmethod
    def try_move_user(self, attempt: MoveAttempt) -> bool:
        pass

    @abstractmethod
    def move_user(self, attempt: MoveAttempt) -> None:
        pass

    @abstractmethod
    def validate_move(self, attempt: MoveAttempt) -> bool:
        pass

    @abstractmethod
    def __iter__(self) -> list[PositionABC]:
        pass