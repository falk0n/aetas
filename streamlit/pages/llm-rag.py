import streamlit as st

from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from modules import config

#
# llm-rag.py
# RAG with LLM. Based on the answer documents are fetched from the retriever.
# Then, everything is stuffed into a prompt and the LLM is doing its thing.
#
st.write("# Retrieval augmented LLM chat")
llm = st.session_state["llm"]
calc_token_length = llm.get_num_tokens


config.show_expander_config("embedding")
config.show_expander_config("vectorstore")
config.show_expander_config("retriever")
retriever = st.session_state["retriever"]

modify_prompt = st.checkbox("Modify prompt configuration")


# configure and create prompt
template = """
Du bist ein Experte für IT-Sicherheit. Deine Antworten sind kurz und präzise.
Wenn möglich benutzt du Aufzählungen.
Beantworte die Frage ausschließlich anhand des folgenden Kontext:
{context}

Question: {question}
"""

height = 300
if modify_prompt:
    st.write("### Prompt")
    height = st.number_input(label="Höhe des Textbereichs in Pixel", value=height, min_value=0, max_value=1000)
    template = st.text_area(label="Prompt template", value=template, height=height)
prompt = PromptTemplate.from_template(template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


st.write("### Query")
config_query = "Welche Anforderungen sind für Linux zu beachten?"
my_query = st.text_input(label="Query text", value=config_query)
st.write(f"Number of tokens in query: {calc_token_length(my_query)}")

if st.button("Show me your answer!"):
    answer = chain.invoke(my_query)
    st.write(f"Number of tokens in answer: { calc_token_length(answer)}")
    st.write(answer)
