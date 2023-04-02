import discord
from dataclasses import dataclass
from typing import Optional
import discord


class Dialogue:
    """Generic display of text and image.

    Attributes:
    - message: the text content, or None. Supports same text formatting as Discord.
    - image_path: the url for the image, or None. Direct image links (e.g. Imgur) are preferred.

    TODO: invariants
    """

    title: Optional[str]
    message: Optional[str]
    image_path: Optional[str] = None

    def __init__(self, title: Optional[str], message: Optional[str], image_path: Optional[str]) -> None:
        self.title = title
        self.message = message
        self.image_path = image_path

    def __eq__(self, __value: object) -> bool:
        """ TODO
        """

        if isinstance(__value, Dialogue):
            return self.title == __value.title and \
            self.message == __value.message and \
            self.image_path == __value.image_path
        return False

    def return_dialogue(self, colour: Optional[discord.Colour] = None) -> discord.Embed:
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
