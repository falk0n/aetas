import streamlit as st
import langchain.embeddings as lce

#
# config-embedding.py
# Configure the global embedding object in session state.
# In this case it is an instruct embedding model from Huggingface.
# Please note, that the model might be downloaded from Huggingface if not already locally cached.
#
st.write("# Configure Instruct Embedding")
st.write("#### Current embedding model")
widget = st.text(f'Embedding model name: {st.session_state["embedding_name"]}')


# select embedding model and computing preference
st.write("#### New embedding model")
embedding_names = {
    "instructor-base": "hkunlp/instructor-base",                        # MTEB retrieval rank 29
    "instructor-large": "hkunlp/instructor-large",                      # MTEB retrieval rank 23
    "instructor-xl": "hkunlp/instructor-xl"}                            # MTEB retrieval rank 14
my_embedding = st.radio(label="Embedding model", options=embedding_names, index=0, horizontal=True)
my_compute_method = st.radio(label="Compute method", options=["cpu", "cuda"], index=0, horizontal=True)

# query instructions make the instruct models stand out
config_query_instruction = "Represent the question for retrieving supporting documents:"
my_query_instruction = st.text_input(label="Query instruction", value=config_query_instruction)

# initialize the embedding model
embedding_model = lce.HuggingFaceInstructEmbeddings(
    model_name=embedding_names[my_embedding],
    model_kwargs={"device": my_compute_method},
    query_instruction=my_query_instruction,     # defined only in case of instruct embedding
    encode_kwargs={"normalize_embeddings": True})


# finally, update the global state after pressing the confirm button
if st.button("Confirm new embedding model"):
    st.session_state["embedding"] = embedding_model
    st.session_state["embedding_name"] = embedding_names[my_embedding]
    st.session_state["embedding_kwargs"] = {"embedding_device": my_compute_method}
    # update the model information at the top of the page
    widget.text(f'model_name: {st.session_state["embedding_name"]}')


st.write("#### Hinweise")
st.write("""
Wenn das Embedding Model geändert wird, sollte auch der Vectorstore neu konfiguriert werden.
Das Embedding Model wird bei der Anlage des Vectorstore benötigt.
Ein bestehender Vectorstore wird nicht automatisch aktualisiert.
""")
