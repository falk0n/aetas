import streamlit as st
from langchain.document_loaders import PDFMinerLoader

#
# load-pdf-pdfminer.py
# Configure the loading of PDF document and make the loader available in the session state.
# The loading function expects one argument, namely the full path of the document to be processed.
#
st.title("Load one document")

st.write("""
There is really nothing to configure here. We simply use PDFMinerLoader from Langchain.
ALl interesting configuration takes place in the preprocessing steps and in the embedding.
This file exists mostly for demonstration purposes because the loader is already set by default.
In case you want some other loader create a new load-XXX module.
""")

st.session_state["loader"] = PDFMinerLoader
st.session_state["loader_name"] = "PDFMinerLoader"
st.session_state["loader_kwargs"] = dict()
