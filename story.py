import logging
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import dotenv_values

from page import Page
from page_content import PageContent
from story_config import StoryConfig
API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")
openai.api_key = API_KEY

"""Classes to represent and build a story"""

class Story:
    """
    Represents a story
    """
    def __init__(self, config:StoryConfig):
        self.config = config
        self.pages = []
        self.llm = ChatOpenAI(
            openai_api_key=API_KEY,
            temperature=0.0
        )
       
    def build_story(self):
        """
        Given a config, builds a story.
        """
        return self.llm.predict(self.config.get_prompt())

    def build_pages(self):
        """
        Populates self.pages
        """
        splitter ='\n\n'
        for (i, text) in enumerate(list(filter(lambda x:x and x!=" ",self.build_story().split(splitter)))):
            response = openai.Image.create(
                prompt=f"A {self.config.color} illustration for the following page from a story: {text}, {self.config.img_style}",
                n=1,
                size="512x512"
            )
            self.pages.append(Page(
                content=PageContent((text), response['data'][0]['url']),
                pageNo=(i+1)
            ))
                


   



        