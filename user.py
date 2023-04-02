from quest_tree import QuestTree

class User:
    """ TODO
    """

    position: QuestTree


    def __init__(self, start: QuestTree) -> None:
        """ TODO
        """

        self.position = QuestTree

    def get_position(self) -> QuestTree:   
        """ TODO
        """

        return self.position

    def make_choice(self, choice: str) -> None:
        """ TODO
        """

        self.position = self.position.get_path(choice)


