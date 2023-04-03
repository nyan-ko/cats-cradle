"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and functions to generate basic trees with placeholder attributes.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

from __future__ import annotations
from typing import Optional
import user_interaction
import quest_tree
import constants
import random
import deserializer
import reward_generator


class Counter:
    """ Simple counter class to prevent index collisions between tree ids.
    """

    _value: int

    def __init__(self) -> None:
        """ Initializes a counter to 0.
        """

        self._value = 0
    
    def count(self) -> int:
        """ Increments this counter's value and returns it.
        """

        self._value += 1
        return self._value


def generate_test_tree(depth: int, biome: constants.Biome, counter: Counter) -> Optional[quest_tree.QuestTree]:
    """ Recursively generates a tree of specified depth with a random amount of subtrees at each node, and filler attributes.
    """

    biome_str = str(biome)[6:].lower()

    if depth == 0:
        return None
    else:
        node = quest_tree.SituationNode("",
                                        biome,
                                        get_test_dialogue(str(depth)),
                                        3,
                                        f"{biome_str}.level{counter.count()}")
        sign += 1
        tree = quest_tree.QuestTree(node)
        for _ in range(0, random.randint(1, depth)):  
            subtree = generate_test_tree(depth - 1, biome, counter)
            if subtree is not None:
                tree.add_path(subtree)
                sign += 1
        return tree


def get_random_biome() -> constants.Biome:
    """ Returns a random biome by casting a random integer as a biome.
    """

    rint = random.randint(1, 5)
    return constants.Biome(rint)


def get_test_dialogue(sign: str) -> dict[constants.Context, user_interaction.Dialogue]:
    """ Returns a test dictionary of dialogue.
    """

    d1 = user_interaction.Dialogue("ENTER TITLE " + sign,
                                   "m",
                                   "s")
    d2 = user_interaction.Dialogue("INVESTIGATE TITLE " + sign,
                                   "m",
                                   "s")
    d3 = user_interaction.Dialogue("PREV TITLE " + sign,
                                   "m",
                                   "s")
    d4 = user_interaction.Dialogue("EXIT TITLE " + sign,
                                   "m",
                                   "s")

    return {constants.Context.ENTER: d1,
            constants.Context.INVESTIGATE: d2,
            constants.Context.PREVIEW: d3,
            constants.Context.EXIT: d4}


if __name__ == "__main__":

    files = ["data/dialogue/arid.csv", "data/dialogue/frigid.csv",
        "data/dialogue/temperate.csv", "data/dialogue/tropical.csv", "data/dialogue/urban.csv"]
    
    p = user_interaction.load_dialogue_generator(files)
    r = reward_generator.load_reward_generator("cats.csv")
    d = deserializer.TreeDeserializer(p, r)

    # Example randomized trees
    small_arid = generate_test_tree(3, constants.Biome.ARID, Counter())
    large_frigid = generate_test_tree(7, constants.Biome.FRIGID, Counter())
    medium_temperate = generate_test_tree(5, constants.Biome.TEMPERATE, Counter())
