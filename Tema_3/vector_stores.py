from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


loader = PyPDFDirectoryLoader("C:\\Projects\\LangChain&LangGraph\\Tema_3\\contratos")
documentos = loader.load()


print(f"Se cargaron: {len(documentos)} documentos desde el directorio")


text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs_split = text_spliter.split_documents(documentos)


print(f"Se crearon: {len(docs_split)} chunks de texto.")


vectorStore = Chroma.from_documents(
    documents=docs_split,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="C:\\Projects\\LangChain&LangGraph\\Tema_3\\chroma_db",
)


consulta = "¿Dónde se encuentra el local del contrato en el que participa María Jiménez Campos?"

resultados = vectorStore.similarity_search(consulta, k=2)

print("Top 2 documentos mas similares a la consulta: \n")
for i, doc in enumerate(resultados, start=1):
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata} \n")
