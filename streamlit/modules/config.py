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


# set session state the given embedding
# Currently a default embedding has to be HuggingFaceEmbeddings
# still need to figure out how to take care of the extra parameter in HuggingFaceInstructEmbeddings
def set_embedding(name, model_kwargs, encode_kwargs):
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs)
    return embedding_function


# set default embedding model based on the configuration file
def default_embedding():
    config = st.session_state["defaults"]["embedding"]
    if config["model_type"] != "HuggingFaceEmbeddings":
        raise ValueError
    # FIXME: We should really check for any missing attributes in the configuration.
    embedding_function = set_embedding(config["embedding_name"],
                                       config["model_kwargs"],
                                       config["encode_kwargs"])
    # set session state for use by the other modules
    st.session_state["embedding"] = embedding_function
    st.session_state["embedding_name"] = config["embedding_name"]
    st.session_state["embedding_kwargs"] = {"model_kwargs": config["model_kwargs"],
                                            "encode_kwargs": config["encode_kwargs"]}
    return embedding_function


# set session state to default vectorstore
def default_vectorstore():
    # FIXME: Assumption: All required configurations are available in the session state.
    config = st.session_state["defaults"]["chroma"]
    config_chroma_dir = config["chroma_dir"]
    config_collection = config["collection"]
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
# FIXME: Assumption is that all required configuration attributes are present
def default_llm():
    config = st.session_state["defaults"]["llm"]
    if config["llm_type"] != "OpenAI":
        raise ValueError
    default_model = config["model"]
    kwargs = config["model_kwargs"]
    llm = OpenAI(model_name=default_model,
                 temperature=kwargs["temperature"],
                 max_tokens=kwargs["max_tokens"])
    st.session_state["llm"] = llm
    st.session_state["llm_name"] = default_model
    st.session_state["llm_kwargs"] = kwargs


# set session state to default retriever based on the vectorstore
def default_retriever():
    config = st.session_state["defaults"]["retriever"]
    config_search_type = config["search_type"]
    config_retriever = config["search_kwargs"]
    vectordb = st.session_state["vectorstore"]
    retriever = vectordb.as_retriever(search_type=config_search_type, search_kwargs=config_retriever)
    retriever_kwargs = {"search_type": config_search_type, "kwargs": config_retriever}
    st.session_state["retriever"] = retriever
    st.session_state["retriever_name"] = "Vectorstore retriever"
    st.session_state["retriever_kwargs"] = retriever_kwargs


# show the details of a global configuration
# name is one of the elements described at the top of this file
def show_config(conf_name, show_details=False, prefix=""):
    print_name = conf_name.capitalize()
    if conf_name == "llm":
        print_name = "LLM"

    st.write(f"### {prefix + print_name}")
    st.write(f'{print_name} name: {st.session_state[conf_name + "_name"]}')

    if show_details:
        details = st.session_state[conf_name + "_kwargs"]
        if len(details.keys()) > 0:
            for detail in sorted(list(details.keys())):
                st.write(f'{detail}: {details[detail]}')
        else:
            st.write("No details available")


# show the details of a global configuration
# name is one of the elements described at the top of this file
def show_expander_config(conf_name, show_details=False, prefix=""):
    print_name = conf_name.capitalize()
    if conf_name == "llm":
        print_name = "LLM"

    with st.expander(f'# {print_name}: {st.session_state[conf_name + "_name"]}'):
        details = st.session_state[conf_name + "_kwargs"]
        if len(details.keys()) > 0:
            for detail in sorted(list(details.keys())):
                st.write(f'{detail}: {details[detail]}')
        else:
            st.write("No details available")
