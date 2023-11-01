import time

import streamlit as st

from langchain.document_loaders import PDFMinerLoader
from langchain.text_splitter import CharacterTextSplitter, NLTKTextSplitter
import langchain.embeddings as lce

import bsi

import fscutils as fsc

#
# ragchain02.py
#
# Show for the first part of the RAG ingestion chain.
# Streamlit application to show some of the moving parts and interim results.
# The action starts at let's GET REAL!
#


st.title("Load one document")

st.header("Document configuration")
config_filedir = "/home/falk/work/nlp/corpus/bsi_sample/"  # default directory
config_filename = "SYS.1.3 Server unter Linux und Unix.pdf.clean.pdf"  # default filename
my_filedir = st.text_input(label="Verzeichnis:", value=config_filedir)  # directory after user input
my_filename = st.text_input(label="Dokument:", value=config_filename)  # filename after user input
infile = my_filedir + my_filename


#
# Let's GET REAL
# 1. Load the PDF and split into lines
# PDFMinerLoader gives\n\n at paragraph breaks etc. and \n at normal line breaks.
# paragraphs are separated already at loading time
loader = PDFMinerLoader(infile)
split_para = CharacterTextSplitter(separator="\n\n", chunk_size=1, chunk_overlap=0, keep_separator=False)
docs_raw = loader.load_and_split(text_splitter=split_para)
my_show_raw = fsc.true_false_radio("show raw output of PDF loader (paragraphs already broken up)", default=False)
if my_show_raw:
    st.write(docs_raw)


# 2. Preprocess PDF (Baustein IT-Grundschutz)
docs_bsi = bsi.parse(docs_raw)
my_show_bsi = fsc.true_false_radio("show Document list after BSI specific parsing", default=False)
if my_show_bsi:
    st.write(docs_bsi)


# 3. Split PDF into sentences
# NOTE: chunk_size in NLTKTextSplitter still is characters due to the standard counting method.
# FIXME: There are still some occurrences where the sentences are not correctly recognized (e.g. in "z.B.").
# TODO: Make it somehow possible to have overlapping sentences.
# E.g. each chunk is two sentences, sharing one with the previous and one with the next chunk.
split_sentence = NLTKTextSplitter(separator="\n", language="german")
split_line = CharacterTextSplitter(separator="\n", chunk_size=1, chunk_overlap=0, keep_separator=False)

my_split_sentences = fsc.true_false_radio("split paragraphs into sentences", default=True)
if my_split_sentences:
    docs_split = split_line.transform_documents(split_sentence.transform_documents(docs_bsi))
else:
    docs_split = docs_bsi

my_show_split = fsc.true_false_radio("show content after splitting into sentences", default=False)
if my_show_split:
    show_me = fsc.list_of_lines(docs_split)
    st.write(show_me)


# 4. Select metadata to keep (-> these will be available in the vector storage for additional filtering)
config_metadata = ["baustein_name",
                   "baustein_id",
                   "chapter_name",
                   "section",
                   "section_name",
                   "requirement",
                   "requirement_name",
                   "source"]
all_metadata = fsc.get_all_metadata(docs_bsi)
my_metadata = st.multiselect(label="keep only these metadata", options=all_metadata, default=config_metadata)
docs_cleaned = fsc.clean_metadata(docs_split, my_metadata)

# 5. Show final Document List (ready to embed)
my_show_clean = fsc.true_false_radio("show Document list after cleaning metadata")
if my_show_clean:
    st.write(docs_cleaned)


st.header("Retrieval model")
# 6. Choose embedding model
config_embedding_names = {
    "multilingual-e5-large": "intfloat/multilingual-e5-large",          # MTEB retrieval rank 6
    "instructor-xl": "hkunlp/instructor-xl",                            # MTEB retrieval rank 14
    "instructor-large": "hkunlp/instructor-large",                      # MTEB retrieval rank 23
    "instructor-base": "hkunlp/instructor-base",                        # MTEB retrieval rank 29
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",     # MTEB retrieval rank 37
    "all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2"        # MTEB retrieval rank 42
}
config_default_hf_embeddings = ["multilingual-e5-large", "all-mpnet-base-v2", "all-MiniLM-L6-v2"]

# User's choice: embedding function
my_embedding = st.radio(label="HuggingFace embedding model", options=config_embedding_names, index=0, horizontal=True)
my_compute_method = st.radio(label="Computing method", options=["cpu", "cuda"], index=0, horizontal=True)

# initialize the embedding function of choice
# TODO: use cache_folder or set SENTENCE_TRANSFORMERS_HOME
if my_embedding in config_default_hf_embeddings:
    embedding_function = lce.HuggingFaceEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )
else:
    # default embed_instruction is "represent the document for retrieval". So we don't need to set it explicitly.
    embedding_function = lce.HuggingFaceInstructEmbeddings(
        model_name=config_embedding_names[my_embedding],
        model_kwargs={"device": my_compute_method},
        encode_kwargs={"normalize_embeddings": True},
    )

# 7. Connect to chroma
config_chroma_dir = "/home/falk/work/nlp/vectordb/chromadb"
my_chroma_dir = st.text_input(label="location of chroma vectorstore", value=config_chroma_dir)

config_collection = "sample_document"
my_collection = st.text_input(label="Chroma collection name: ", value=config_collection)

vectordb = fsc.connect_to_empty_vectorstore(my_collection, embedding_function, my_chroma_dir)

# default is False -> we can adjust parameters before starting a compute intensive embedding
my_compute_embedding = fsc.true_false_radio("compute embedding and store", default=False)
if my_compute_embedding:
    time_start = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    vectordb.add_documents(docs_cleaned)
    time_end = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    duration_ms = int((time_end - time_start)/1000000)
    st.write(f"embedding time: { duration_ms} [ms]")

data = vectordb.get(include=["metadatas"])
st.write(f'Number of entries in vectorstore: {len(data["ids"])}')
