"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and methods to represent the interactions a user can make within a quest line.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

from __future__ import annotations

from core.interfaces.user_abc import UserABC
from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

from core.structs.move_attempt import MoveAttempt
from core.structs.move_permissions import MovePermissions

class User(UserABC):
    """ TODO

    """

    # Start private attributes
    _map: MapABC
    _position: PositionABC  
    _identifier: str
    # End private attributes

    def __init__(self, map: MapABC) -> None:
        self._map = map

    # Start ABC methods
    def try_move(self, position_identifier: str) -> bool:
        """
        """

        destination = self._map.get_position_by_identifier(position_identifier)

        permissions = MovePermissions() # TODO
        attempt = MoveAttempt(self, self.get_position(), destination, permissions)

        return self._map.try_move_user(attempt)
    
    def move(self, position_identifier: str) -> None:
        """
        """

        destination = self._map.get_position_by_identifier(position_identifier)
        self._position = destination
    
    def get_position(self) -> PositionABC:
        return self._position
    
    def get_identifier(self) -> str:
        return self._identifier
    # End ABC methods

