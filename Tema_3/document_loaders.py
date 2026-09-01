"""Loader para PDFs"""
# from langchain_community.document_loaders import PyPDFLoader


# loader = PyPDFLoader("C:\\Projects\\LangChain&LangGraph\\Tema_3\\CV.pdf")

# pages = loader.load()

# for i, page in enumerate(pages):
#     print(f"=== Pagina {i + 1} ===")
#     print(f" Contenido: {page.page_content}")
#     print(f"Metadatos: {page.metadata}")

"""Loader para Webs"""
from langchain_community.document_loaders import WebBaseLoader


loader = WebBaseLoader("https://www.josecode.dev/")

pages = loader.load()
print(pages)
