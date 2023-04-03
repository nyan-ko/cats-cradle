"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and methods to represent the interactions a user can make within a quest line.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

from __future__ import annotations
from quest_tree import QuestTree


class User:
    """Class representing the user.

    Instance Attributes:
    - position: QuestTree object representing the current quest tree.
    """

    position: QuestTree

    def __init__(self) -> None:
        self.position = None

    def make_choice(self, choice: str) -> QuestTree:
        """Advances the user to their choice in the QuestTree.
        """
        self.position = self.position.get_path(choice)
        return self.position

    def get_position(self) -> QuestTree:
        """Returns self.position.
        """
        return self.position

    def get_choices(self) -> dict[str, QuestTree]:
        """Returns the paths corresponding to self.position.
        """
        return self.position.paths

    def start_quest(self, tree: QuestTree) -> None:
        """Initializes self.position to equal the QuestTree when the quest begins.
        """
        self.position = tree

    def started_quest(self) -> bool:
        """Returns True if the user has started their quest.
        """
        return self.position is not None
