from enum import Enum
from langchain import PromptTemplate

class AgeRange(Enum):
    """
    Represents the possible age range reprs for a story config.
    """
    PRETEEN="preteens"
    TEEN="teenagers"
    ADULT="adults"

class Language(Enum):
    """
    Represents the possible language reprs for a story config.
    """
    ENGLISH = "English"
    HINDI = "Hindi"


class ImageGenStyle(Enum):
    """
    Possible image generation styles for a story
    """
    HYPER = "Hyperrealistic"
    WATER = "Watercolor"
    COMIC = "Comic"

class Color(Enum):
    """
    Possible color configs
    """
    BW  = "Black and White"
    COLOR = "Color"


class PageSz(Enum):
    """
    Possible page sizes (text length)
    """
    SM = "small" 
    MD = "medium"
    LG = "large"

class StoryConfig:
    """
    Represents the configuration of a story.
    """
    def __init__(self, age:AgeRange, language:Language, text:str, img_style:ImageGenStyle, color:Color=Color.COLOR, sz:PageSz=PageSz.LG):
        self.age = age
        self.language = language
        self.text = text
        self.img_style = img_style
        self.color = color
        self.sz = sz

    def get_prompt(self):
        """
        Generates a prompt to build a story with this configuration
        """
        prompt = PromptTemplate.from_template("""
            Can you convert the following text into a story in {language} consisting of a sequence of segments?
            Separate each segment with two new lines. Do not include segment headers.
            Make each segment {size} in size
            The target age for this story is {age} 
            {text}
        """)
        return prompt.format(language=self.language, age=self.age, text=self.text, size=self.sz)
         
