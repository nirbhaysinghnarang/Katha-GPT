from story import Story
import json
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values

# Load the OpenAI API key from the .env file
API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")

class StoryCharacters:
    """
    A class for analyzing characters in a story and generating character descriptions using the OpenAI API.

    This class allows you to analyze characters in a given story and generate physical descriptions
    for each character, returning the results as a JSON mapping.

    Attributes:
        story (Story): The story for which character descriptions are generated.
        llm (ChatOpenAI): The language model used for generating descriptions.

    Example usage:

    >>> from story import Story
    >>> story_instance = Story(text="Once upon a time...")
    >>> character_analyzer = StoryCharacters(story_instance)
    >>> character_descriptions = character_analyzer.fetchCharacters()
    >>> print(character_descriptions)
    """

    def __init__(self, story: Story):
        """
        Initialize a StoryCharacters instance.

        Args:
            story (Story): The story for which character descriptions are generated.
        """
        self.story = story
        self.llm = ChatOpenAI(temperature=0.0, openai_api_key=API_KEY)

    def fetchCharacters(self):
        """
        Analyze characters in the story and generate character descriptions as a JSON mapping.

        Returns:
            dict: A JSON mapping from each character in the story to a physical description.

        Example usage:

        >>> character_descriptions = character_analyzer.fetchCharacters()
        >>> print(character_descriptions)
        """
        prompt = PromptTemplate.from_template("""
        Your goal is to analyze the following story {story} 
        and generate a JSON that maps from each character in the story to a physical description that you come up with. 
        The description should be specific and just describe clothing, physical features, and facial features. 
        The description should not be sentences, just comma-separated adjectives.
        For each character, also include a short description for eg. Indian warrior.
        In addition, come up with clothing for each character.
        """)
        formatted = prompt.format(story=self.story.text)
        self.json = json.loads(
            self.llm.predict(
                formatted
            )
        )
        return self.json
