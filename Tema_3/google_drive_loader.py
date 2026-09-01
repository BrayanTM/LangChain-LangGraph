from langchain_community.document_loaders import GoogleDriveLoader
import dotenv

dotenv.load_dotenv()

credentials_path = "C:\\Projects\\LangChain&LangGraph\\Tema_3\\keys.json"
token_path = "C:\\Projects\\LangChain&LangGraph\\Tema_3\\token.json"

loader = GoogleDriveLoader(
    folder_id="1T1-D28M3Yu8T--VLxy_ew-obZRIhtrHh",
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=True,
)

documents = loader.load()
print(f"Metadatos {documents[0].metadata}")
print(f"Contenido {documents[0].page_content}")
