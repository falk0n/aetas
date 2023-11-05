import streamlit as st

from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

#
# llm-rag.py
# RAG with LLM. Based on the answer documents are fetched from the retriever.
# Then, everything is stuffed into a prompt and the LLM is doing its thing.
#
st.write("# Retrieval augmented LLM chat")
llm = st.session_state["llm"]
calc_token_length = llm.get_num_tokens

modify_retriever = st.checkbox(label="Modify retriever configuration")
modify_prompt = st.checkbox("Modify prompt configuration")

config_search_types = ["similarity_score_threshold", "similarity"]
config_k = 5
config_score_threshold = 0.3

# configure and create retriever
search_type = config_search_types[0]
if modify_retriever:
    st.write("### Retriever")
    search_type = st.selectbox(label="Search type", options=config_search_types)
    config_k = st.number_input(
        label="Max number of return values", min_value=1, max_value=20,
        value=config_k)
    config_score_threshold = st.number_input(
        label="Score threshold", min_value=0.0, max_value=1.0,
        value=config_score_threshold)

st.write(f"search type: {search_type}")
config_retriever = {"k": config_k, "score_threshold": config_score_threshold}
embedding_function = st.session_state["embedding"]
vectordb = st.session_state["vectorstore"]
retriever = vectordb.as_retriever(search_type=search_type, search_kwargs=config_retriever)


# configure and create prompt
template = """
Du bist ein Experte für IT-Sicherheit. Deine Antworten sind kurz und präzise.
Wenn möglich benutzt du Aufzählungen.
Beantworte die Frage ausschließlich anhand des folgenden Kontext:
{context}

Question: {question}
"""

height = 200
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
