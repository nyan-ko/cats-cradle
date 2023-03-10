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

    message: Optional[str]
    image_path: Optional[str]