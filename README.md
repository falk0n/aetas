# aetas
## tools for RAG with langchain

### Introduction
This repo contains the code for the experimental platform AETAS.
It is designed to do some easy experiments with retrieval augmented generation using the langchain framework.
AETAS is not an end user application! It is target at engineers who want to experiments with some embeddings
and want a little bit more comfort than the Python command line or Jupyter notebooks provide.
Many interesting experiments are  going to require you to writing additional modules.

### Running the application
For starting the application the run command is intended.
It assumes you have configured the following environment variables correctly:
* HUGGINGFACEHUB_API_TOKEN
* SENTENCE_TRANSFORMERS
* HF_HOME
* OPENAI_API_KEY

### Installation
You should set up a virtual environment for python using requirements.txt.
Please note that pytorch is not part of requirements.txt because on my system it is installed globally.
So maybe you need to install it additionally on your machine.

### Testing
In general, the code has been developed on archlinux. No testing on other platforms has been done yet.
The application is only standard python functionality, so there should no real problems running with another Linux.

~~~~