"""CSC111 Winter 2023 Project: Cat's Cradle

This module contains classes and methods to represent the dialogue generator and related aspects needed for dialogue.

This file is copyright (c) 2023 by Edric Liu, Janet Fu, Nancy Hu, and Lily Meng.
"""
from __future__ import annotations
import discord
from dataclasses import dataclass
from typing import Optional


class Dialogue:
    """Generic display of text and image.

    Instance Attributes:
    - message: the text content, or None. Supports same text formatting as Discord.
    - image_path: the url for the image, or None. Direct image links (e.g. Imgur) are preferred.

    Representation Invariants:
    - self.message is a valid line of dialogue from dialogues.csv.
    """

    title: Optional[str]
    message: Optional[str]
    image_path: Optional[str] = None

    def __init__(self, title: Optional[str], message: Optional[str], image_path: Optional[str]) -> None:
        self.title = title
        self.message = message
        self.image_path = image_path

    def __eq__(self, __value: object) -> bool:
        """Returns True if two Dialogue objects are identical. Returns false if ___value is not a Dialogue object or is
        not equal.
        """
        if isinstance(__value, Dialogue):
            return self.title == __value.title and \
                self.message == __value.message and \
                self.image_path == __value.image_path
        return False

    def _is_pointer(self) -> bool:
        """Returns True if self.message is a pointer (begins with @).
        """
        return self.message[0] == "@"

    def embeddify(self, colour: Optional[discord.Colour] = None) -> discord.Embed:
        """Returns the dialogue in the form of an embedded message.
        """
        embed = discord.Embed(
            colour=colour,
            description=self.message,
            title=self.title
        )
        if self.image_path is not None:
            embed.set_image(url=self.image_path)
        return embed