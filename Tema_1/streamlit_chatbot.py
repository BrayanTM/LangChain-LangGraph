import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

dotenv.load_dotenv()

# Configurar la página de la aplicación
st.set_page_config(page_title="Chatbot Basico", page_icon="🤖")
st.title("🤖 Chatbot basico con LangChain y Streamlit")
st.markdown(
    "### Este es un ***chatbot de ejemplo*** construido con **LangChain + Streamlit**. ¡Escribe tu mensaje abajo para comenzar!"
)


with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"])

    # Nuevo! Personalidad configurable\
    personality = st.selectbox(
        "Personalidad del Asistente",
        [
            "Útil y amigable",
            "Profesional y formal",
            "Casual y relajado",
            "Experto y técnico",
            "Creativo y divertido",
        ],
    )


chat_model = ChatOpenAI(model=model_name, temperature=temperature)


system_messages = {
    "Útil y amigable": "Eres un asistente útil y amigable llamado ChatBot Pro. Responde de manera clara y concisa.",
    "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
    "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
    "Experto y técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con presición técnica.",
    "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre.",
}


# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# Crear el template de prompt con comportamiento especifico
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        # Mensaje del sistema, defina la personaidad una sola vez.
        ("system", system_messages[personality]),
        # El historial y mensaje actual - se manejan como texto formateado.
        (
            "human",
            "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}",
        ),
    ]
)


# Crear cadena usando LCEL (Langchain Expression Language)
chain = chat_prompt_template | chat_model


# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje en pantalla
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(msg.content)


if st.button("🗑️ Nueva conversación"):
    # ¿Qué necesitas limpiar?
    st.session_state.mensajes = []
    # ¿Qué función de Streamlit refresca la página?
    st.rerun()


# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")
if pregunta:
    # Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        # Mostrar la respuesta en la interfaz
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Streaming de la respuesta
            for chunk in chain.stream(
                {"mensaje": pregunta, "historial": st.session_state.mensajes}
            ):
                if isinstance(chunk.content, str):
                    full_response += chunk.content
                response_placeholder.markdown(full_response + "|")

            response_placeholder.markdown(full_response)

        # Almacenamos el mensaje en la memoria de streamlit
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))

    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info(
            "Verifica que tu API KEY de OpenAI este configurado correctamente en las variables de entorno"
        )
