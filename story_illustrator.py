from story_config import StoryConfig
from dotenv import dotenv_values
from collections import defaultdict
from story_illustrator_query import StoryIllustratorQuery
import requests
import json
import time

# Load the OpenAI API key from the .env file
API_KEY = dotenv_values(".env").get("MJ_API_KEY")


class StoryIllustrator:
    """
    A class for generating illustrations for a story using the OpenAI API.

    This class allows you to generate illustrations for each page of a story based on
    provided configuration settings.

    Attributes:
        story (Story): The story for which illustrations are generated.
        config (StoryConfig): Configuration settings for generating illustrations.
        store (defaultdict): A dictionary to store generated image URLs.

    Example usage:

    >>> from story_config import StoryConfig
    >>> config = StoryConfig(color="vibrant", img_style="fantasy")
    >>> illustrator = StoryIllustrator(story_instance, config)
    >>> illustrator.populateStore()
    >>> print(illustrator.store)
    """

    def __init__(self, story, config, story_characters):
        """
        Initialize a StoryIllustrator instance.

        Args:
            story (Story): The story for which illustrations are generated.
            config (StoryConfig): Configuration settings for generating illustrations.
        """
        self.story = story
        self.config = config
        self.pages = self.story.pages
        self.story_characters = story_characters
        self.store = defaultdict()
        self.imagine_url = 'https://api.thenextleg.io/v2/imagine'
        print(API_KEY)


    def getMessageId(self, prompt):
        payload = json.dumps({
        "msg": prompt,
        "ref": "",
        "webhookOverride": "", 
        "ignorePrefilter": "false"
        })
        headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
        }

        return json.loads(requests.request("POST", self.imagine_url, headers=headers, data=payload).text)['messageId']

    def getMessageUrl(self, messageId):
        return  f"https://api.thenextleg.io/v2/message/{messageId}?expireMins=2"

    def getImage(self, prompt):
        messageId = self.getMessageId(prompt)
        messageUrl = self.getMessageUrl(messageId)
        headers = {
        'Authorization': f'Bearer {API_KEY}',
        }
        response=json.loads(requests.request("GET", messageUrl, headers=headers).text)

        while response['progress']!=100:
            response = json.loads(requests.request("GET", messageUrl, headers=headers).text)
            time.sleep(5)
        return response['response']["imageUrls"][0]


    def getUrl(self, response):
        """
        Extract the URL from the OpenAI API response.

        Args:
            response (dict): The response from the OpenAI API.

        Returns:
            str: The URL of the generated image.

        Example usage:

        >>> response = {...}  # OpenAI API response
        >>> url = self.getUrl(response)
        >>> print(url)
        """
        return response['data'][0]['url']

    def generateImage(self, pageNo: int):
        """
        Generate an illustration for a specific page of the story.

        Args:
            pageNo (int): The page number for which to generate the illustration.

        Example usage:

        >>> illustrator.generateImage(0)
        """
        page = self.pages[pageNo]

        illustratorQuery = StoryIllustratorQuery(page, self.story_characters, self.config)
        prompt = illustratorQuery.generatePrompt()
        print(f"Prompt:{prompt}")
        imgUrl = self.getImage(prompt)
        self.store[pageNo] = imgUrl

    def populateStore(self):
        """
        Generate illustrations for all pages of the story and store their URLs in the 'store' dictionary.

        Example usage:

        >>> illustrator.populateStore()
        >>> print(illustrator.store)
        """
        for n in range(len(self.pages)):
            print(f"On page {n}/{len(self.pages)-1}")
            self.generateImage(n)
