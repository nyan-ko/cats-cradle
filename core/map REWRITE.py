
from core.interfaces.user_abc import UserABC
from core.interfaces.map_abc import MapABC
from core.interfaces.position_abc import PositionABC

from core.structs.move_permissions import MovePermissions
from core.structs.move_attempt import MoveAttempt

class Map(MapABC):
    """ TODO
    """

    # Start private attributes
    _positions: dict[str, PositionABC]
    # End private attributes

    # Start ABC methods
    def get_position_by_identifier(self, id: str) -> PositionABC:
        if id in self._positions:
            return self._positions[id]
        else:
            return None
    
    def try_move_user(self, attempt: MoveAttempt) -> bool:
        if self.validate_move(attempt):
            self.move_user(attempt)
            return True
        else:
            return False
    
    def move_user(self, attempt: MoveAttempt) -> None:
        user = attempt.who
        destination = attempt.end
        user.move(destination.get_identifier())
    
    def validate_move(self, attempt: MoveAttempt) -> bool:
        return True  # TODO
    # End ABC methods