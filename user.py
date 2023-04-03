from __future__ import annotations


from quest_tree import QuestTree

class User:
    """
    """

    position: QuestTree

    def __init__(self) -> None:
        """
        """

        self.position = None

    def make_choice(self, choice: str) -> QuestTree:
        """
        """

        self.position = self.position.get_path(choice)
        return self.position

    def get_position(self) -> QuestTree:
        """
        """

        return self.position

    def get_choices(self) -> dict[str, QuestTree]:
        """
        """
        
        return self.position.paths
    
    def start_quest(self, tree: QuestTree) -> None:
        """
        """

        self.position = tree
    
    def started_quest(self) -> bool:
        """
        """

        return self.position is not None