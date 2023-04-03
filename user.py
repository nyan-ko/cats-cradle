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

    def get_choices(self) -> dict[str, QuestTree]:
        """
        """
        
        return self.position.paths
    
    def started_quest(self) -> bool:
        """
        """

        return self.position is not None