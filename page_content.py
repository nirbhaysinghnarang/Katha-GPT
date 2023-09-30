class PageContent:
    """
    Encapsulates the content of a page.

    This class represents the content of a page in a story, including text and an optional image URL.

    Attributes:
        text (str): The text content of the page.
        imageURL (str, optional): The URL of an image associated with the page (default is None).

    Example usage:

    >>> content = PageContent(text="Once upon a time...", imageURL="https://example.com/image.jpg")
    >>> print(content.text)
    >>> print(content.imageURL)
    """
    def __init__(self, text, imageURL=None):
        """
        Initialize a PageContent instance.

        Args:
            text (str): The text content of the page.
            imageURL (str, optional): The URL of an image associated with the page (default is None).
        """
        self.text = text
        self.imageURL = imageURL
