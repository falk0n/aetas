import streamlit as st
import langchain.embeddings as lce

#
# config-embedding.py
# This module allows the user to select the embedding model to use.
# As per the application architecture the following session variables are set:
# embedding_function: langchain.schema.embeddings.Embeddings
# embedding_name: str
# embedding_device: str
#

st.write("# Configure Embedding")
st.write("#### Current embedding")
widget_name = st.text(f'model_name: {st.session_state["embedding_name"]}')
widget_device = st.text(f'device: {st.session_state["embedding_device"]}')


st.write("#### Specify new embedding")
config_embedding_types = ["Standard Embedding", "Instruct Embedding"]
my_embedding_type = st.radio(label="Embedding type", options=config_embedding_types, index=0, horizontal=True)


# Standard and Instructor embeddings have different models that require different initializations
# FIXME: The code duplication doesn't look nice. What might be a better way?
if my_embedding_type == config_embedding_types[0]:
    config_embedding_names = {
        "multilingual-e5-large": "intfloat/multilingual-e5-large",          # MTEB retrieval rank 6
        "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",     # MTEB retrieval rank 37
        "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2"}       # MTEB retrieval rank 42
    my_embedding = st.radio(label="Embedding model", options=config_embedding_names, index=0, horizontal=True)
    my_compute_method = st.radio(label="Compute method", options=["cpu", "cuda"], index=0, horizontal=True)
    embedding_name = config_embedding_names[my_embedding]
    embedding_device = my_compute_method
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True})
else:
    config_embedding_names = {
        "instructor-xl": "hkunlp/instructor-xl",                            # MTEB retrieval rank 14
        "instructor-large": "hkunlp/instructor-large",                      # MTEB retrieval rank 23
        "instructor-base": "hkunlp/instructor-base"}                        # MTEB retrieval rank 29
    my_embedding = st.radio(label="Embedding model", options=config_embedding_names, index=0, horizontal=True)
    my_compute_method = st.radio(label="Compute method", options=["cpu", "cuda"], index=0, horizontal=True)
    # query instructions make the instruct model unique
    config_query_instruction = "Represent the question for retrieving supporting documents:"
    my_query_instruction = st.text_input(label="Query instruction", value=config_query_instruction)
    embedding_name = config_embedding_names[my_embedding]
    embedding_device = my_compute_method
    embedding_function = lce.HuggingFaceInstructEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        query_instruction=my_query_instruction,     # defined only in case of instruct embedding
        encode_kwargs={"normalize_embeddings": True})


# finally, update the global state
if st.button("Set new embedding function"):
    st.session_state["embedding_function"] = embedding_function
    st.session_state["embedding_name"] = embedding_name
    st.session_state["embedding_device"] = embedding_device
    # update the model information at the top of the page
    widget_name.text(f'model_name: {st.session_state["embedding_name"]}')
    widget_device.text(f'device: {st.session_state["embedding_device"]}')
