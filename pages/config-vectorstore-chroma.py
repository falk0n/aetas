import streamlit as st
import chromadb
from langchain.vectorstores import Chroma

from modules import config

#
# config-vectorstore.py
# Configure the global vectorstore object in session state.
# This is a configuration with a persistent chroma client.
#
st.write("# Configure Vectorstore")
config.show_config("vectorstore", True)
kwargs = st.session_state["vectorstore_kwargs"]


st.write("### Specify new vectorstore")
config_chroma_dir = kwargs["persist_dir"]
my_chroma_dir = st.text_input(label="Location of chroma vectorstore", value=config_chroma_dir)

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
