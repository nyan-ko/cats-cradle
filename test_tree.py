import user_interaction
import quest_tree
import constants
import random


def generate_test_tree(depth: int) -> quest_tree.QuestTree:
    """ Recursively gnerates a tree of specified depth with a random amount of subtrees at each node, and filler attributes.
    """

    if depth == 0:
        return None
    else:
        node = quest_tree.SituationNode("reward",
                                        get_random_biome(),
                                        get_test_dialogue(str(depth)))
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
                                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in odio eu erat dignissim dapibus ac eget tellus. Duis eu sem molestie, commodo eros eu, lacinia tortor. Vestibulum feugiat libero dolor, vel aliquam felis venenatis et. Nullam auctor in elit eget eleifend. Nunc molestie efficitur dui et porttitor. Donec ut laoreet lectus.",
                                   "https://www.shutterstock.com/image-photo/kitten-british-blue-on-white-background-794297041")
    d2 = user_interaction.Dialogue("INVESTIGATE TITLE " + sign,
                                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in odio eu erat dignissim dapibus ac eget tellus. Duis eu sem molestie, commodo eros eu, lacinia tortor. Vestibulum feugiat libero dolor, vel aliquam felis venenatis et. Nullam auctor in elit eget eleifend. Nunc molestie efficitur dui et porttitor. Donec ut laoreet lectus.",
                                   "https://www.shutterstock.com/image-photo/kitten-british-blue-on-white-background-794297041")
    d3 = user_interaction.Dialogue("EXIT TITLE " + sign,
                                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec in odio eu erat dignissim dapibus ac eget tellus. Duis eu sem molestie, commodo eros eu, lacinia tortor. Vestibulum feugiat libero dolor, vel aliquam felis venenatis et. Nullam auctor in elit eget eleifend. Nunc molestie efficitur dui et porttitor. Donec ut laoreet lectus.",
                                   "https://www.shutterstock.com/image-photo/kitten-british-blue-on-white-background-794297041")

    return {constants.Context.ENTER: d1,
            constants.Context.INVESTIGATE: d2,
            constants.Context.EXIT: d3}    
