import streamlit as st
from langchain.chat_models import ChatOpenAI

#
# llm-qa.py
# Configure the global LLM object in session state.
# In this case we configure an OpenAI model with the new chat endpoint.
# Langchain provides the new LLM object for this
#
st.write("# Configure OpenAI LLM")
st.write("#### Current LLM")
widget = st.text(f'LLM name: {st.session_state["llm_name"]}')

st.write("#### New LLM")
google_says = """
This uses the new chat model endpoint.
"""
st.write(google_says)
config_model_list = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106", "gpt-4", "gpt-4-32k"]
my_model = st.radio(label="choose model to use", options=config_model_list, index=0, horizontal=True)

kwargs = dict()
kwargs["temperature"] = st.number_input(label="Temperature:", value=0.3, min_value=0.0, max_value=1.0)
kwargs["max_tokens"] = st.number_input(label="max tokens in output", value=512, min_value=-1, max_value=4096)

# initialize the llm
llm = ChatOpenAI(model_name=my_model,
                 temperature=kwargs["temperature"],
                 max_tokens=kwargs["max_tokens"])

# finally, update the global state after pressing the confirm button
if st.button("Confirm new LLM"):
    st.session_state["llm"] = llm
    st.session_state["llm_name"] = my_model
    st.session_state["llm_kwargs"] = kwargs
    # update the model information at the top of the page
    widget.text(f'LLM name: {st.session_state["llm_name"]}')
