from json import JSONEncoder
from page_content import PageContent

class Page:
    """Represents a page"""
    def __init__(self, content:PageContent, pageNo):
        self.content = content
        self.pageNo = pageNo