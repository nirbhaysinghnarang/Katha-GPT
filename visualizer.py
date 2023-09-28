import streamlit as st
from story_retriever import StoryRetriever
from story_config import StoryConfig
from story import Story
from story_config import ImageGenStyle


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
    story.build_pages()
    st.title("Generated Story")
    for (i,page) in enumerate(story.pages):
        st.write(f"Page {i+1}")
        st.image(page.content.imageURL)
        st.write(page.content.text)
        "---"
    st.title("Source")
    st.write(most_relevant_content)



