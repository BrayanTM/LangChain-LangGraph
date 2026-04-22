import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
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


chat_model = ChatOpenAI(model=model_name, temperature=temperature)


# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# Crear el template de prompt con comportamiento especifico
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
 
Historial de conversación:
{historial}
 
Responde de manera clara y concisa a la siguiente pregunta: {mensaje}""",
)


# Crear cadena usando LCEL (Langchain Expression Language)
chain = prompt_template | chat_model


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
