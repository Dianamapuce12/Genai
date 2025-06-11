from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import PromptTemplate
import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.openai  import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
import streamlit as st
from llama_index.core.retrievers import VectorIndexRetriever 
from llama_index.core.query_engine import RetrieverQueryEngine


load_dotenv()

st.title("SuperRH RAG for you!")
st.write("Gagnez plus de temp juste en demandant le metier souhaitée")


try:
    openai_api_key = st.secrets["openai_api_key"]
    
    # Validate the API key format
    if not openai_api_key.startswith("sk-"):
        st.error("Invalid OpenAI API key format. The key should start with 'sk-'")
        st.stop()

Settings.llm = OpenAI(model="gpt-4o")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)

index = VectorStoreIndex.from_documents(documents)

text_qa_template_str = (
    """Tu es un assistant IA spécialisé dans l'analyse des cv. L'utilisateur envoie une question par rapport 'un metier. Ta tache est de chercher la reponse dans les cv fournis dans ta base de connaissance pour donner la liste des gens appropriés à ce metier.
    Voilà le contexte :
    {context}

    Instruction :
    1. 
    2. Repond sous forme de liste et grand titre en gras.
    2. Tu répond poliment et avec les nom des candidats lié à ce poste dans ta base de connaissance.
    3. Pas de hallucination .

    Question : {question}\n
    Réponse : """
)



text_qa_template = PromptTemplate(text_qa_template_str)

retriever = VectorIndexRetriever(index, similarity_top_k=10, filter=None)
st.write(retriever)

query_engine = RetrieverQueryEngine.from_args(retriever)
query_engine.update_prompts({"response_synthesizer:text_qa_template": text_qa_template})
st.write(query_engine)
st.subheader("Cherchez votre métier ci-dessous:")
query = st.text_input("recherchez votre metier", placeholder="Devellopeur")

if query:
    response = query_engine.query(query)
    st.write("##Reponse:")
    st.write(str(response))
