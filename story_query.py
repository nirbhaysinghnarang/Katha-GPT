from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

import streamlit as st

API_KEY = st.secrets["OPEN_AI_KEY"]

class StoryQuery:
    def __init__(self, query):
        self.llm = OpenAI(temperature=0.0, openai_api_key=API_KEY)
        self.prompt_template = PromptTemplate.from_template("You are an AI model. Your goal is to take the query given to you and convert it to a query that represents the user asking to hear about a story. This is the query {query}")
        self.query = query

    def transform_prompt(self):
        """
        Transforms [self.query] into a query representing 
        the user asking to hear a story.
        """
        return self.llm(self.prompt_template.format(query=self.query))
