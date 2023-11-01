# aetas
## tools for RAG with langchain

### Introduction
This repository contains some tools and code snippets for creating a RAG type of chatbot with langchain.
In case of questions please check back with me.

For running the code you should set up a virtual environment for python using requirements.txt.
Please note that pytorch is not part of the venv because it is installed globally on my system.
In general, the code has been developed on archlinux. No testing on other platforms has been done.

Python scripts assume you have configured the following environment variables correctly:
* HUGGINGFACEHUB_API_TOKEN
* SENTENCE_TRANSFORMERS
* HF_HOME
* OPENAI_API_KEY

### Major Tools
* ragchain02.py: reading one pdf file and  trace its preprocessing
* ragchain03.py: load a directory of pdf documents into chroma vectorstore
* retrieve02.py: retrieve documents from the vector store

