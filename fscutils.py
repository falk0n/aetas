import streamlit as st

import chromadb

from langchain.docstore.document import Document
from langchain.vectorstores import Chroma


# show and evaluate a radio button with the boolean values True, False
def true_false_radio(text, default=True):
    default_index = 0
    if not default:
        default_index = 1
    value = st.radio(label=text, options=["True", "False"], index=default_index, horizontal=True)
    result = True
    if value == "False":
        result = False
    return result


# helper function to convert a Document into a dict() (with entries "page_content" and "metadata")
def conv_document_to_dict(chunk):
    return chunk.dict()


# helper function to recreate a Document from a dict() (with entries "page_content" and "metadata")
def conv_dict_to_document(chunk):
    result = Document(
        page_content=chunk["page_content"],
        metadata=chunk["metadata"],
    )
    return result


# helper function to convert a list of Document into a list of dict()
def conv_document_list_to_dicts(docs):
    return list(map(conv_document_to_dict, docs))


# helper function to recreate a list Document from a list of dict()
def conv_dict_list_to_documents(dicts):
    return list(map(conv_dict_to_document, dicts))


# return a sorted list of all metadata attribute names in the given Document list
def get_all_metadata(docs):
    chunks = conv_document_list_to_dicts(docs)
    names = set()
    for entry in chunks:
        names |= set(entry["metadata"].keys())
    return sorted(names)


# helper function to remove all metadata attributes from docs that are not in allowed_metadata
def clean_metadata(docs, allowed_metadata):
    allowed = set(allowed_metadata)
    dicts = conv_document_list_to_dicts(docs)
    for entry in dicts:
        new_metadata = dict()
        meta_copy = allowed & set(entry["metadata"].keys())
        for key in meta_copy:
            new_metadata[key] = entry["metadata"][key]
        entry["metadata"] = new_metadata
    return conv_dict_list_to_documents(dicts)


# connect to local chroma vectorstore as specified
# Changing the vectorstore langchain is using is as easy as changing this function.
def connect_to_empty_vectorstore(collection, embedding, chroma_dir):
    # We start with a chroma client and then make sure the collection is fresh.
    # required because: embedding function is part of the collection definition
    # I didn't find a more elegant solution using only langchain methods.
    chroma_client = chromadb.PersistentClient(chroma_dir)
    try:
        chroma_client.delete_collection(collection)     # Throws ValueError if collection does not exist
    finally:
        chroma_client.get_or_create_collection(name=collection, embedding_function=embedding)
    # 2. Now we can create the langchain vectorstore and proceed
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=collection,
        persist_directory=chroma_dir,
        embedding_function=embedding)
    return vectorstore


def list_of_lines(docs):
    dicts = conv_document_list_to_dicts(docs)
    result = [ entry["page_content"] for entry in dicts]
    return result
