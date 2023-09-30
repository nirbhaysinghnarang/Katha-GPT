import logging
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from dotenv import dotenv_values
from pathlib import Path
import json

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
        self.text = ""

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

    def to_json(self):
        """
        Serialize the object to JSON.
        """
        return {
            "config":self.config.to_json(),
            "pages":[page.to_json() for page in self.pages],
            
        }

    def save_json(self):
        """
        Serialize the object to a JSON file and save it in the 'story_jsons' directory.

        This method converts the object's attributes to JSON format and saves it in a file
        with a name derived from the StoryConfig attributes. If the 'story_jsons' directory
        does not exist, it will be created.

        Raises:
            ValueError: If the JSON file with the same name already exists, indicating that
                the story configuration has already been generated and saved.

        Example usage:

        >>> story_instance = YourClassName(...)  # Initialize your class
        >>> story_instance.to_json()  # Save the story configuration as JSON
        """
        json_directory = Path.joinpath(Path.cwd(), "story_jsons")
        if not json_directory.exists():
            json_directory.mkdir(parents=True) 
        story_name = f'{self.config.text_id}_{self.config.age}_{self.config.color}_{self.config.img_style}_{self.config.sz}'
        story_path = Path.joinpath(json_directory, f"{story_name}.json")
        if story_path.exists():
            raise ValueError("Story configuration has already been generated and saved.")
        story_path.touch()
        story_json = json.dumps(self.to_json())
        story_path.write_text(story_json, encoding="utf-8")