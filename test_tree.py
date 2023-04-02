import user_interaction
import quest_tree
import constants
import random


START = 1
END = 5

def generate_test_tree(depth: int) -> quest_tree.QuestTree:
    """ Recursively generates a tree of specified depth with a random amount of subtrees at each node, and filler attributes.
    """

    if depth == 0:
        return None
    else:
        node = quest_tree.SituationNode("reward",
                                        get_random_biome(),
                                        get_test_dialogue(str(depth)),
                                        get_random_id("help"))
        tree = quest_tree.QuestTree(node)
        for i in range(0, random.randint(1, depth)):  # Generate a random number of subtrees in terms of the remaining depth.
            subtree = generate_test_tree(depth - 1)
            if subtree is not None:
                tree.add_path(subtree)
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
    d3 = user_interaction.Dialogue("EXIT TITLE " + sign,
                                   "m",
                                   "s")

    return {constants.Context.ENTER: d1,
            constants.Context.INVESTIGATE: d2,
            constants.Context.EXIT: d3}    


def get_random_id(sign: str) -> str:
    global START
    global END
    r = random.randrange(START, END)
    START, END = END, END + r
    return f"{sign}{r}"