import streamlit as st
from langchain.vectorstores import Chroma
import chromadb

#
# config-vectorstore.py
# This module allows the user to select the vector store to use.
# As per the application architecture the following session variables are set:
# vectorstore: langchain.....Vectorstore
# vectorstore_dir: str
# vectorstore_collection: str
# vectorstore_client: chroma client (result from chroma.PersistentClient)
#

st.write("# Configure Vectorstore")
st.write("#### Current vectorstore")
kwargs = st.session_state["vectorstore_kwargs"]
widget_dir = st.text(f'persist_directory: {kwargs["persist_dir"]}')
widget_collection = st.text(f'collection: {st.session_state["vectorstore_name"]}')


st.write("#### Specify new vectorstore")
config_chroma_dir = kwargs["persist_dir"]
my_chroma_dir = st.text_input(label="location of chroma vectorstore", value=config_chroma_dir)

# let the user select only a collection that already exists
chroma_client = chromadb.PersistentClient(my_chroma_dir)
chroma_collections = [foo.name for foo in chroma_client.list_collections()]
my_collection = st.radio(label="Chroma collection name: ", options=chroma_collections, horizontal=True)
vectordb = Chroma(
    client=chroma_client,
    collection_name=my_collection,
    embedding_function=st.session_state["embedding"],
    persist_directory=my_chroma_dir)


# finally, update the global state
if st.button("Set new vectorstore"):
    st.session_state["vectorstore"] = vectordb
    st.session_state["vectorstore_name"] = my_collection
    kwargs["chroma_client"] = chroma_client
    kwargs["persist_dir"] = my_chroma_dir
    st.session_state["embedding_kwargs"] = kwargs
    # update the vectorstore information at the top of the page
    widget_dir.text(f'persist_directory: {kwargs["persist_dir"]}')
    widget_collection.text(f'collection: {st.session_state["vectorstore_name"]}')
