import streamlit as st
from langchain.text_splitter import CharacterTextSplitter


#
# preprocess-bsi.py
# Configure the preprocess object in session state.
# In this case it is a CharacterTextSplitter.
# You can configure, chunk_size and chunk_overlap.
#
def character_text_splitter_preprocessor(docs):
    # read the configuration for the CharacterTextSplitter from session state
    config_kwargs = st.session_state["preprocess_kwargs"]
    chunk_size = config_kwargs["chunk_size"]
    chunk_overlap = config_kwargs["chunk_overlap"]
    # configure the splitter, do the work and return results
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    docs_raw = text_splitter.split_documents(docs)
    return docs_raw


st.write("# Configure CharacterTextSplitter preprocessing")
st.write("#### Current preprocessing")
widget = st.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')

st.write("#### New preprocessing")
new_kwargs = dict()
old_kwargs = st.session_state["preprocess_kwargs"]
new_kwargs["chunk_size"] = old_kwargs.get("chunk_size", 1)
new_kwargs["chunk_overlap"] = old_kwargs.get("chunk_overlap", 0)
new_kwargs["keep_separator"] = old_kwargs.get("chunk_overlap", False)

new_kwargs["chunk_size"] = st.number_input(label="Chunk size", value=new_kwargs["chunk_size"], min_value=1)
new_kwargs["chunk_overlap"] = st.number_input(label="Chunk size", value=new_kwargs["chunk_overlap"], min_value=0)


if st.button("Set new preprocessing configuration"):
    st.session_state["preprocess"] = character_text_splitter_preprocessor
    st.session_state["preprocess_name"] = "CharacterTextSplitter"
    st.session_state["preprocess_kwargs"] = new_kwargs
    # update the preprocessing information at the top of the page
    widget.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')
