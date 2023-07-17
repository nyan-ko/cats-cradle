from core.game import Game

class AbstractService:

    game: Game

    def __init__(self, game: Game) -> None:
        self.game = game

    def execute(self) -> None:
        raise NotImplementedError

