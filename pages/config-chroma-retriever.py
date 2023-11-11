import streamlit as st

from modules import config

#
# config-vectorstore-retriever.py
# Configure the global retriever object in session state.
# This script configures a retriever from a vectorstore.
#


st.write("# Configure chroma retriever")
vectordb = st.session_state["vectorstore"]
if st.checkbox("Show vectorstore"):
    config.show_config("vectorstore", prefix="Used ")


st.write("### Current configuration")
retriever_name = st.session_state["retriever_name"]
retriever_kwargs = st.session_state["retriever_kwargs"]

config_search_type = retriever_kwargs["search_type"]
config_retriever = retriever_kwargs["kwargs"]
widget_search_type = st.text(f"Search type: {config_search_type}")
widget_ret_config = st.text(f"Retriever kwargs: {config_retriever}")


st.write("### New configuration")

st.write(f'Search type: {config_search_type}')
config_search_types = ["similarity_score_threshold", "similarity"]
index = config_search_types.index(config_search_type)
search_type = st.selectbox(label="Search type", options=config_search_types, index=index)

config_retriever["k"] = st.number_input(label="Anzahl Ergebnisse:", value=config_retriever["k"])

config_retriever["score_threshold"] = st.number_input(
    label="Minimal similarity for match",
    value=config_retriever["score_threshold"], min_value=0.0, max_value=1.0)


if st.button("Activate new retriever"):
    retriever = vectordb.as_retriever(search_type=search_type, search_kwargs=config_retriever)
    retriever_kwargs["search_type"] = search_type
    retriever_kwargs["kwargs"] = config_retriever
    st.session_state["retriever"] = retriever
    st.session_state["retriever_name"] = retriever_name
    st.session_state["retriever_kwargs"] = retriever_kwargs
    widget_search_type.text(f"Search type: {config_search_type}")
    widget_ret_config.text(f"Retriever kwargs: {config_retriever}")
