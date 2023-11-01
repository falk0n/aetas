import streamlit as st

import chromadb

from langchain.vectorstores import Chroma
import langchain.embeddings as lce


#
# retrieve02.py
# Let's enter test questions and retrieve matching documents from the store.
# The action starts at let's GET REAL!
#

st.write("# Retrieval from vectorstore")
st.write("## Configuration")

# select and configure embedding model
config_default_hf_embeddings = ["multilingual-e5-large", "all-mpnet-base-v2", "all-MiniLM-L6-v2"]
config_embedding_names = {
    "multilingual-e5-large": "intfloat/multilingual-e5-large",          # MTEB retrieval rank 6
    "instructor-xl": "hkunlp/instructor-xl",                            # MTEB retrieval rank 14
    "instructor-large": "hkunlp/instructor-large",                      # MTEB retrieval rank 23
    "instructor-base": "hkunlp/instructor-base",                        # MTEB retrieval rank 29
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",     # MTEB retrieval rank 37
    "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2"        # MTEB retrieval rank 42
}
my_embedding = st.radio(label="HuggingFace embedding model", options=config_embedding_names, index=0, horizontal=True)
my_compute_method = st.radio(label="Computing method", options=["cpu", "cuda"], index=0, horizontal=True)
if my_embedding in config_default_hf_embeddings:
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )
else:   # initialize InstructEmbedding
    embedding_function = lce.HuggingFaceInstructEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )

# location of chroma vectorstore
config_chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
my_chroma_dir = st.text_input(label="location of chroma vectorstore", value=config_chroma_dir)

# name of chroma collection where we store the documents
chroma_client = chromadb.PersistentClient(my_chroma_dir)
chroma_collections = [foo.name for foo in chroma_client.list_collections()]
my_collection = st.radio(label="Chroma collection name: ", options=chroma_collections, horizontal=True)


vectordb = Chroma(
    client=chroma_client,
    collection_name=my_collection,
    embedding_function=embedding_function,
    persist_directory=my_chroma_dir)


# Let's GET REAL
st.write("## Query")
question_default = "Welche Anforderungen gibt es für Linux?"
question = st.text_input(label="Frage:", value=question_default)

filter_metadata = dict()

config_anzahl = 5
my_anzahl = st.number_input(label="Wie viele Ergebnisse sollen zurückgegeben werden?", value=config_anzahl)


st.write("## Results")
st.write("### Statistics")
data = vectordb.get(include=["metadatas"])
st.write(f'total number of entries in vectorstore: {len(data["ids"])}')

st.write("### Query results")
retrieved_docs = vectordb.similarity_search_with_score(query=question, k=my_anzahl, filter=filter_metadata)
for doc in retrieved_docs:
    metadata = doc[0].metadata
    st.write(f"#### Baustein: *{ metadata.get('baustein_name', 'nicht gesetzt')}*")
    st.write(f"**Kapitel:** *{ metadata.get('chapter_name', 'nicht gesetzt')}*")
    st.write(f"**Abschnitt:** *{ metadata.get('section_name', 'nicht gesetzt')}*")
    st.write(f"**Anforderung:** *{ metadata.get('requirement', False) }*")
    st.write(f"**Inhalt:** *{doc[0].page_content}*")
    st.write(f'**Cosine similarity**: *{ "{:.5f}".format(doc[1]) }*')
    st.write("\n")