"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains the code necessary to run the bot on Discord.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""

import bot
from user import User
from deserializer import TreeDeserializer
from biome_generator import BiomeGenerator
import user_interaction
import reward_generator

###############################################################################
# Initilizing the bot as a CatsCradle object (find this class in the bot.py
# file) and running the bot token.
###############################################################################

if __name__ == "__main__":
    files = ["data/dialogue/arid.csv", "data/dialogue/frigid.csv",
        "data/dialogue/temperate.csv", "data/dialogue/tropical.csv", "data/dialogue/urban.csv"]
    
    p = user_interaction.load_dialogue_generator(files)
    r = reward_generator.load_reward_generator("cats.csv")
    d = TreeDeserializer(p, r)
    
    b = bot.CatsCradle(User(), TreeDeserializer(p, r), BiomeGenerator())
    b.run('token')
