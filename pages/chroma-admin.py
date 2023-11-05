import streamlit as st
import chromadb
import pandas as pd
import numpy as np

#
# chroma-admin.py
# Open a persistent chroma vectorstore and do some simple collection management.
#
st.write("# Simple collection management")

# location of chroma vectorstore
chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
if st.checkbox("select chromadb location"):
    chroma_dir = st.text_input(label="location of chroma vectorstore", value=chroma_dir)
chroma_client = chromadb.PersistentClient(chroma_dir)


st.write("### Collections overview")
chroma_collections_raw = chroma_client.list_collections()
collection_names = sorted([collection.name for collection in chroma_collections_raw])
collection_stats = np.zeros(shape=(len(collection_names), 2), dtype=int)
for row in range(len(collection_names)):
    collection = chroma_client.get_collection(collection_names[row])
    collection_stats[row, 0] = collection.count()
    if collection_stats[row, 0] > 0:
        peek_value = collection.peek(limit=1)
        collection_stats[row, 1] = len(peek_value["embeddings"][0])
    else:
        collection_stats[row, 1] = 0
collections_overview = pd.DataFrame(collection_stats, index=collection_names, columns=["Entries", "Vector length"])
st.table(data=collections_overview)


st.write("### Collection management")
available_collections = collection_names
my_collection = st.selectbox(label="Choose collection", options=available_collections)
collection = chroma_client.get_collection(my_collection)

available_actions = ["Create new", "Clean", "Delete"]
my_action = st.radio(label="Select action", options=available_actions, index=0, horizontal=True)
my_new_collection = "default collection"
if my_action == "Create new":
    my_new_collection = st.text_input(label="Name of new collection", value=my_new_collection)

if st.button("Perform action"):
    if my_action == "Create new":
        chroma_client.get_or_create_collection(my_new_collection)
    elif my_action == "Clean":
        chroma_client.delete_collection(my_collection)
        chroma_client.get_or_create_collection(my_collection)
    else:   # Delete as the default action ;)
        chroma_client.delete_collection(my_collection)
