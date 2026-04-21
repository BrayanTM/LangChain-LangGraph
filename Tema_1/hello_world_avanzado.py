import dotenv
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)


llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente: ",
)
