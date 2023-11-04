import streamlit as st

from langchain.text_splitter import CharacterTextSplitter, NLTKTextSplitter

from modules import bsi, fscutils as fsc


#
# preprocess-bsi.py
# Configure the preprocessing and set the preprocessor in the session state.#
def bsi_preprocessor(docs):
    # 1. split into paragraphs as a preparation for the bsi.parse function
    split_para = CharacterTextSplitter(separator="\n\n", chunk_size=1, chunk_overlap=0, keep_separator=False)
    docs_raw = split_para.split_documents(docs)

    # 2. Preprocess PDF (Baustein IT-Grundschutz)
    attributes = st.session_state["preprocess_kwargs"]
    docs_bsi = bsi.parse(docs_raw, attributes["aggregate_into_chapters"])
    return docs_bsi


st.write("## Configure BSI specific preprocessing")
split_into_sections = fsc.true_false_radio("Aggregate sections into chapters", default=True)

if st.button("Save preprocessing configuration"):
    st.session_state["preprocess"] = bsi_preprocessor
    st.session_state["preprocess_name"] = "BSI specific processing"
    st.session_state["preprocess_kwargs"] = {"aggregate_into_chapters": split_into_sections}
