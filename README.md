# aetas
## tools for RAG with langchain

### Introduction
This repo contains the code for the experimental platform AETAS.
It is designed to do some easy experiments with retrieval augmented generation
using the langchain framework and models from HuggingFace.co
AETAS is not an end user application!
It is targeted at engineers who want to experiment with some embeddings
and want a little bit more comfort than the Python command line or a Jupyter notebooks provide.
Many interesting experiments are  going to require you to write additional modules.
The general architecture uses streamlit. So all the modules go into the pages directory.

### Running the application
The application is contained in streamlit-app directory. Make it your working directory.
Then, start the application the run command.
It assumes you have configured the following environment variables correctly:
* HUGGINGFACEHUB_API_TOKEN
* SENTENCE_TRANSFORMERS
* HF_HOME
* OPENAI_API_KEY

As usual with streamlit it listens on localhost:8501.
Strictly speaking, you don't need the directories corpus and xml2txt.
These contain the code used to prepare the BSI IT-Grundschutz Bausteine
which were used for the experiments.

### Installation
You should set up a virtual environment for python using requirements.txt.
Please note that pytorch is not part of requirements.txt
because on my system it is installed globally.
So maybe you need to install it additionally on your machine.

### Testing
In general, the code has been developed on archlinux.
No testing on other platforms has been done yet.
The application uses only standard python features,
so there should be no real problems running on another reasonable system.

~~~~