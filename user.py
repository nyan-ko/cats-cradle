"""
"""

from quest_tree import QuestTree

class User:
    """
    """

    position: QuestTree

    def __init__(self) -> None:
        """
        """

        pass

    def make_choice(self, choice: str) -> None:
        """
        """

        self.position = self.position.get_path(choice)