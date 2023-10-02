from enum import Enum
from langchain import PromptTemplate
import hashlib

class AgeRange(Enum):
    """
    Represents the possible age ranges for a story configuration.
    """
    PRETEEN = "preteens"
    TEEN = "teenagers"
    ADULT = "adults"

class Language(Enum):
    """
    Represents the possible languages for a story configuration.
    """
    ENGLISH = "English"
    HINDI = "Hindi"

class ImageGenStyle(Enum):
    """
    Represents the possible image generation styles for a story configuration.
    """
    HYPER = "Hyperrealistic"
    WATER = "Watercolor"
    COMIC = "Comic book panel, illustrated by Steve Ditko"

class Color(Enum):
    """
    Represents the possible color configurations for a story.
    """
    BW = "Black and White"
    COLOR = "Color"

class PageSz(Enum):
    """
    Represents the possible page sizes (text length) for a story configuration.
    """
    SM = "small"
    MD = "medium"
    LG = "large"

class StoryConfig:
    """
    Represents the configuration of a story.

    This class is used to define the configuration settings for generating a story.
    It includes information about age range, language, text content, image generation style,
    color configuration, and page size.

    Attributes:
        age (AgeRange): The target age range for the story.
        language (Language): The language of the story.
        text (str): The text content for the story.
        img_style (ImageGenStyle): The style of image generation for the story.
        color (Color, optional): The color configuration for the story (default is Color.COLOR).
        sz (PageSz, optional): The page size (text length) for each segment (default is PageSz.LG).

    Example usage:

    >>> from story_config import AgeRange, Language, ImageGenStyle, Color, PageSz
    >>> age = AgeRange.TEEN
    >>> language = Language.ENGLISH
    >>> text = "Once upon a time..."
    >>> img_style = ImageGenStyle.HYPER
    >>> config = StoryConfig(age, language, text, img_style)
    >>> prompt = config.get_prompt()
    >>> print(prompt)
    """

    def __init__(self, age: AgeRange, language: Language, text: str, img_style: ImageGenStyle, color: Color = Color.COLOR, sz: PageSz = PageSz.LG):
        """
        Initialize a StoryConfig instance.

        Args:
            age (AgeRange): The target age range for the story.
            language (Language): The language of the story.
            text (str): The text content for the story.
            img_style (ImageGenStyle): The style of image generation for the story.
            color (Color, optional): The color configuration for the story (default is Color.COLOR).
            sz (PageSz, optional): The page size (text length) for each segment (default is PageSz.LG).
        """
        self.age = age
        self.language = language
        self.text = text
        self.img_style = img_style
        self.color = color
        self.sz = sz
        self.hasher = hashlib.sha3_512()
        self.hasher.update(bytes(self.text, "utf-8"))
        self.text_id = self.hasher.hexdigest()

    def to_json(self):
        """
        Serialize the StoryConfig object to a JSON-serializable dictionary.

        Returns:
            dict: A JSON-serializable dictionary representing the StoryConfig object.
        """
        return {
            "age": self.age,
            "language": self.language,
            "text": self.text,
            "img_style": self.img_style,
            "color": self.color,
            "sz": self.sz,
            "text_id": self.text_id
        }

    def get_prompt(self):
        """
        Generates a prompt to build a story with this configuration.

        Returns:
            str: The generated prompt.
        """
        prompt = PromptTemplate.from_template("""
            Can you convert the following text into a story in {language} consisting of a sequence of segments?
            Separate each segment with two new lines. Do not include segment headers.
            Make a scene for each segment, with dialogues for characters in the segment.
            Make each segment {size} in size. Make it elaborate and descriptive.
            The target age for this story is {age}.
            {text}
        """)
        return prompt.format(language=self.language, age=self.age, text=self.text, size=self.sz)
