from enum import Enum


class Biome(Enum):
    """ Possible biomes a node is allowed to take. Generally dictates which nodes are allowed to connect with each other.
    """

    TEMPERATE = 1,
    FRIGID = 2, 
    TROPICAL = 3
    ARID = 4,
    URBAN = 5


class Context(Enum):
    """ Possible contexts a node's dialogue can take.

    Contexts are as follows:
    - ENTER: when the user enters a node.
    - STAY: when the user is analyzing a node's paths.
    - EXIT: when the user leaves a node.
    """

    ENTER = 1,
    STAY = 2,
    EXIT = 3