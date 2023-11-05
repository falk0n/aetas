import streamlit as st

from modules import config

#
# llm-qa.py
# Simple interface for chatting with the llm from the global session state.
#
st.write("# Simple LLM chat")
llm = st.session_state["llm"]
calc_token_length = llm.get_num_tokens

if st.checkbox("Show LLM configuration"):
    config.show_config("llm", True)

st.write("### Query")
config_query = "Bitte nenne mir 5 Gründe, warum man eine AI Anwendung in Python programmieren sollte."
my_query = st.text_input(label="Query text", value=config_query)
st.write(f"Number of tokens in query: {calc_token_length(my_query)}")

if st.button("Show me your answer!"):
    answer = llm.invoke(my_query)
    st.write(f"Number of tokens in answer: { calc_token_length(answer)}")
    st.write(answer)
