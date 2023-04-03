from __future__ import annotations
from quest_tree import SituationNode, QuestTree
from user_interaction import Dialogue, DialogueGenerator
from constants import Biome, Context
from reward_generator import RewardGenerator
import random
import csv


class TreeDeserializer:
    """
    """

    dialogue: DialogueGenerator
    reward: RewardGenerator

    def __init__(self, dialogue: DialogueGenerator, reward: RewardGenerator) -> None:
        """
        """

        self.dialogue = dialogue
        self.reward = reward

    def deserialize_tree(self, input_file: str) -> QuestTree:
        """
        """

        with open(input_file, "r") as file:
            lines = list(csv.reader(file))
            return self._deserialize_tree_helper(lines, 0, 0)[0]

    def get_random_tree(self, input_files: list[str]) -> QuestTree:
        """
        """

        return self.deserialize_tree(random.choice(input_files))

    def _deserialize_tree_helper(self, lines: list[list[str]], line_num: int, depth: int) -> tuple[QuestTree, int]:
        """
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
        """
        """

        split = "_"

        contents = data.split(split)

        id = contents[0]
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

        return SituationNode(reward, biome, dialogue, flag, id)

    def _generate_dialogue(self, biome: Biome) -> dict[Context, Dialogue]:
        """
        """

        get_message = lambda context: self.dialogue.get_random_message(biome, context)

        return {
            Context.ENTER: Dialogue("Entering a new area...", get_message(Context.ENTER), None),
            Context.INVESTIGATE: Dialogue("Seaching around...", get_message(Context.INVESTIGATE), None),
            Context.PREVIEW: Dialogue("Looking ahead...", get_message(Context.PREVIEW), None),
            Context.EXIT: Dialogue("Leaving the area...", get_message(Context.EXIT), None)
        }

    def _generate_reward(self, biome: Biome) -> str:
        """
        """

        return self.reward.get_possible_reward(biome)

    def _deserialize_node_dialogue(self, dialogue: str) -> dict[Context, Dialogue]:
        """
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
