from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import constants
from user_interaction import Dialogue
from io import TextIOWrapper


# Characters to split node data into chunks when they're in text form
# These symbols were chosen to avoid potential conflict with links/messages since they're unlikely to be found in normal situations
SERIALIZER_SPLITTER_CHAR = "≠"
DIALOGUE_SPLITTER_CHAR = "℮"


class SituationNode:
    """ Representation of an individual scenario within a quest.

    Attributes:
    - reward: a string describing the user's reward for arriving at this node, or None.
        TODO: figure out format for cat strings and items
    - biome: an enum representing this node's biome.
    - dialogue: a mapping of dialogue with respect to the context in which they appear.
    - id: a unique identifier for this tree.

    TODO: representation invariants
    """

    reward: Optional[str]
    biome: constants.Biome
    dialogue: dict[constants.Context, Dialogue]
    id: str

    def __init__(self, reward: Optional[str], biome: constants.Biome,
                    dialogue: dict[constants.Context, Dialogue], id: str) -> None:
        """ Initializes a new situation.
        """

        self.reward = reward
        self.biome = biome
        self.dialogue = dialogue
        self.id = id

    def return_dialogue(self) -> Dialogue:
        """Returns the node's dialogue.
        """
        return self.dialogue[constants.Context.ENTER].return_dialogue()
    
    def serialize(self) -> str:
        """ Converts this node into a text representation, with the format "<reward>℮<biome>℮<dialogue>".
        """

        split = SERIALIZER_SPLITTER_CHAR

        return f"{self.reward}{split}" + \
                f"{self.biome.value}{split}" + \
                f"{self._serialize_dialogue()}"
        
    def _serialize_dialogue(self) -> str:
        """ Helper function to convert the dialogue dictionary into a text representation.
        """

        split = DIALOGUE_SPLITTER_CHAR

        d1 = self.dialogue[constants.Context.ENTER]
        d2 = self.dialogue[constants.Context.INVESTIGATE]
        d3 = self.dialogue[constants.Context.EXIT]

        return f"{d1.title}{split}{d1.message}{split}{d1.image_path}{split}" + \
                f"{d2.title}{split}{d2.message}{split}{d2.image_path}{split}" + \
                f"{d3.title}{split}{d3.message}{split}{d3.image_path}"



class QuestTree:
    """ Recursive tree implementation of a branching quest line.

    Attributes:
    - current_node: the root node of this tree.
    - paths: the possible nodes the user can traverse to.

    TODO: representation invariants
    """

    current_node: SituationNode
    paths: dict[str, QuestTree]

    def __init__(self, node: SituationNode) -> None:
        """ Initializes a new quest tree.
        """

        self.current_node = node
        self.paths = {}

    def get_identifier(self) -> str:
        """ TODO
        """

        return self.current_node.id

    def add_path(self, path: QuestTree) -> None:
        """ Adds a quest tree to this tree's possible paths.
        """

        if path.get_identifier() not in self.paths:
            self.paths[path.get_identifier()] = path

    def get_path(self, id: str) -> QuestTree:
        """ TODO
        """

        if id in self.paths:
            return self.paths[id]
        else:
            return None

    def return_dialogue(self) -> Dialogue:
        """Returns the node's dialogue.
        """
        return self.current_node.dialogue[constants.Context.ENTER].return_dialogue()
        
    def serialize(self, output_file: str) -> None:
        """ Converts and writes this tree and its children as a .csv file at output_file.
        Each line of the .csv file represents an individual path through this tree.
        """

        with open(output_file, "a") as file:
            self._serialize_helper(file, "")

    def _serialize_helper(self, file: TextIOWrapper, current_line: str) -> None:
        """ Recursive helper function to write individual paths.
        """
    
        # Append the current node as serialized data to the accumulator.
        # String formatting f"<string>" is used here. 
        current_line += f"{self.current_node.serialize()},"

        # Base case: when there are no more children, write the value of the accumulator.
        if len(self.paths) == 0:  
            file.write(f"{current_line}\n")
        else:
            # Recursive step: keep accumulating node data along each path.
            for path in self.paths:
                path._serialize_helper(file, current_line)
