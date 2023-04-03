"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and functions to deserialize trees for the quest lines.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""
from __future__ import annotations
import random
import csv
from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue, DialogueGenerator
from constants import Biome, Context
from reward_generator import RewardGenerator


class TreeDeserializer:
    """ Representation of the deserialiser for the quest lines that will be generated as trees.

    Instance Attributes:
        - dialogue: the generator for the dialogue in the quest line
        - reward: the generator for the reward that the user might gain from the quest line
    """

    dialogue: DialogueGenerator
    reward: RewardGenerator

    def __init__(self, dialogue: DialogueGenerator, reward: RewardGenerator) -> None:
        """ Initialise the deserializer using the given dialogue and reward parameters.
        """

        self.dialogue = dialogue
        self.reward = reward

    def deserialize_tree(self, input_file: str) -> QuestTree:
        """ Returns a QuestTree, given an input file.
        """

        with open(input_file, "r") as file:
            lines = list(csv.reader(file))
            return self._deserialize_tree_helper(lines, 0, 0)[0]

    def get_random_tree(self, input_files: list[str]) -> QuestTree:
        """ Return a random tree that is generated from a random input file from the given list of input_files.
        """

        return self.deserialize_tree(random.choice(input_files))

    def _deserialize_tree_helper(self, lines: list[list[str]], line_num: int, depth: int) -> tuple[QuestTree, int]:
        """ Returns the created quest tree given the lines, number of lines and depth.
        """

        current_depth = max(lines[line_num][0].count("|") - 1, 0)
        serialized_node = lines[line_num][depth]

        if depth == len(lines[line_num]) - 1:
            node = self._deserialize_node(serialized_node)

            return (QuestTree(node), 0)
        else:
            node = self._deserialize_node(serialized_node)

            tree = QuestTree(node)

            (main_path, peeked) = self._deserialize_tree_helper(lines, line_num, depth + 1)
            tree.add_path(main_path)

            peek = peeked + 1
            while line_num + peek < len(lines) and lines[line_num + peek][0].count("|") - 1 == depth + current_depth:
                (subpath, subpeeked) = self._deserialize_tree_helper(lines, line_num + peek, 1)
                peek += subpeeked + 1
                tree.add_path(subpath)

            return (tree, peek - 1)

    def _deserialize_node(self, data: str) -> SituationNode:
        """ Returns a SituationNode with its necessary parameters, after reading and splitting the given data.
        """

        split = "_"

        contents = data.split(split)

        _id = contents[0]
        biome = Biome(int(contents[1]))
        flag = int(contents[2])

        index = 3

        if flag & 1 == 0:  # Reward was *not* randomly generated => read it from file
            reward = contents[index]
            index += 1
        else:
            reward = self._generate_reward(biome)

        if flag & 2 == 0:  # Ditto for dialogue
            dialogue = self._deserialize_node_dialogue(contents[index])
        else:
            dialogue = self._generate_dialogue(biome)

        return SituationNode(reward, biome, dialogue, flag, _id)

    def _generate_dialogue(self, biome: Biome) -> dict[Context, Dialogue]:
        """ Return a mapping of the Contexts and Dialogues for a given Biome.
        """

        get_message = lambda context: self.dialogue.get_random_message(biome, context)

        return {
            Context.ENTER: Dialogue("Entering a new area...", get_message(Context.ENTER), None),
            Context.INVESTIGATE: Dialogue("Searching around...", get_message(Context.INVESTIGATE), None),
            Context.PREVIEW: Dialogue("Looking ahead...", get_message(Context.PREVIEW), None),
            Context.EXIT: Dialogue("Leaving the area...", get_message(Context.EXIT), None)
        }

    def _generate_reward(self, biome: Biome) -> str:
        """ Return the possible reward for the given Biome.
        """

        return self.reward.get_possible_reward(biome)

    def _deserialize_node_dialogue(self, dialogue: str) -> dict[Context, Dialogue]:
        """ Return a mapping of the Contexts and Dialogues for a given dialogue dataset.
        """

        split = "~"

        contents = dialogue.strip('"').split(split)

        entry_dialogue = Dialogue(contents[0], contents[1], contents[2])
        inv_dialogue = Dialogue(contents[3], contents[4], contents[5])
        prev_dialogue = Dialogue(contents[6], contents[7], contents[8])
        exit_dialogue = Dialogue(contents[9], contents[10], contents[11])

        return {
            Context.ENTER: entry_dialogue,
            Context.INVESTIGATE: inv_dialogue,
            Context.PREVIEW: prev_dialogue,
            Context.EXIT: exit_dialogue
        }


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
    })
