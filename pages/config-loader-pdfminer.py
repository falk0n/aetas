import streamlit as st
from langchain.document_loaders import PDFMinerLoader

from modules import config

#
# config-pdf-pdfminer.py
# Configure the global loader object in session state.
# In this case we simply use PDFMinerLoader.
#
st.title("Load one document")

st.write("""
There is really nothing to configure here. We simply use PDFMinerLoader from Langchain.
All interesting configuration takes place in the preprocessing steps and in the embedding.
This file exists mostly for demonstration purposes because the loader is already set by default.
In case you want some other loader create a new load-XXX module.
""")

st.session_state["loader"] = PDFMinerLoader
st.session_state["loader_name"] = "PDFMinerLoader"
st.session_state["loader_kwargs"] = dict()

config.show_config("loader", True)
