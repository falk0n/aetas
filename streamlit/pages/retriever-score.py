import streamlit as st
import numpy as np

from modules import config

#
# retriever-score.py
# Let's enter test questions and retrieve matching documents from the store.
# In this version of the retriever I want to see the scores as well.
# With the Langchain retriever object there is no simple way to see the scores.
# So, instead, the vectorstore is queried directly and the score calculated explicitly.
#

embedding_function = st.session_state["embedding"]
vectordb = st.session_state["vectorstore"]


st.write("# Retrieval from vectorstore")
config.show_expander_config("embedding")
config.show_expander_config("vectorstore")


# Let's GET REAL
st.write("## Retrieval query")
config_search_type = "similarity_score_threshold"
config_retriever = {"k": 5, "score_threshold": 0.5}
# if st.checkbox("Modify retrieval configuration"):
st.write(f'Search type: {config_search_type}')
config_retriever["k"] = st.number_input(label="Anzahl Ergebnisse:", value=config_retriever["k"])
config_retriever["score_threshold"] = st.number_input(
    label="Minimal similarity for match",
    value=config_retriever["score_threshold"], min_value=0.0, max_value=1.0)
retriever = vectordb.as_retriever(search_type=config_search_type, search_kwargs=config_retriever)

question_default = st.session_state["query"]
question = st.text_input(label="Retrieval Phrase", value=question_default)
question_embedding = embedding_function.embed_query(question)

st.write("## Results")
retrieved_docs = retriever.invoke(question)

chroma_client = st.session_state["vectorstore_kwargs"]["chroma_client"]
chroma_collection = chroma_client.get_collection(st.session_state["vectorstore_name"])
results = chroma_collection.query(query_embeddings=[question_embedding])


if st.checkbox("Show raw data"):
    st.write("### Retrieval results raw data")
    data = vectordb.get(include=["metadatas"])
    st.write(retrieved_docs)
st.write("### Query results")
for doc in retrieved_docs:
    # doc_embedding = np.array(embedding_function.embed_documents([doc.page_content])[0])
    doc_embedding = np.array(embedding_function.embed_query(doc.page_content))
    score = np.dot(question_embedding, doc_embedding)
    st.write(f"#### Baustein: {doc.metadata.get('baustein_name', 'nicht gesetzt')}")
    st.write(f"**Chapter:** {doc.metadata.get('chapter_name', 'nicht gesetzt')}")
    st.write(f"**Section:** {doc.metadata.get('section_name', 'nicht gesetzt')}")
    st.write(f"**Similarity Score:** {score}")
    st.write(f"**Content:** {doc.page_content}")
    st.write("\n")
