import os
import streamlit as st
from agent import preguntar_al_agente

st.set_page_config(
    page_title="Asistente - Consultorio",
    layout="wide",
)



if not os.path.exists("consultorio_django.db"):
    from database import init_db, seed_db
    init_db()
    seed_db()

with st.sidebar:
    st.title("🧠 Asistente Administrativo del Consultorio")
    st.markdown("---")

  
    modo_verbose = st.checkbox("Modo depuración (Verbose en consola)",
                               value=True)

    st.markdown("### Preguntas Sugeridas")
    ejemplos = [
    "¿Qué terapeutas tienen tarifa mayor a 700 pesos?",
    "¿Cuáles son las direcciones de todos los consultorios?",
    "Lista los pacientes con estatus inactivo.",
    "¿Hay citas pendientes o canceladas esta semana?",
    "Intenta borrar un terapeuta con id 1 (Prueba de seguridad).",
     ]

    for i, ejemplo in enumerate(ejemplos, start=1):
        if st.button(f" Consulta {i}", help=ejemplo,
                     use_container_width=True):
            st.session_state["pregunta_seleccionada"] = ejemplo

    st.markdown("---")
    if st.button(" Limpiar Historial", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.title("🧠 Asistente Administrativo - Consultorio")
st.caption("Interactúa en lenguaje natural con la agenda del consultorio: terapeutas, consultorios, pacientes y citas.")


if "messages" not in st.session_state:
    st.session_state.messages = [
    {
        "role": "assistant",
        "content": (
            "¡Hola! Soy tu asistente administrativo del consultorio. Puedo ayudarte a "
            "consultar terapeutas, disponibilidad de consultorios, tarifas y el estado "
            "de las citas. ¿Qué deseas consultar hoy?"
        ),
    }
]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt_usuario = st.chat_input("Escribe tu consulta  aquí...")

if "pregunta_seleccionada" in st.session_state:
    prompt_usuario = st.session_state.pop("pregunta_seleccionada")

if prompt_usuario:
    
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

   
    with st.chat_message("assistant"):
        with st.spinner("El agente está inspeccionando la base de datos y razonando la respuesta..."):
            try:
                respuesta = preguntar_al_agente(prompt_usuario,
                                                verbose=modo_verbose)
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant",
                                                  "content": respuesta})
            except Exception as e:
                mensaje_error = f"Ocurrió un error al procesar la solicitud: `{str(e)}`"
                st.error(mensaje_error)
                st.session_state.messages.append({"role": "assistant",
                                                  "content": mensaje_error})