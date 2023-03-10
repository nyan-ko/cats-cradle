from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from user_interaction import Dialogue


class Biome(Enum):
    """ Possible biomes a node is allowed to take. Generally dictates which nodes are allowed to connect with each other.
    """

    TEMPERATE = 1,
    FRIGID = 2, 
    TROPICAL = 3
    ARID = 4,
    URBAN = 5


@dataclass
class SituationNode:
    """ Representation of an individual scenario within a quest.

    Attributes:
    - reward: a string describing the user's reward for arriving at this node, or None. 
        TODO: figure out format for cat strings and items
    - biome: an enum representing this node's biome.
    - dialogue: a mapping of dialogue with respect to the context in which they appear.
        Valid contexts:
        - 'enter': when the user enters this node.
        - 'stay': when the user is analyzing this node's paths.
        - 'exit': when the user leaves this node.

    TODO: representation invariants
    """

    reward: Optional[str]
    biome: Biome
    dialogue: dict[str, Dialogue]


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


