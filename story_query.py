from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from dotenv import dotenv_values

API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")

class StoryQuery:
    """
    Convenience class to transform a query into a request for a story.

    This class provides a convenient way to transform a given query into a user request
    to hear a story. It utilizes a language model to generate a transformed query.

    Attributes:
        query (str): The original query.
        llm (OpenAI): The language model used for transformation.
        prompt_template (PromptTemplate): A template for generating transformation prompts.

    Example usage:

    >>> query = "Tell me about adventure."
    >>> story_query = StoryQuery(query)
    >>> transformed_query = story_query.transform_prompt()
    >>> print(transformed_query)
    """

    def __init__(self, query):
        """
        Initialize a StoryQuery instance.

        Args:
            query (str): The original query.
        """
        self.llm = OpenAI(temperature=0.0, openai_api_key=API_KEY)
        self.prompt_template = PromptTemplate.from_template("""
            You are an AI model.
            Your goal is to take the query given to you and 
            convert it to a query that represents the user asking to hear about a story. 
            This is the query {query}""")
        self.query = query

    def transform_prompt(self):
        """
        Transform the original query into a request for a story.

        Returns:
            str: The transformed query representing a user request to hear a story.

        Example usage:

        >>> transformed_query = story_query.transform_prompt()
        >>> print(transformed_query)
        """
        return self.llm(self.prompt_template.format(query=self.query))
