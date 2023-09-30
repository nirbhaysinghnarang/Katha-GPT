import logging
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from dotenv import dotenv_values

from page import Page
from page_content import PageContent
from story_config import StoryConfig

API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")
openai.api_key = API_KEY

class Story:
    """
    Represents a story.

    This class is used to represent a story and includes methods for building the story,
    creating pages, and populating images for each page.

    Attributes:
        config (StoryConfig): Configuration settings for generating the story.
        pages (list): A list of Page objects representing the story's pages.
        llm (ChatOpenAI): The language model used for generating the story.

    Example usage:

    >>> from story_config import StoryConfig
    >>> config = StoryConfig(...)
    >>> story_instance = Story(config)
    >>> story_instance.build_story()
    >>> story_instance.build_pages()
    >>> print(story_instance.pages)
    """

    def __init__(self, config: StoryConfig):
        """
        Initialize a Story instance.

        Args:
            config (StoryConfig): Configuration settings for generating the story.
        """
        self.config = config
        self.pages = []
        self.llm = ChatOpenAI(
            openai_api_key=API_KEY,
            temperature=0.0
        )

    def build_story(self):
        """
        Build the story based on the provided configuration.
        """
        self.text = self.llm.predict(self.config.get_prompt())

    def build_pages(self):
        """
        Populate self.pages with story pages.

        Each page is created based on the text generated for the story.
        """
        splitter = '\n\n'
        for (i, text) in enumerate(list(filter(lambda x: x and x != " ", self.text.split(splitter)))):
            self.pages.append(Page(
                content=PageContent((text), None),
                pageNo=(i + 1)
            ))

    def populate_images(self, illustrator):
        """
        Populate images for each page in the story using an illustrator.

        Args:
            illustrator: An instance of StoryIllustrator used to fetch images.
        """
        for (i, page) in enumerate(illustrator.store):
            self.pages[i].content.imageURL = illustrator.store[page]
