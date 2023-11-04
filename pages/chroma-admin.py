import streamlit as st
import chromadb

from modules import fscutils as fsc


#
# chroma-admin.py
# Open a local chroma vectorstore and do some simple maintenance.
# The action starts at let's GET REAL!
#

st.write("# Simple Chroma Admin")

# location of chroma vectorstore
chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
if st.checkbox("select chromadb location"):
    chroma_dir = st.text_input(label="location of chroma vectorstore", value=chroma_dir)

# Let's GET REAL
chroma_client = chromadb.PersistentClient(chroma_dir)
chroma_collections_raw = chroma_client.list_collections()

chroma_collections = dict()
for collection in chroma_collections_raw:
    chroma_collections[collection.name] = collection

available_collections = sorted(chroma_collections.keys())
my_collection = st.selectbox(label="choose collection", options=available_collections)
collection = chroma_collections[my_collection]

st.write("### Collection info")
model_dump = collection.model_dump()
for key in model_dump.keys():
    st.write(f"{key}: {model_dump[key]}")

entries_in_collection = collection.count()
st.write(f'Anzahl Embeddings: {entries_in_collection}')

if entries_in_collection > 0:
    peek_value = collection.peek(limit=1)
    st.write(f'dimensions: {len(peek_value["embeddings"][0])}')
    st.write(f'metadata keys: {list(peek_value["metadatas"][0].keys())}')

st.write("### Delete Collection")
config_delete_collection = False
config_really_delete = False

my_delete_collection = fsc.true_false_radio("delete collection", default=config_delete_collection)
if my_delete_collection:
    my_really_delete = fsc.true_false_radio(
        f"REALLY delete collection {my_collection} NOW", default=config_really_delete)
    if my_really_delete:
        chroma_client.delete_collection(my_collection)
        my_delete_collection = False
        my_really_delete = False
        my_collection = "please select an existing collection"

# if st.checkbox("I want to delete the selection"):
#    if st.checkbox(f"I want to REALLY delete collection {my_collection}"):
#        chroma_client.delete_collection(my_collection)
#        my_collection = "not available"
