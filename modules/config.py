import streamlit as st
import chromadb
import langchain.embeddings as lce

from langchain.vectorstores import Chroma
from langchain.document_loaders import PDFMinerLoader
from langchain.llms import OpenAI

#
# Session state contains five elements:
# loader, preprocess, embedding, vectorstore, llm
#
# For each element there are three variables in the session state:
# XXX, XXX_name, XXX_kwargs where XXX is one of the elements above.
# XXX is a function/object depending on the element. Expected types / signatures are specified below.
# XXX_name is a str providing a readable name for the element.
# XXX_kwargs is a dictionary containing configurations of the elements.
# Available keys depend on the specific instance of the element.
#
# Signatures/ Expected types:
# embedding: langchain.schema.embeddings.Embeddings
# vectorstore:
# loader: str -> [Document]
# preprocess: [Document] -> [Document]
#


# set session state to default embedding
def default_embedding():
    default_embedding_model = "intfloat/multilingual-e5-large"
    default_device = "cpu"
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=default_embedding_model,
        model_kwargs={"device": default_device},
        encode_kwargs={"normalize_embeddings": True})
    st.session_state["embedding"] = embedding_function
    st.session_state["embedding_name"] = default_embedding_model
    st.session_state["embedding_kwargs"] = {"embedding_device": default_device}
    return embedding_function


# set session state to default vectorstore
def default_vectorstore():
    config_chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
    config_collection = "default_collection"
    chroma_client = chromadb.PersistentClient(config_chroma_dir)
    vectordb = Chroma(
        client=chroma_client,
        collection_name=config_collection,
        embedding_function=st.session_state["embedding"],
        persist_directory=config_chroma_dir)
    st.session_state["vectorstore"] = vectordb
    st.session_state["vectorstore_name"] = config_collection
    kwargs = {"persist_dir": config_chroma_dir,
              "chroma_client": chroma_client}
    st.session_state["vectorstore_kwargs"] = kwargs


# set session state to default document loader
def default_loader():
    st.session_state["loader"] = PDFMinerLoader
    st.session_state["loader_name"] = "PDFMinerLoader"
    st.session_state["loader_kwargs"] = dict()


# This is the default preprocessing function. It does nothing.
def no_preprocessing(docs):
    return docs


# set session state to default preprocessing
def default_preprocess():
    st.session_state["preprocess"] = no_preprocessing
    st.session_state["preprocess_name"] = "none"
    st.session_state["preprocess_kwargs"] = dict()


# set session state to default llm
def default_llm():
    default_model = "text-davinci-003"
    kwargs = {"temperature": 0.1, "max_tokens": 256}
    llm = OpenAI(model_name=default_model,
                 temperature=kwargs["temperature"],
                 max_tokens=kwargs["max_tokens"])
    st.session_state["llm"] = llm
    st.session_state["llm_name"] = default_model
    st.session_state["llm_kwargs"] = kwargs


# show the details of a global configuration
# name is one of the elements described at the top of this file
def show_config(conf_name, show_details=False, prefix=""):
    print_name = conf_name.capitalize()
    if conf_name == "llm":
        print_name = "LLM"

    st.write(f"### {prefix + print_name}")
    st.write(f'{print_name} name: {st.session_state[conf_name + "_name"]}')

    if show_details:
        st.write(f'{print_name} object: {st.session_state[conf_name]}')
        details = st.session_state[conf_name + "_kwargs"]
        if len(details.keys()) > 0:
            for detail in sorted(list(details.keys())):
                st.write(f'{detail}: {details[detail]}')
        else:
            st.write("No details available")
