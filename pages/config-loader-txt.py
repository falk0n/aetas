import streamlit as st
from langchain.document_loaders import TextLoader

#
# config-loader-txt.py
# Configure the global loader object in session state.
# In this case it is TextLoader.
#

st.write("# Configure TextLoader")
st.write("#### Current document loader")
widget = st.text(f'Loader name: {st.session_state["loader_name"]}')

st.write("#### New document loader")
st.write("""
There is really nothing to configure here. As a TextLoader we use from Langchain.
It has no configuration options and puts the whole text file into a Document. 
All interesting stuff takes place in the preprocessing and in the embedding.
""")

if st.button("Set TextLoader as new loader for documents"):
    st.session_state["loader"] = TextLoader
    st.session_state["loader_name"] = "TextLoader"
    st.session_state["loader_kwargs"] = dict()
    widget.text(f'Loader name: {st.session_state["loader_name"]}')
