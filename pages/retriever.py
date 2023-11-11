import streamlit as st
import numpy as np

from modules import config

#
# retriever.py
# Let's enter test questions and retrieve matching documents from the store.
# This copies some functionality from config-chroma-retriever because
# tuning retriever parameters based on query results requires a fast feedback loop.
#

embedding_function = st.session_state["embedding"]
vectordb = st.session_state["vectorstore"]


st.write("# Retrieval from vectorstore")
if st.checkbox("Show vectorstore and embedding"):
    config.show_config("embedding", False)
    config.show_config("vectorstore", False)


# Let's GET REAL
st.write("## Retrieval query")
retriever_kwargs = st.session_state["retriever_kwargs"]
config_search_type = retriever_kwargs["search_type"]
config_retriever = retriever_kwargs["kwargs"]

# option to change search type
config_search_types = ["similarity_score_threshold", "similarity"]
index = config_search_types.index(config_search_type)
search_type = st.selectbox(label="Search type", options=config_search_types, index=index)

# option to change k
config_retriever["k"] = st.number_input(label="Anzahl Ergebnisse:", value=config_retriever["k"])

# option to change score_threshold
config_retriever["score_threshold"] = st.number_input(
    label="Minimal similarity for match",
    value=config_retriever["score_threshold"], min_value=0.0, max_value=1.0)
retriever = vectordb.as_retriever(search_type=config_search_type, search_kwargs=config_retriever)

# option to set a new global retriever config
if st.button("Set new retriever configuration"):
    retriever = vectordb.as_retriever(search_type=config_search_type, search_kwargs=config_retriever)
    retriever_kwargs = {"search_type": search_type, "kwargs": config_retriever}
    st.session_state["retriever"] = retriever
    st.session_state["retriever_name"] = "Vectorstore retriever"
    st.session_state["retriever_kwargs"] = retriever_kwargs


st.write("## Retrieval phrase")
question_default = "Welche Anforderungen gibt es für Linux?"
question = st.text_input(label="Retrieval phrase", label_visibility="collapsed", value=question_default)


st.write("## Results")
retrieved_docs = retriever.invoke(question)
if st.checkbox("Show statistics and raw data"):
    st.write("#### Statistics and raw data")
    data = vectordb.get(include=["metadatas"])
    st.write(f'total number of entries in vectorstore: {len(data["ids"])}')
    st.write(retrieved_docs)
st.write("### Query results")
for doc in retrieved_docs:
    metadata = doc.metadata
    st.write(f"#### Baustein: {metadata.get('baustein_name', 'nicht gesetzt')}")
    st.write(f"**Chapter:** {metadata.get('chapter_name', 'nicht gesetzt')}")
    st.write(f"**Section:** {metadata.get('section_name', 'nicht gesetzt')}")
    st.write(f"**Content:** {doc.page_content}")
    st.write("\n")
