import streamlit as st
import chromadb

import langchain.embeddings as lce
from langchain.vectorstores import Chroma


#
# Session variables:
# embedding_function: langchain.schema.embeddings.Embeddings
# embedding_name: str (model_name for embedding_function)
# embedding_device: str (cpu, cuda, etc.)
#
def config_default_embedding():
    default_embedding = "intfloat/multilingual-e5-large"
    default_device = "cpu"
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=default_embedding,
        model_kwargs={"device": default_device},
        encode_kwargs={"normalize_embeddings": True})
    st.session_state["embedding_function"] = embedding_function
    st.session_state["embedding_name"] = default_embedding
    st.session_state["embedding_device"] = default_device
    return embedding_function


#
# Create the default vectorstore and make it available in the session state
# Session variables:
# vectorstore: langchain.....Vectorstore
# vectorstore_dir: str
# vectorstore_collection: str
# vectorstore_client: chroma client (result from chroma.PersistentClient)
#
def config_default_vectorstore():
    config_chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
    config_collection = "default_collection"
    chroma_client = chromadb.PersistentClient(config_chroma_dir)
    vectordb = Chroma(
        client=chroma_client,
        collection_name=config_collection,
        embedding_function=st.session_state["embedding_function"],
        persist_directory=config_chroma_dir)
    st.session_state["vectorstore"] = vectordb
    st.session_state["vectorstore_dir"] = config_chroma_dir
    st.session_state["vectorstore_collection"] = config_collection
    st.session_state["vectorstore_client"] = chroma_client
