import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()


llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.7)


plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente: ",
)

chain = plantilla | llm | StrOutputParser()


resultado = chain.invoke("Brayan")
print("Respuesta del modelo: ", resultado)
