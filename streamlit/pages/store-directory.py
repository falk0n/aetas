import time
import os

import streamlit as st

#
# store-directory.py
# Embed and store all files from a directory in the vectorstore.
# This script uses the configurations made by other modules.
# namely loader, preprocessing, vectorstore.
#
st.write("# Embed and store all files from directory")
st.write("### Directory configuration")
config = st.session_state["defaults"]["store-directory"]
config_filedir = config["directory"]
my_filedir = st.text_input(label="Directory to load:", value=config_filedir)

if st.checkbox("Show processing configuration"):
    st.write(f'Loader: {st.session_state["loader_name"]}')
    st.write(f'Preprocessor: {st.session_state["preprocess_name"]}')
    st.write(f'Embedding: {st.session_state["embedding_name"]}')
    st.write(f'Collection: {st.session_state["vectorstore_name"]}')


st.write("### Processing files")
vectordb = st.session_state["vectorstore"]
loader = st.session_state["loader"]
preprocessor = st.session_state["preprocess"]

if st.button("Process files in directory"):
    widget = st.text("Processing: starts now")
    time_start = time.perf_counter_ns()
    for name in os.listdir(my_filedir):
        widget.text(f"Processing: {name}")
        filename = os.path.join(my_filedir, name)
        fileloader = loader(filename)
        docs_raw = fileloader.load()
        docs_preprocessed = preprocessor(docs_raw)
        vectordb.add_documents(docs_preprocessed)
    time_end = time.perf_counter_ns()
    widget = st.text("Processing: done")
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"total processing time (mostly embedding): {duration_ms} [ms]")
