import time
import streamlit as st

#
# store-document.py
# Embed and store one document in the vectorstore.
# This script uses the configurations made by other modules.
# namely loader, preprocessing, vectorstore.
#

st.write("# Embed and store one document")
st.write("### Document configuration")
config = st.session_state["defaults"]["store-document"]
config_filedir = config["directory"]    # default directory
config_filename = config["filename"]    # default filename
my_filedir = st.text_input(label="Verzeichnis:", value=config_filedir)  # directory after user input
my_filename = st.text_input(label="Dokument:", value=config_filename)   # filename after user input
infile = my_filedir + my_filename

if st.checkbox("Show processing configuration"):
    st.write(f'Loader: {st.session_state["loader_name"]}')
    st.write(f'Preprocessor: {st.session_state["preprocess_name"]}')
    st.write(f'Embedding: {st.session_state["embedding_name"]}')
    st.write(f'Collection: {st.session_state["vectorstore_name"]}')

show_docs_raw = st.checkbox("Show raw documents")
show_docs_preprocessed = st.checkbox("Show preprocessed documents")

if st.button("Process document"):
    st.write("## Process document")
    loader = st.session_state["loader"]
    fileloader = loader(infile)
    docs_raw = fileloader.load()
    if show_docs_raw:
        st.write(docs_raw)

    preprocessor = st.session_state["preprocess"]
    docs_preprocessed = preprocessor(docs_raw)
    if show_docs_preprocessed:
        st.write(docs_preprocessed)

    vectordb = st.session_state["vectorstore"]
    time_start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    vectordb.add_documents(docs_preprocessed)
    time_end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"Processing time (store and embed): { duration_ms} [ms]")
