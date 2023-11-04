import time
import streamlit as st

#
# store-document.py
# Embed and store one document in the vectorstore.
# This script uses the configurations made by other modules.
# namely loader, preprocessing, embedding and vectorstore.
#

st.write("# Embed and store one document")
st.write("## Document configuration")
config_filedir = "/home/falk/work/nlp/corpus/bsi_pdf/"                  # default directory
config_filename = "SYS.1.3 Server unter Linux und Unix.pdf.clean.pdf"   # default filename
my_filedir = st.text_input(label="Verzeichnis:", value=config_filedir)  # directory after user input
my_filename = st.text_input(label="Dokument:", value=config_filename)   # filename after user input
infile = my_filedir + my_filename

if st.checkbox("Show processing configuration"):
    st.write(f'Loader: {st.session_state["loader_name"]}')
    st.write(f'Preprocessor: {st.session_state["preprocess_name"]}')
    st.write(f'Embedding: {st.session_state["embedding_name"]}')
    st.write(f'Collection: {st.session_state["vectorstore_name"]}')

if st.button("Process document"):
    st.write("## Process document")
    loader = st.session_state["loader"]
    fileloader = loader(infile)
    docs_raw = fileloader.load()
    if st.checkbox("Show raw documents"):
        st.write(docs_raw)

    preprocessor = st.session_state["preprocess"]
    docs_preprocessed = preprocessor(docs_raw)
    if st.checkbox("Show preprocessed documents"):
        st.write(docs_preprocessed)

    vectordb = st.session_state["vectorstore"]
    time_start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    vectordb.add_documents(docs_preprocessed)
    time_end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"Processing time (store and embed): { duration_ms} [ms]")
