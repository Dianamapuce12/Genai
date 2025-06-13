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



documents = SimpleDirectoryReader('cv').load_data()


Settings.llm = OpenAI(model="gpt-4.1")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)

index = VectorStoreIndex.from_documents(documents)





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
