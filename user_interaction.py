import discord
from dataclasses import dataclass
from typing import Optional

@dataclass
class Dialogue:
    """Generic display of text and image.

    Attributes:
    - message: the text content, or None. Supports same text formatting as Discord.
    - image_path: the url for the image, or None. Direct image links (e.g. Imgur) are preferred.

    TODO: invariants
    """

    title: Optional[str]
    message: Optional[str]
    image_path: Optional[str]
    
    def return_dialogue(self, image_url: Optional[str] = None, colour: Optional[discord.Colour] = None) -> discord.Embed:
        """Returns the dialogue in the form of an embedded message.
        """
        embed = discord.Embed(
            colour=discord.Colour.dark_gold(),
            description=self.message,
            title=self.title
        )
        if image_url is not None:
            embed.set_image(url=self.image_path)
        return embed
