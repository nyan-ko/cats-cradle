from __future__ import annotations
from abc import ABC, abstractmethod

from core.interfaces.user_abc import UserABC

class PositionABC(ABC):
    """ Interface for defining a position.
    """

    @abstractmethod
    def get_identifier(self) -> str:
        pass

    @abstractmethod
    def get_neighbours(self) -> list[PositionABC]:
        pass
    
    @abstractmethod
    def get_occupants(self) -> list[UserABC]:
        pass
    
    @abstractmethod
    def get_rewards(self) -> list[str]:
        pass