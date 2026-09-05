import dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

dotenv.load_dotenv()

# 1. Cargar el documento PDF
loader = PyPDFLoader("C:\\Projects\\LangChain&LangGraph\\Tema_3\\quijote.pdf")
pages = loader.load()

# Dividir el texto en chunks mas pequeños
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)

chunks = text_splitter.split_documents(pages)

# 3. Pasar el texto al LLM
llm = ChatOpenAI(model="gpt-5.6-luna", temperature=0.2)
summaries = []

for i, chunk in enumerate(chunks):
    if i > 2:
        break
    response = llm.invoke(
        f"Haz un resumen de los puntos mas importantes del siguiente texto: {chunk.page_content}"
    )
    summaries.append(response.content)

final_summary = llm.invoke(
    f"Combina y sintetiza estos resumenes en un resumen coherente y completo: {' '.join(summaries)} "
)
print(final_summary.content)
