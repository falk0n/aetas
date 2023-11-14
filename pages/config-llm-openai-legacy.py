import streamlit as st
from langchain.llms import OpenAI

#
# llm-qa.py
# Configure the global LLM object in session state.
# In this case we configure an OpenAI instruct model with a legacy endpoint.
# Please note that the newer interface from OpenAI is the chat endpoint.
#
st.write("# Configure OpenAI LLM")
st.write("#### Current LLM")
widget = st.text(f'LLM name: {st.session_state["llm_name"]}')


st.write("#### New LLM")
google_says = """
While GPT-3.5 Turbo performs well in 0-shot classification and math,
Davinci-003 performs slightly better in k-shot classification
and may be a better option for those looking for clear, concise responses that get straight to the point.
"""
st.write(google_says)
config_model_list = ["text-davinci-003", "gpt-3.5-turbo-instruct"]
my_model = st.radio(label="choose model to use", options=config_model_list, index=0, horizontal=True)

kwargs = dict()
kwargs["temperature"] = st.number_input(label="Temperature:", value=0.3, min_value=0.0, max_value=1.0)
kwargs["max_tokens"] = st.number_input(label="max tokens in output", value=512, min_value=-1, max_value=4096)

# initialize the llm
llm = OpenAI(model_name=my_model,
             temperature=kwargs["temperature"],
             max_tokens=kwargs["max_tokens"])


# finally, update the global state after pressing the confirm button
if st.button("Confirm new LLM"):
    st.session_state["llm"] = llm
    st.session_state["llm_name"] = my_model
    st.session_state["llm_kwargs"] = kwargs
    # update the model information at the top of the page
    widget.text(f'LLM name: {st.session_state["llm_name"]}')
