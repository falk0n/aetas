import streamlit as st
from modules import config

#
# config-default-query.py
# Configure the global loader object in session state.
# In this case it is TextLoader.
#

st.write("# Configure default query")
st.write("#### Current default query")

widget = st.text(f'Loader name: {st.session_state["query_name"]}')

st.write("#### New default query")
st.write("""
The default query is used in the following modules: chroma-collection-analysis, retriever,
retriever-score, llm-rag. It's just a string with the default query.
""")

new_default_query_text = st.text_input(label="default query", value=st.session_state["query"])
new_default_query_name = st.text_input(label="default query name", value=st.session_state["query_name"])

if st.button("Set default query"):
    st.session_state["query"] = new_default_query_text
    st.session_state["query_name"] = new_default_query_name
    st.session_state["query_kwargs"] = dict()
    widget.text(f'Loader name: {st.session_state["query_name"]}')


# rest default query to lorem ipsum
if st.button("Reset default query"):
    config.default_query()
    widget.text(f'Loader name: {st.session_state["query_name"]}')
