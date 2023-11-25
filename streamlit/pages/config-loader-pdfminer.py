import streamlit as st
from langchain.document_loaders import PDFMinerLoader


#
# config-loader-pdfminer.py
# Configure the global loader object in session state.
# In this case we simply use PDFMinerLoader.
#

st.write("# Configure PDFMinerLoader")
st.write("#### Current document loader")
widget = st.text(f'Loader name: {st.session_state["loader_name"]}')

st.write("#### New document loader")
st.write("""
There is really nothing to configure here. We simply use PDFMinerLoader from Langchain.
PDFMinerLoader has no specific configuration options.
All interesting stuff takes place in the preprocessing and in the embedding.
""")

if st.button("Set PDFMinerLoader as new loader for documents"):
    st.session_state["loader"] = PDFMinerLoader
    st.session_state["loader_name"] = "PDFMinerLoader"
    st.session_state["loader_kwargs"] = dict()
    widget.text(f'Loader name: {st.session_state["loader_name"]}')
