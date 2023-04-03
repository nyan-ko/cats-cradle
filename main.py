"""CSC111 Winter 2023 Project: Cat's Cradle
This module contains classes to represent a quest tree and its nodes.
Methods exist for serialization and deserialization of trees.
This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

import bot
from user import User
from test_tree import p, r
from deserializer import TreeDeserializer
from biome_generator import BiomeGenerator

###############################################################################
# Initilizing the bot as a CatsCradle object (find this class in the bot.py 
# file) and running the bot token.
###############################################################################

b = bot.CatsCradle(User(), TreeDeserializer(p, r), BiomeGenerator())
b.run('MTA4MzI1MDc2NzI1MjY5MzA1NQ.Gs5xjl.iye3xFQcgFtslDBo1gFeecT6j78A2Ws0azwIq8')

