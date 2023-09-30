from json import JSONEncoder
from page_content import PageContent

class Page:
    """
    Represents a page in a story.

    This class is used to represent a page in a story and includes information about the
    page's content and page number.

    Attributes:
        content (PageContent): The content of the page, typically containing text and image information.
        pageNo (int): The page number within the story.

    Example usage:

    >>> from page_content import PageContent
    >>> content = PageContent(text="Once upon a time...", imageURL="https://example.com/image.jpg")
    >>> page_instance = Page(content, pageNo=1)
    >>> print(page_instance.content.text)
    >>> print(page_instance.pageNo)
    """
    def __init__(self, content: PageContent, pageNo):
        """
        Initialize a Page instance.

        Args:
            content (PageContent): The content of the page, typically containing text and image information.
            pageNo (int): The page number within the story.
        """
        self.content = content
        self.pageNo = pageNo


    def to_json(self):
        """
        Returns a json representation of the object
        """

        return {
            "content":self.content.to_json(),
            "pageNo":self.pageNo
        }