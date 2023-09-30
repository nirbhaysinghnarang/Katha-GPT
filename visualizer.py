import streamlit as st
from story_retriever import StoryRetriever
from story_config import StoryConfig
from story import Story
from story_config import ImageGenStyle
from story_characters import StoryCharacters
from story_illustrator import StoryIllustrator
import logging



st.title('Katha GPT Visualizer')


query = st.sidebar.text_input('Query', type='default')
age = st.sidebar.radio(
    "Age Range",
    options=[
        "Preteens",
        "Teens",
        "Adult"
    ]
)

language = st.sidebar.radio(
    "Language",
    options=[
        "English",
        "Hindi"
    ],
)

img_gen_style = st.sidebar.radio(
    "Image Generation",
    options=[
        "Hyperrealistic",
        "Watercolor",
        "Comic",
    ]
)

color = st.sidebar.radio(
    "Color",
    options=[
        "Black and White",
        "Color"
    ]
)

size = st.sidebar.radio(
    "Page Size",
    options=[
        "large",
        "med",
        "small"
    ]
)

submit = st.sidebar.button("Submit", type="primary")


if submit and query:
    most_relevant_content = StoryRetriever(query).retrieve()
    config = StoryConfig(
	    age,
	    language, 
	    most_relevant_content, 
	    img_gen_style,
        color,
        size
	)
    story = Story(config=config)
    story.build_story()
    logging.info(story.text)
    story.build_pages()
    story.pages = [story.pages[0]]
    characters = StoryCharacters(story)
    characters.fetchCharacters()
    illustrator = StoryIllustrator(story, config, characters)
    illustrator.populateStore()
    story.populate_images(illustrator)
    logging.info("Finished generating and populating images...rendering.\n\n\n")
    story.save_json()
    st.title("Generated Story")
    for (i,page) in enumerate(story.pages):
        st.write(f"Page {i+1}")
        st.image(page.content.imageURL)
        st.write(page.content.text)
        "---"
    st.title("Source")
    st.write(most_relevant_content)



