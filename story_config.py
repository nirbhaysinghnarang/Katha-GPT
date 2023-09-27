from enum import Enum
from langchain import PromptTemplate
import time

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


class StoryConfig:
    """
    Represents the configuration of a story.
    """
    
    def __init__(self, age:AgeRange, language:Language, text:str, num_pages):
        self.age = age
        self.language = language
        self.text = text
        self.num_pages = num_pages


    def __str__(self):
        return f"{self.age}_{self.language}_{str(time.time())[:5]}"

    def get_prompt(self):
        """
        Generates a prompt to build a story with this configuration
        """
        prompt = PromptTemplate.from_template("""
            Can you convert the following text into a story in {language} consisting of a sequence of {num_pages} segments?
            Separate each segment with two new lines. 
            The target age for this story is {age} 
            {text}
        """)
        return prompt.format(language=self.language, num_pages=self.num_pages, age=self.age, text=self.text,)
         
