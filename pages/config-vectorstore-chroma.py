import streamlit as st
import chromadb
from langchain.vectorstores import Chroma

#
# config-vectorstore.py
# Configure the global vectorstore object in session state.
# This is a configuration with a persistent chroma client.
#
st.write("# Configure Vectorstore")
st.write("### Current vectorstore")
kwargs = st.session_state["vectorstore_kwargs"]
widget_path = st.text(f'Persist path: {kwargs["persist_dir"]}')
widget_collection = st.text(f'Collection name: {st.session_state["vectorstore_name"]}')


st.write("### New vectorstore")
config_chroma_dir = kwargs["persist_dir"]
my_chroma_dir = st.text_input(label="Location of chroma vectorstore", value=config_chroma_dir)

# let the user select only collections that already exist
chroma_client = chromadb.PersistentClient(my_chroma_dir)
chroma_collections = [foo.name for foo in chroma_client.list_collections()]
my_collection = st.selectbox(label="Chroma collection name: ", options=chroma_collections)
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
    widget_path.text(f'Persist path: {kwargs["persist_dir"]}')
    widget_collection.text(f'Collection name: {st.session_state["vectorstore_name"]}')


st.write("#### Hinweise")
st.write("""
Es können nur bestehende Collections ausgewählt werden.
Falls eine neue Collection benötigt wird, muss diese zunächst angelegt werden (chroma-admin).  
""")
