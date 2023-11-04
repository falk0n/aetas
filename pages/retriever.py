import streamlit as st

#
# retriever.py
# Let's enter test questions and retrieve matching documents from the store.
# The action starts at let's GET REAL!
#

embedding_function = st.session_state["embedding_function"]
vectordb = st.session_state["vectorstore"]

st.write("# Retrieval from vectorstore")
if st.checkbox("Show vectorstore and embedding"):
    st.write("#### Embedding function")
    st.text(f'Name: {st.session_state["embedding_name"]}')
    st.text(f'Device: {st.session_state["embedding_device"]}')
    st.write("#### Vectorstore")
    st.text(f'persist_dir: {st.session_state["vectorstore_dir"]}')
    st.text(f'collection: {st.session_state["vectorstore_collection"]}')


# Let's GET REAL
st.write("### Retrieval query")
config_search_type = "similarity_score_threshold"
config_retriever = {"k": 5, "score_threshold": 0.5}
if st.checkbox("Modify retrieval configuration"):
    st.write(f'Search type: {config_search_type}')
    config_retriever["k"] = st.number_input(label="Anzahl Ergebnisse:", value=config_retriever["k"])
    config_retriever["score_threshold"] = st.number_input(
        label="Minimal similarity for match",
        value=config_retriever["score_threshold"], min_value=0.0, max_value=1.0)
retriever = vectordb.as_retriever(search_type=config_search_type, search_kwargs=config_retriever)

question_default = "Welche Anforderungen gibt es für Linux?"
question = st.text_input(label="Retrieval Phrase", value=question_default)


st.write("### Results")
retrieved_docs = retriever.invoke(question)
if st.checkbox("Show statistics and raw data"):
    st.write("#### Statistics and raw data")
    data = vectordb.get(include=["metadatas"])
    st.write(f'total number of entries in vectorstore: {len(data["ids"])}')
    st.write(retrieved_docs)
st.write("### Query results")
for doc in retrieved_docs:
    metadata = doc.metadata
    st.write(f"#### Baustein: *{ metadata.get('baustein_name', 'nicht gesetzt')}*")
    st.write(f"**Kapitel:** *{ metadata.get('chapter_name', 'nicht gesetzt')}*")
    st.write(f"**Abschnitt:** *{ metadata.get('section_name', 'nicht gesetzt')}*")
    st.write(f"**Anforderung:** *{ metadata.get('requirement', False) }*")
    st.write(f"**Inhalt:** *{doc.page_content}*")
    st.write("\n")
