import time
import os

import streamlit as st
from langchain.document_loaders import PDFMinerLoader

from modules import fscutils as fsc, bsi

#
# store-directory.py
# Embed and store all files from a directory in the vectorstore.
# This script uses the configurations made by other modules.
# namely loader, preprocessing, vectorstore.
#
st.write("# Embed and store all files from directory")
st.write("### Directory configuration")
config_filedir = "/home/falk/work/nlp/corpus/bsi_sample/"
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
    time_start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    for name in os.listdir(my_filedir):
        widget.text(f"Processing: {name}")
        filename = my_filedir + name
        fileloader = loader(filename)
        docs_raw = fileloader.load()
        docs_preprocessed = preprocessor(docs_raw)
        vectordb.add_documents(docs_preprocessed)
    time_end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    widget = st.text("Processing: done")
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"total processing time (mostly embedding): {duration_ms} [ms]")
