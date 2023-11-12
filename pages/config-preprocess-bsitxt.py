import streamlit as st
from langchain.text_splitter import CharacterTextSplitter

from modules import fscutils as fsc


#
# preprocess-bsitxt.py
# Configure the preprocess object in session state.
# In this case it is a customized preprocessing for IT-Grundschutz Bausteine.
# For further explanations see the longer description in the code.
#
def character_bsi_txt_preprocessor(docs):
    # configure the splitter, do the work and return results
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1, chunk_overlap=0)

    docs_raw = text_splitter.split_documents(docs)
    docs_dict = fsc. conv_document_list_to_dicts(docs_raw)

    for item in docs_dict:
        # Baustein name and id
        baustein_raw = item["metadata"]["source"].split("/")[-1]
        baustein_name = baustein_raw.replace(".txt", "")
        baustein = baustein_name.split(" ")[0]
        item["metadata"]["baustein_name"] = baustein_name
        item["metadata"]["baustein"] = baustein
        # metadata for chapter/section/subsection headings
        headings_line = item["page_content"].split("\n")[0]
        headings = headings_line.split("/")
        if len(headings) > 0:
            item["metadata"]["chapter_name"] = headings[0]
        if len(headings) > 1:
            item["metadata"]["section_name"] = headings[1]
        if len(headings) > 2:
            item["metadata"]["subsection_name"] = headings[2]
        item["metadata"]["reference"] = baustein + "/" + headings_line
    docs_annotated = fsc.conv_dict_list_to_documents(docs_dict)
    return docs_annotated


st.write("# Configure BSI txt preprocessing")
st.write("#### Current preprocessing")
widget = st.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')

st.write("#### New preprocessing")
st.write("""
Currently there are no configuration options for this processor.
It expects txt files produced from the xml2txt processing for the XML version
of the IT-Grundschutz Kompendium from BSI.

The txt files are in a convenient form: paragraphs are separated by \n\n.
Each paragraph consists of an one line heading with format chapter[/section[/subsection]]
and a potentially long content line.
This preprocessing splits the paragraphs and adds metadata to each document.
""")

if st.button("Set new preprocessing configuration"):
    st.session_state["preprocess"] = character_bsi_txt_preprocessor
    st.session_state["preprocess_name"] = "BSI txt preprocessing"
    st.session_state["preprocess_kwargs"] = dict()
    # update the preprocessing information at the top of the page
    widget.text(f'Preprocessing name: {st.session_state["preprocess_name"]}')
