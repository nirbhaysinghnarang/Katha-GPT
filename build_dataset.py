"""
This script will generate 
"""
import requests
import os
from story_config import StoryConfig
from story_config import AgeRange
from story_config import Language
from story import Story
from pathlib import Path



text = """
Laura Gibbs · 1. Vyasa Seeks a Scribe
Vyasa had composed a poem and needed a scribe to write it down."Will you be my scribe?" he asked Ganesha, the elephant-headed god."I will," said Ganesha, "provided you do not pause in your recitation.""I agree," Vyasa replied, "provided you understand each word's meaning before you write it down."Vyasa recited, and Ganesha wrote.Sometimes Vyasa said things that were confusing, and Ganesha would pause and think.Once, when Ganesha's pen splintered, he broke off one of his own tusks to keep writing. That was the first version of the Mahabharata.This Mahabharata will begin with King Shantanu.
"""

ages = [AgeRange.ADULT, AgeRange.PRETEEN, AgeRange.TEEN]
langs = [Language.ENGLISH, Language.HINDI]

for age in ages:
    for lang in langs:
        config = StoryConfig(age, lang, text, 5)
        story = Story(config)
        story.build_story()
        story.build_pages()
        for (i,page) in enumerate(story.pages):
            url = page.content.imageURL
            response = requests.get(url)
            img_path = f'img/{str(config)}/{(i+1)}.png'
            p = Path(img_path)
            if not p.exists():
                p.parent.mkdir(parents=True)
            with open(img_path, "wb") as img_file:
                img_file.write(response.content)
                page.content.imageURL = img_path
            page.content.imageURL = img_path


        print(age, lang, story.pages)

        