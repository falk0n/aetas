import tomllib
import streamlit as st
from modules import config


# read default configurations
config_file = "aetas.toml"
with open(config_file, "rb") as file:
    configuration = tomllib.load(file)
    st.session_state["defaults"] = configuration


# First, run initial all global session objects.
if "init-already-done" not in st.session_state.keys():
    widget = st.text("Initial configuration ...")
    config.default_loader()
    config.default_preprocess()
    config.default_embedding()
    config.default_vectorstore()
    config.default_retriever()
    config.default_llm()
    st.session_state["init-already-done"] = True    # make sure we don't initialize twice and overwrite user configs
    widget.text("Initial configuration done.")


st.write("## New Configuration")
st.write(configuration)


st.write("## Old Configuration")
for name in ["loader", "preprocess", "embedding", "vectorstore", "retriever", "llm"]:
    config.show_expander_config(name)
