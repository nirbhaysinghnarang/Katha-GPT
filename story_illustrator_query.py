from story_characters import StoryCharacters
from story_config import StoryConfig
from page import Page
from langchain import PromptTemplate

from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values

# Load the OpenAI API key from the .env file
API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")

class StoryIllustratorQuery:
    """
    A class for generating prompts to instruct an image generator using a story page and character descriptions.

    This class is designed to create prompts for instructing an image generator, such as DALL-E, using a story page
    and a JSON file containing character descriptions. The generated prompt provides detailed instructions for
    generating an image of a scene from the story.

    Attributes:
        page (Page): The page from the story that will be used in the prompt.
        story_characters (StoryCharacters): An instance of StoryCharacters containing character descriptions.
        llm (ChatOpenAI): The language model used for generating prompts.

    Example usage:

    >>> from story_characters import StoryCharacters
    >>> from story_config import StoryConfig
    >>> from page import Page
    >>> page_instance = Page(content="Once upon a time...")
    >>> character_analyzer = StoryCharacters(story_instance)
    >>> query = StoryIllustratorQuery(page_instance, character_analyzer)
    >>> prompt = query.generatePrompt()
    >>> print(prompt)
    """

    def __init__(self, page: Page, story_characters: StoryCharacters, config:StoryConfig):
        """
        Initialize a StoryIllustratorQuery instance.

        Args:
            page (Page): The page from the story that will be used in the prompt.
            story_characters (StoryCharacters): An instance of StoryCharacters containing character descriptions.
        """
        self.page = page
        self.story_characters = story_characters
        self.config = config
        self.llm = ChatOpenAI(temperature=0.0, openai_api_key=API_KEY)

    def generatePrompt(self):
        """
        Generate a detailed prompt for instructing an image generator.

        The generated prompt combines information from the story page and character descriptions
        to create instructions for generating an image of a scene from the story.

        Returns:
            str: The generated prompt.

        Example usage:

        >>> prompt = query.generatePrompt()
        >>> print(prompt)
        """
        prompt = PromptTemplate.from_template("""
        You are a helpful AI assistant. 
        Your goal is to take a page from a story and a JSON file containing 
        descriptions of characters in the story and output a prompt that will be 
        fed to an image generator such as DALL-E to generate an image for the scene. 
        Here is the page {page} and here is the JSON {json}. 
        The image should be {color} and in this style {style}.
        Do not make the prompt flowery or long. Describe the physical 
        characteristics using the json succintly. The resulting prompt should 
        not give directives, it should just describe the scene. It should also be two sentences
        at most and should not include any narrative. Include the color and style at the end with commas.
        """)

        
        formatted = prompt.format(
            page=self.page.content.text, 
            json=self.story_characters.json,
            color=self.config.color,
            style=self.config.img_style
        )
        return self.llm.predict(formatted)
