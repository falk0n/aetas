import streamlit as st
import pandas as pd
import numpy as np
import math as m

#
# chroma-collection-analysis.py
# This script does some simple statistics and analysis of a collection.
# Subject of the analysis is always the collection configured with the vectorstore.
#
st.write("# Collection analysis")

# initialize chroma_client, collection and retrieve all the data
vectordb_kwargs = st.session_state["vectorstore_kwargs"]
chroma_dir = vectordb_kwargs["persist_dir"]
chroma_client = vectordb_kwargs["chroma_client"]

collection_name = st.session_state["vectorstore_name"]
collection = chroma_client.get_collection(collection_name)

include_attributes = ["embeddings", "metadatas", "documents"]
all_data = collection.get(include=include_attributes)

# calculate basic properties of the vectorstore
vector_length = len(all_data["embeddings"][0])
entries = len(all_data["ids"])

# calculate statistics about the embeddings in the vectorstore
min_distance = 1
max_distance = -1
config_bins = 50

vectors = np.asarray(all_data["embeddings"])
dot_products = np.matmul(vectors, vectors.T)
values = []
for x in range(entries):
    for y in range(entries):
        if x < y:
            score = dot_products[x, y]
            min_distance = min(min_distance, score)
            max_distance = max(max_distance, score)
            values.append(score)

# select distance measure to display
st.write("""
The first diagram shows the global distribution of similarities in the vectorstore.
Please note the there is no triangle inequality for cos similarity.
Only euclidean distance allows you to use your geometric intuition.
:sweat_smile:
""")


st.write("## Entries in collection")
st.write(f'Collection name: {collection_name}')
st.write(f'Number of entries: {len(all_data["ids"])}')
st.write(f'Embedding length: {vector_length}')

st.write("## Distances distribution of test query")
embedding_function = st.session_state["embedding"]
question_default = st.session_state["query"]
question = st.text_input(label="Retrieval Phrase", value=question_default)
question_embedding = np.array(embedding_function.embed_query(question))
query_distances = np.matmul(vectors, question_embedding.T)
min_query_distance = min(query_distances)
max_query_distance = max(query_distances)

st.write(f"Minimal distance from query: {min_query_distance}")
st.write(f"Maximal distance from query: {max_query_distance}")

query_df = pd.DataFrame({"scores": query_distances})
query_histogram = query_df["scores"].hist(bins=config_bins)
st.pyplot(fig=query_histogram.figure)

st.write("## Global distribution of similarities")
st.write(f"Minimal distance between two vectors: {min_distance}")
st.write(f"Maximal distance between two vectors: {max_distance}")

global_df = pd.DataFrame({"scores": values})
global_histogram = global_df["scores"].hist(bins=config_bins)
st.pyplot(fig=global_histogram.figure)
