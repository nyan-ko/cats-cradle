from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import constants
from user_interaction import Dialogue


@dataclass
class SituationNode:
    """ Representation of an individual scenario within a quest.

    Attributes:
    - reward: a string describing the user's reward for arriving at this node, or None. 
        TODO: figure out format for cat strings and items
    - biome: an enum representing this node's biome.
    - dialogue: a mapping of dialogue with respect to the context in which they appear.

    TODO: representation invariants
    """

    reward: Optional[str]
    biome: constants.Biome
    dialogue: dict[constants.Context, Dialogue]


class QuestTree:
    """ Recursive tree implementation of a branching quest line.

    Attributes:
    - current_node: the root node of this tree.
    - paths: the possible nodes the user can traverse to.

    TODO: representation invariants
    """

    current_node: SituationNode
    paths: set[QuestTree]

    def __init__(self, node: SituationNode) -> None:
        """Initializes a new quest tree.
        """

        self.current_node = node
        self.paths = set()

    def add_path(self, path: QuestTree) -> None:
        """Adds a quest tree to this tree's possible paths.
        """

        self.paths.add(path)
        
    def begin_quest(self) -> Dialogue:
        """Begins the quest. Returns the node's dialogue.
        """
        # this may be able to be generalized for all nodes not only the first
        return self.current_node.dialogue[constants.Context]


