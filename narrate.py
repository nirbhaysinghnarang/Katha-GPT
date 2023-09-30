import torch
from TTS.api import TTS
from page import Page
class Narrate:
    """
    Transcribe text to speech
    """
    def __init__(self, page:Page):
        self.page = page
        self.model_name = TTS().list_models()[0]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(self.model_name).to(self.device)
    

    def talk(self):
        return self.tts.tts(self.page.content, speaker=self.tts.speakers[0], language=self.tts.languages[0])
