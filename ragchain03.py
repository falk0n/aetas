import time
import os

import streamlit as st

from langchain.document_loaders import PDFMinerLoader
from langchain.text_splitter import CharacterTextSplitter, NLTKTextSplitter
import langchain.embeddings as lce

import bsi

import fscutils as fsc

#
# ragchain03.py
#
# Load and embed all documents in the given directory into the chroma collection.
# The action starts at let's GET REAL!
#

# text_splitter for later use
split_para = CharacterTextSplitter(separator="\n\n", chunk_size=1, chunk_overlap=0, keep_separator=False)
split_line = CharacterTextSplitter(separator="\n", chunk_size=1, chunk_overlap=0, keep_separator=False)
split_sentence = NLTKTextSplitter(separator="\n", language="german")

# metadata attributes to put into vector store
config_metadata = ["baustein_name",
                   "baustein_id",
                   "chapter_name",
                   "section_name",
                   "requirement_name",
                   "requirement",
                   "source"]

# embedding models to choose from
config_default_hf_embeddings = ["multilingual-e5-large", "all-mpnet-base-v2", "all-MiniLM-L6-v2"]
config_embedding_names = {
    "multilingual-e5-large": "intfloat/multilingual-e5-large",          # MTEB retrieval rank 6
    "instructor-xl": "hkunlp/instructor-xl",                            # MTEB retrieval rank 14
    "instructor-large": "hkunlp/instructor-large",                      # MTEB retrieval rank 23
    "instructor-base": "hkunlp/instructor-base",                        # MTEB retrieval rank 29
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",     # MTEB retrieval rank 37
    "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2"        # MTEB retrieval rank 42
}


st.title("Load directory")
st.header("Configurations")
# directory with pdf documents from BSI
config_filedir = "/home/falk/work/nlp/corpus/bsi_sample/"
my_filedir = st.text_input(label="Directory to load:", value=config_filedir)

# whether to split paragraphs into sentences
my_split_sentences = fsc.true_false_radio("split paragraphs into sentences", default=True)

# embedding model to use
my_embedding = st.radio(label="HuggingFace embedding model", options=config_embedding_names, index=0, horizontal=True)
my_compute_method = st.radio(label="Computing method", options=["cpu", "cuda"], index=0, horizontal=True)

# location of chroma vectorstore
config_chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
my_chroma_dir = st.text_input(label="location of chroma vectorstore", value=config_chroma_dir)

# name of chroma collection where we store the documents
config_collection = "sample_document"
my_collection = st.text_input(label="Chroma collection name: ", value=config_collection)    # choose collection name

# initialize the embedding function of choice
if my_embedding in config_default_hf_embeddings:
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )
else:   # initialize InstructEmbedding
    embedding_function = lce.HuggingFaceInstructEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )


# Let's GET REAL
# Putting this into the if statement due to streamlit logic (re-evaluate of whole script at every change).
st.header("Processing files")
my_compute_embedding = fsc.true_false_radio("compute embedding and store", default=False)
if my_compute_embedding:
    vectordb = fsc.connect_to_empty_vectorstore(my_collection, embedding_function, my_chroma_dir)
    time_start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    for filename in os.listdir(my_filedir):
        infile = my_filedir + filename
        st.caption(filename)
        loader = PDFMinerLoader(infile)
        docs_raw = loader.load_and_split(text_splitter=split_para)
        docs_bsi = bsi.parse(docs_raw)
        if my_split_sentences:
            docs_split = split_line.transform_documents(split_sentence.transform_documents(docs_bsi))
        else:
            docs_split = docs_bsi
        docs_cleaned = fsc.clean_metadata(docs_split, config_metadata)

        vectordb.add_documents(docs_cleaned)
    time_end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"total processing time (mostly embedding): { duration_ms} [ms]")
    data = vectordb.get(include=["metadatas"])
    st.write(f'Number of entries in vectorstore: {len(data["ids"])}')
else:
    st.write("no processing done")
