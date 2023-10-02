from story import Story
import json
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from story_config import StoryConfig
from story_config import ImageGenStyle
from dotenv import dotenv_values
import requests
import time
from collections import defaultdict

# Load the OpenAI API key from the .env file
API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")
MJ_API_KEY = dotenv_values(".env").get("MJ_API_KEY")

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

    def __init__(self, story: Story, config:StoryConfig):
        """
        Initialize a StoryCharacters instance.

        Args:
            story (Story): The story for which character descriptions are generated.
        """
        self.story = story
        self.llm = ChatOpenAI(temperature=0.0, openai_api_key=API_KEY)
        self.imagine_url = 'https://api.thenextleg.io/v2/imagine'
        self.characterImages = defaultdict()
        self.character_file = open("character_map.json", 'r+')
        self.character_map = json.loads(self.character_file.read())
        self.config = config



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
        Infer gender and age of each character.
        The keys should be 'description', 'name', 'attire', 'gender', 'age'.
        """)
        formatted = prompt.format(story=self.story.text)
        self.json = json.loads(
            self.llm.predict(
                formatted
            )
        )
        return self.json

    def getMessageId(self, prompt):
        """
        Get a message ID from the NextLeg API for a given prompt.

        Args:
            prompt (str): The prompt to send to the API.

        Returns:
            str: The message ID received from the API.

        Example usage:

        >>> message_id = self.getMessageId("Generate an illustration for a forest scene.")
        >>> print(message_id)
        """
        payload = json.dumps({
        "msg": prompt,
        "ref": "",
        "webhookOverride": "", 
        "ignorePrefilter": "false"
        })
        headers = {
        'Authorization': f'Bearer {MJ_API_KEY}',
        'Content-Type': 'application/json'
        }

        return json.loads(requests.request("POST", self.imagine_url, headers=headers, data=payload).text)['messageId']

    def getMessageUrl(self, messageId):
        """
        Get the message URL for a given message ID.

        Args:
            messageId (str): The message ID for which to get the URL.

        Returns:
            str: The message URL.

        Example usage:

        >>> message_id = "12345"  # Replace with an actual message ID
        >>> message_url = self.getMessageUrl(message_id)
        >>> print(message_url)
        """
        return  f"https://api.thenextleg.io/v2/message/{messageId}?expireMins=2"

    def getImage(self, prompt):
        """
        Get an image URL generated from a given prompt.

        Args:
            prompt (str): The prompt to generate the image from.

        Returns:
            str: The URL of the generated image.

        Example usage:

        >>> prompt = "Generate an illustration of a castle at night."
        >>> image_url = self.getImage(prompt)
        >>> print(image_url)
        """
        messageId = self.getMessageId(prompt)
        messageUrl = self.getMessageUrl(messageId)
        headers = {
        'Authorization': f'Bearer {MJ_API_KEY}',
        }
        response=json.loads(requests.request("GET", messageUrl, headers=headers).text)

        while response['progress']!=100:
            response = json.loads(requests.request("GET", messageUrl, headers=headers).text)
            time.sleep(5)
        print(response['response']['imageUrls'][0])
        return response['response']["imageUrls"][0]

    def _generateCharacterFace(self, character):
        character = self.json[character] 
        assert(all(key in character for key in ['description', 'name','attire', 'gender', 'age']))
        prompt = PromptTemplate.from_template(
            """
            Frontal profile of {character} ({gender}, 
            age:{age}) from the Mahabharat, {description}, wearing {attire}, {style}"""
        )
        return self.getImage(prompt.format(
            character=character['name'], 
            gender=character['gender'],
            age=character['age'],
            description=character['description'], 
            attire=character['attire'],
            style=ImageGenStyle[self.config.img_style].value
            )
        )

    def transformKeysToLowerCase(self):
        #Character names should be case agnostic
        transformed = {}
        for key in self.json:
            transformed[key.lower()] = self.json[key]
        self.json = transformed
        
    def generateCharacterFaces(self):
        self.transformKeysToLowerCase()
        for character in self.json:
            if character in self.character_map:
                print(f"{character} cached...fetching resemblance from memory.")
                self.characterImages[character.lower()] = self.character_map[character.lower]
            else:
                print(f"{character} not seen before...generating resemblance.")
                self.characterImages[character.lower()] = self._generateCharacterFace(character)
                self.character_map[character.lower()] = self.characterImages[character]
        print(f'New character map:{self.character_map}')
        self.character_file.write("") #flush existing contents
        #overwrite with new contents
        self.character_file.write(json.dumps(self.character_map))
        return self.characterImages


