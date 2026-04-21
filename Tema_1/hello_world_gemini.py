import dotenv
import logging
from langchain_google_genai import ChatGoogleGenerativeAI


dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.7)


pregunta = "¿En qué año llego el ser humano a la luna por primera vez?"
logging.info("Pregunta: %s", pregunta)
respuesta = llm.invoke(pregunta)
logging.info("Respuesta del modelo: %s", respuesta.content)
