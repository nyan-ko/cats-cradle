
from core.interfaces.user_abc import UserABC
from core.interfaces.position_abc import PositionABC

from structs.move_permissions import MovePermissions

class MoveAttempt:
    """ TODO
    """

    who: UserABC
    start: PositionABC
    end: PositionABC
    permissions: MovePermissions

    def __init__(self, 
                 who: UserABC, 
                 start: PositionABC, 
                 end: PositionABC,
                 permissions: MovePermissions) -> None:
        """
        """

        self.who = who
        self.start = start
        self.end = end
        self.permissions = permissions