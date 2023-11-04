import streamlit as st

from langchain.llms import OpenAI
import tiktoken

from modules import fscutils as fsc, config

#
# llm-qa.py
# Simple interface for chatting with a llm using streamlit and langchain.
# Mostly useful for as a "Hello world"-type of chatbot and also to understand some parameters like max_tokens.
#

# first, run initial configurations
config.config_default_embedding()
config.config_default_vectorstore()


st.title("Simple OpenAI interface")

st.header("Model configuration")
google_says = """
While GPT-3.5 Turbo performs well in 0-shot classification and math,
Davinci-003 performs slightly better in k-shot classification
and may be a better option for those looking for clear, concise responses that get straight to the point.
"""
st.write(google_says)
config_model_list = ["text-davinci-003", "gpt-3.5-turbo-instruct"]
my_model = st.radio(label="choose model to use", options=config_model_list, index=0, horizontal=True)

config_no_completions = 1
my_no_completions = st.number_input(label="number of completions", value=config_no_completions, min_value=1)

config_temperature = 0.5
my_temperature = st.number_input(label="Temperature:", value=config_temperature, min_value=0.0, max_value=1.0)

config_max_tokens = 256
my_max_tokens = st.number_input(label="max tokens in output", value=config_max_tokens, min_value=-1, max_value=1024)

# finally we can create and configure the llm
llm = OpenAI(model_name=my_model, temperature=my_temperature, max_tokens=my_max_tokens, n=my_no_completions)
encoder = tiktoken.encoding_for_model(my_model)


st.header("Q&A Session")
my_start_qa = fsc.true_false_radio("start Q&A session", default=False)

config_query = "Bitte nenne mir 5 Gründe, warum man eine AI Wendung in Python programmieren sollte."
my_query = st.text_input(label="Frage:", value=config_query)

encoding = encoder.encode(my_query)
st.write(f"Anzahl der Token: { len(encoding)}")
my_show_token = fsc.true_false_radio("show token list", default=False)
if my_show_token:
    st.write(encoding)

if my_start_qa:
    answer = llm.invoke(my_query)
    st.write(answer)
