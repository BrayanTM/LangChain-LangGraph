from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
import dotenv
import json

dotenv.load_dotenv()


# Configuración del modelo
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)


def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    # Pista: usa .strip() para eliminar espacios
    text_striped = text.strip(" ")
    # Pista: limita a 500 caracteres con slicing [:500]
    text_clean = text_striped[:500]
    return text_clean  # ¡Completa aquí!


# Convertir la función en un Runnable
preprocessor = RunnableLambda(preprocess_text)


def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume el siguiente texto en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content


summary_branch = RunnableLambda(generate_summary)


def analyze_sentiment(text):
    """Analiza el sentimiento y devuelve resultado estructurado"""
    prompt = f"""Analiza el sentimiento del siguiente texto.
    Responde ÚNICAMENTE en formato JSON válido:
    {{"sentimiento": "positivo|negativo|neutro", "razon": "justificación breve"}}
    
    Texto: {text}"""

    response = llm.invoke(prompt)
    try:
        return json.loads(str(response.content))
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "Error en análisis"}


sentiment_branch = RunnableLambda(analyze_sentiment)


def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"],
    }


merger = RunnableLambda(merge_results)


parallel_analysis = RunnableParallel(
    {"resumen": summary_branch, "sentimiento_data": sentiment_branch}
)


# Cadena completa
chain = preprocessor | parallel_analysis | merger


reviews_batch = [
    "Excelente producto, muy satisfecho con la compra",
    "Terrible calidad, no la recomiendo para nada",
    "Esta bien, cumple su funcion basica pero nada especial",
]


result_batch = chain.batch(reviews_batch)


print(result_batch)
