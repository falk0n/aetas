import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

from modules import bsi, fscutils as fsc


#
# preprocess-bsi.py
# Configure the preprocess object in session state.
# In this case it is a specialized preprocessing for PDFs from BSI IT-Grundschutz.
# Assumptions:
#   - Paragraphs are separated by "\n\n"
#   - no occurrences of "\n\n" except as paragraph separator
#
def bsi_preprocessor(docs):
    # First, split by line feed (\x0c). Otherwise, the header lines are not going to be recognized.
    # Then split into paragraphs (\n\n) and lines. bsi.parse() expects lines that can be classified.
    split_pages = CharacterTextSplitter(separator="\x0c", chunk_size=1, chunk_overlap=0, keep_separator=False)
    split_para = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=1, chunk_overlap=0, keep_separator=False)
    docs_raw = split_para.split_documents(split_pages.split_documents(docs))

    # 2. Preprocess PDF (Baustein IT-Grundschutz)
    attributes = st.session_state["preprocess_kwargs"]
    docs_bsi = bsi.parse(docs_raw, attributes["aggregate_into_chapters"])
    return docs_bsi


st.write("# Configure BSI specific preprocessing")
st.write("#### Preprocessing")
widget = st.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')

aggregate_sections = fsc.true_false_radio("Aggregate sections into chapters", default=False)

if st.button("Save preprocessing configuration"):
    st.session_state["preprocess"] = bsi_preprocessor
    st.session_state["preprocess_name"] = "BSI specific processing"
    st.session_state["preprocess_kwargs"] = {"aggregate_into_chapters": aggregate_sections}
    # update the preprocessing information at the top of the page
    widget.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')
