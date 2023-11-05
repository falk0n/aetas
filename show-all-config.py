import streamlit as st
from modules import config

# First, run initial all global session objects.
if "init-already-done" not in st.session_state.keys():
    widget = st.text("Initial configuration ...")
    config.default_loader()
    config.default_preprocess()
    config.default_embedding()
    config.default_vectorstore()
    config.default_llm()
    st.session_state["init-already-done"] = True    # make sure we don't initialize twice and overwrite user configs
    widget.text("Initial configuration done.")


# Then, we can show all configurations.
st.write("# Show all global configurations")
show_me_details = st.checkbox("Show configuration details")

for name in ["loader", "preprocess", "embedding", "vectorstore", "llm"]:
    config.show_config(name, show_me_details)
