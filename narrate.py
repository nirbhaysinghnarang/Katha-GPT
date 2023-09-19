import streamlit as st
from query_db import getMostRelevantStory
st.title("Katha GPT")
input_col, output_col = st.columns(2)

response = ""
with input_col:
   
    st.text_input(
        "What story would you like to hear today?",
        key="query_input",
    )
    if st.button("Narrate"):
    	response = getMostRelevantStory(st.session_state.query_input)


with output_col:
	if response:
		st.write(response)

