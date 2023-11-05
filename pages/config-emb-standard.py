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

st.write("# Configure Standard Embedding")
st.write("#### Current embedding model")
widget = st.text(f'Embedding model name: {st.session_state["embedding_name"]}')


# select embedding model and computing preference
st.write("#### New embedding model")
embedding_names = {
    "multilingual-e5-large": "intfloat/multilingual-e5-large",          # MTEB retrieval rank 6
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",     # MTEB retrieval rank 37
    "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2"}       # MTEB retrieval rank 42
my_embedding = st.radio(label="Embedding model", options=embedding_names, index=0, horizontal=True)
my_compute_method = st.radio(label="Compute method", options=["cpu", "cuda"], index=0, horizontal=True)

# initialize the embedding model
# This might download the model from Huggingface if not already locally cached.
embedding_model = lce.HuggingFaceEmbeddings(
    model_name=embedding_names[my_embedding],
    model_kwargs={"device": my_compute_method},
    encode_kwargs={"normalize_embeddings": True})

# finally, update the global state after pressing the confirm button
if st.button("Confirm new embedding model"):
    st.session_state["embedding"] = embedding_model
    st.session_state["embedding_name"] = embedding_names[my_embedding]
    st.session_state["embedding_kwargs"] = {"embedding_device": my_compute_method}
    # update the model information at the top of the page
    widget.text(f'Embedding model name: {st.session_state["embedding_name"]}')
