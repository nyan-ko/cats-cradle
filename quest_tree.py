"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes to represent a quest tree and its nodes.
Methods exist for serialization and deserialization of trees.

This file is copyright (c) 2023 by Edric Liu.
"""

from __future__ import annotations
import constants
from user_interaction import Dialogue
from io import TextIOWrapper


class SituationNode:
    """ Representation of an individual scenario within a quest.

    Attributes:
    - reward: a string describing the user's reward for arriving at this node, or None.
    - biome: an enum representing this node's biome.
    - dialogue: a mapping of dialogue with respect to the context in which they appear.
    - id: a unique identifier for this tree.

    Representation Invariants:
    - len(self.reward) > 0
    - len(self.dialogue) == 4
    - self.identifier is a unique string in its corresponding tree
    """

    reward: str
    biome: constants.Biome
    dialogue: dict[constants.Context, Dialogue]
    random_dialogue: bool
    identifier: str

    def __init__(self, reward: str,
                 biome: constants.Biome,
                 dialogue: dict[constants.Context, Dialogue],
                 random_dialogue: bool,
                 identifier: str) -> None:
        """ Initializes a new situation.
        """

        self.reward = reward
        self.biome = biome
        self.dialogue = dialogue
        self.random_dialogue = random_dialogue
        self.identifier = identifier

    def return_dialogue(self) -> Dialogue:
        """Returns the node's dialogue.
        """
        return self.dialogue[constants.Context.ENTER].return_dialogue()

    def __eq__(self, __value: object) -> bool:
        """ Determines if two nodes are equal to each other.
        Equality is determined by all attributes being equal.
        """

        if isinstance(__value, SituationNode):
            return self.reward == __value.reward and \
                self.biome == __value.biome and \
                self.dialogue == __value.dialogue and \
                self.identifier == __value.identifier

        return False

    def serialize(self) -> str:
        """ Converts this node into a text representation, with the format "<id>_<reward>_<biome>_<dialogue>".
        """

        # The splitter character.
        split = "_"

        if not self.random_dialogue:
            return f"{self.identifier}{split}" + \
                f"{self.reward}{split}" + \
                f"{self.biome.value}{split}" + \
                f"{self._serialize_dialogue()}"
        else:  # No need to serialize dialogue if it was randomly generated
            return f"{self.identifier}{split}" + \
                f"{self.reward}{split}" + \
                f"{self.biome.value}"

    def _serialize_dialogue(self) -> str:
        """ Helper function to convert the dialogue dictionary into a text representation.

        Preconditions:
        - not self.random_dialogue
        """

        split = "~"

        d1 = self.dialogue[constants.Context.ENTER]
        d2 = self.dialogue[constants.Context.INVESTIGATE]
        d3 = self.dialogue[constants.Context.PREVIEW]
        d4 = self.dialogue[constants.Context.EXIT]

        return f"\"{d1.title}{split}{d1.message}{split}{d1.image_path}{split}" + \
            f"{d2.title}{split}{d2.message}{split}{d2.image_path}{split}" + \
            f"{d3.title}{split}{d3.message}{split}{d3.image_path}{split}" + \
            f"{d4.title}{split}{d4.message}{split}{d4.image_path}\""


class QuestTree:
    """ Recursive tree implementation of a branching quest line.

    Attributes:
    - current_node: the root node of this tree.
    - paths: the possible subtrees the user can traverse to. Each key is equal to
        the 'identifier' attribute of the node within the corresponding subtree.

    Representation Invariants:
    - self.current_node is not None
    - all(key == self.paths[key].get_identifier() for key in self.paths)
    """

    current_node: SituationNode
    paths: dict[str, QuestTree]

    def __init__(self, node: SituationNode) -> None:
        """ Initializes a new quest tree.
        """

        self.current_node = node
        self.paths = {}

    def get_identifier(self) -> str:
        """ Returns the identifier of this tree's node.
        """

        return self.current_node.identifier

    def add_path(self, path: QuestTree) -> None:
        """ Adds a quest tree to this tree's possible paths.

        Preconditions:
        - path.get_identifier() not in self.paths
        """

        self.paths[path.get_identifier()] = path

    def get_path(self, identifier: str) -> QuestTree:
        """ Returns the subtree corresponding to 'identifier'.

        Preconditions:
        - identifier in self.paths
        """

        return self.paths[identifier]

    def return_dialogue(self) -> Dialogue:
        """Returns the node's dialogue.
        """

        return self.current_node.dialogue[constants.Context.ENTER].return_dialogue()

    def __eq__(self, __value: object) -> bool:
        """ Determines if two trees are equal to each other.
        Equality is determined by both nodes being equal, and all subtrees being equal.
        """

        if isinstance(__value, QuestTree):
            if self.current_node != __value.current_node:
                return False
            if len(self.paths) != len(__value.paths):
                return False
            for identifier in self.paths:
                subtree = self.paths[identifier]
                if identifier not in __value.paths or subtree != self.paths[identifier]:
                    return False
            return True
        return False

    def __len__(self) -> int:
        """ Returns the size of this tree, including the current node.
        """

        return sum(len(tree) for tree in self.paths.values()) + 1

    # -------------
    # Serialization
    # -------------

    def serialize(self, output_file: str) -> None:
        """ Converts and writes this tree and its children as a .csv file at output_file.
        Each line of the .csv file represents an individual path through this tree.

        Preconditions:
        - output_file refers to a valid file path.
        """

        with open(output_file, "w") as file:
            self._serialize_helper(file, "", 0)

    def _serialize_helper(self, file: TextIOWrapper, current_line: str, depth: int) -> None:
        """ Recursive helper function to write individual paths.
        """

        # Base case: when there are no more children, write the value of the accumulator.
        if len(self.paths) == 0:
            file.write(f"{current_line}{self.current_node.serialize()}\n")
        else:
            # Recursive step: keep accumulating node data along each path.
            first = True
            for path in self.paths.values():
                if first:
                    # Append the current node as serialized data to the accumulator.
                    # String formatting f"<string>" is used here.
                    appended_line = f"{current_line}{self.current_node.serialize()},"
                    path._serialize_helper(file, appended_line, depth + 1)
                    first = False
                else:
                    # We don't need want data from this node to be repeated through each subtree,
                    # so just add empty columns.
                    empty_columns = "|" * (depth + 1) + ","
                    path._serialize_helper(file, empty_columns, depth + 1)
