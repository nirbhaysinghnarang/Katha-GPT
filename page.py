from json import JSONEncoder
from page_content import PageContent

class Page(JSONEncoder):
    """Represents a page"""
    def __init__(self, content:PageContent, pageNo):
        super().__init__()
        self.content = content
        self.pageNo = pageNo

    def default(self, o):
        return o.__dict__
