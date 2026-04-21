import dotenv
from langchain_openai import ChatOpenAI


dotenv.load_dotenv()


llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.7)


pregunta = "¿En qué año llego el ser humano a la luna por primera vez?"
print("Pregunta: ", pregunta)
respuesta = llm.invoke(pregunta)
print("Respuesta del modelo: ", respuesta.content)
