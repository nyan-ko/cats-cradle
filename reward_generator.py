"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and functions to deserialize trees for the quest lines.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""
from __future__ import annotations
from constants import Biome
import csv
import random

class RewardGenerator:
    """
    """

    rewards: dict[Biome, list[str]]
    emotes: dict[str, str]

    def __init__(self, rewards: dict[Biome, list[str]], emotes: dict[str, str]) -> None:
        """
        """

        self.rewards = rewards
        self.emotes = emotes

    def get_possible_reward(self, biome: Biome) -> str:
        """
        """

        if random.random() <= 0.8:
            return ""
        else:
            return random.choice(self.rewards[biome])

    def get_emote(self, cat: str) -> str:
        """
        """

        return self.emotes[cat]


def load_reward_generator(file_path: str) -> RewardGenerator:
    """
    """

    rewards_so_far = {Biome.ARID: [],
                      Biome.FRIGID: [],
                      Biome.TEMPERATE: [],
                      Biome.TROPICAL: [],
                      Biome.URBAN: []}
    emotes_so_far = {}

    with open(file_path, "r") as file:
        reader = csv.reader(file)

        for line in reader:
            cat_name = line[0]
            emote = line[1]
            biome = Biome(int(line[2]))
            rewards_so_far[biome].append(cat_name)
            emotes_so_far[cat_name] = emote

    return RewardGenerator(rewards_so_far, emotes_so_far)
