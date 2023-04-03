from __future__ import annotations
import user_interaction
import quest_tree
import constants
import random
import deserializer


START = 1
END = 5
sign = 0

files = ["data/dialogue/arid.csv", "data/dialogue/frigid.csv",
        "data/dialogue/temperate.csv", "data/dialogue/tropical.csv", "data/dialogue/urban.csv"]

p = user_interaction.load_dialogue_generator(files)
d = deserializer.TreeDeserializer(p)


def helper(depth: int, biome: constants.Biome) -> quest_tree.QuestTree:

    global sign
    sign = 0

    tree = generate_test_tree(depth, biome)
    print(f"length: {len(tree)}")

    return tree

def generate_test_tree(depth: int, biome: constants.Biome) -> quest_tree.QuestTree:
    """ Recursively generates a tree of specified depth with a random amount of subtrees at each node, and filler attributes.
    """

    biome_str = str(biome)[6:].lower()
    global sign

    if depth == 0:
        return None
    else:
        node = quest_tree.SituationNode("None",
                                        biome,
                                        get_test_dialogue(str(depth)),
                                        False,
                                        f"{biome_str}.level{sign}")
        sign += 1
        tree = quest_tree.QuestTree(node)
        for i in range(0, random.randint(1, depth)):  # Generate a random number of subtrees in terms of the remaining depth.
            subtree = generate_test_tree(depth - 1, biome)
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


def get_random_id(sign: str) -> str:
    global START
    global END
    r = random.randrange(START, END)
    START, END = END, END + r
    return f"{sign}{r}"
