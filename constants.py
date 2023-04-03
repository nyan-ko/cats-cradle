"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes to represent the constants used by the bot.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

from enum import Enum


class Biome(Enum):
    """Possible biomes a node is allowed to take. Generally dictates which nodes are allowed to connect with each other.
    """

    TEMPERATE = 1
    FRIGID = 2
    TROPICAL = 3
    ARID = 4
    URBAN = 5


class Context(Enum):
    """Possible contexts a node's dialogue can take.

    Contexts are as follows:
    - ENTER: when the user enters a node.
    - INVESTIGATE: when the user is analyzing a node's paths.
    - PREVIEW: when the user is viewing this node from a parent node.
    - EXIT: when the user leaves a node.
    """

    ENTER = 1
    INVESTIGATE = 2
    PREVIEW = 3
    EXIT = 4


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
    })