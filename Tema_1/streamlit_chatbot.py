import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import streamlit as st

dotenv.load_dotenv()

# Configurar la página de la aplicación
st.set_page_config(page_title="Chatbot Basico", page_icon="🤖")
st.title("🤖 Chatbot basico con LangChain y Streamlit")
st.markdown(
    "### Este es un ***chatbot de ejemplo*** construido con **LangChain + Streamlit**. ¡Escribe tu mensaje abajo para comenzar!"
)


chat_model = ChatOpenAI(model="gpt-5.4-mini", temperature=0.5)


# Inicializar el historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar mensajes previos en la interfaz

for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje en pantalla
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(msg.content)


# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")
if pregunta:
    # Mostrar inmediatamente el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Almacenamos el mensaje en la memoria de streamlit
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
