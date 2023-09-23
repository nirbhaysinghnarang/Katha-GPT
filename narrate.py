import streamlit as st
from query_db import build_story

st.title("Katha GPT")
input_col, output_col = st.columns(2)
story = None
with input_col:
    st.text_input(
        "What story would you like to hear today?",
        key="query_input",
    )
    if st.button("Narrate"):
        query = st.session_state.query_input
        story = build_story(query)
       

with output_col:
    if story:
        st.header("Story")
        st.write(story)
   
