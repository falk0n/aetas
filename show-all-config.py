import streamlit as st

from modules import config


# first, run initial configurations (if not already done)
if "init-already-done" not in st.session_state.keys():
    widget = st.text("Initial configuration ...")
    config.default_loader()
    config.default_preprocess()
    config.default_embedding()
    config.default_vectorstore()
    config.default_llm()
    st.session_state["init-already-done"] = True    # make sure we don't initialize twice and overwrite user configs
    widget.text("Initial configuration done.")


# show the details of a global configuration
# name is one of loader, preprocess, embedding, vectorstore
def show_config(conf_name, show_details=False):
    print_name = conf_name.capitalize()
    st.write(f"### {print_name}")
    st.write(f'{print_name} name: {st.session_state[conf_name + "_name"]}')

    if show_details:
        st.write(f'{print_name} object: {st.session_state[conf_name]}')
        details = st.session_state[conf_name + "_kwargs"]
        if len(details.keys()) > 0:
            for detail in sorted(list(details.keys())):
                st.write(f'{detail}: {details[detail]}')
        else:
            st.write("No details available")


# now, we can show all configurations
st.write("# Show all global configurations")
show_me_details = st.checkbox("Show configuration details")

for name in ["loader", "preprocess", "embedding", "vectorstore", "llm"]:
    show_config(name, show_me_details)
