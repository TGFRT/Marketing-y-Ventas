import streamlit as st
import google.generativeai as gen_ai
import time
import PyPDF2

# Configura Streamlit
st.set_page_config(
    page_title="CREADOR DE MARKETING CON INGENIAR",
    page_icon=":rocket:",
    layout="centered",
)

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configura el modelo de Google Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configuración de generación
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Título de la web
st.title("CREADOR DE MARKETING CON INGENIAR 🚀")

# Selección de la funcionalidad
option = st.selectbox("Elige una opción:", ("Creador de Contenido", "Analizador de Audiencia", "Creador de Campañas de Marketing"))

# Barra de progreso al cambiar de opción
with st.spinner("Cargando..."):
    time.sleep(1)

if option == "Creador de Contenido":
    st.header("Creador de Contenido")

    tema = st.text_area("Introduce el tema del contenido que deseas generar:")
    
    # Tipos de contenido
    tipo_contenido = st.selectbox("Selecciona el tipo de contenido:", ["Artículo", "Publicación para Redes Sociales", "Boletín"])

    if st.button("Generar Contenido"):
        if not tema:
            st.error("Por favor, ingresa un tema para generar contenido.")
        else:
            prompt = f"""
            Genera un {tipo_contenido.lower()} sobre el siguiente tema:
            Tema: {tema}
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un generador de contenido de marketing."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Contenido Generado:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Ocurrió un error al generar el contenido: {str(e)}")

elif option == "Analizador de Audiencia":
    st.header("Analizador de Audiencia")

    # Entradas para datos del público objetivo
    datos_publico = st.text_area("Ingresa datos sobre tu público objetivo (intereses, comportamientos, etc.):")

    # Subida de archivo PDF
    uploaded_file = st.file_uploader("Sube un archivo PDF con estadísticas adicionales", type="pdf")

    if st.button("Analizar Audiencia"):
        if not datos_publico:
            st.error("Por favor, ingresa información sobre tu público objetivo.")
        else:
            # Leer contenido del PDF si se sube uno
            pdf_content = ""
            if uploaded_file is not None:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"

            prompt = f"""
            Analiza la siguiente información sobre mi público objetivo:
            Datos del público: {datos_publico}
            Información adicional del PDF: {pdf_content}
            
            Proporciona un análisis de sus necesidades, intereses y hábitos de consumo.
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un analizador de audiencia de marketing."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Análisis de Audiencia:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Ocurrió un error al analizar la audiencia: {str(e)}")

else:  # Opción: Creador de Campañas de Marketing
    st.header("Creador de Campañas de Marketing")

    # Entradas para la campaña
    objetivos = st.text_area("Introduce los objetivos de tu campaña de marketing:")
    mensaje = st.text_area("¿Qué mensaje quieres transmitir en tu campaña?")
    
    if st.button("Generar Estrategia de Marketing"):
        if not objetivos or not mensaje:
            st.error("Por favor, completa todos los campos antes de generar la estrategia.")
        else:
            prompt = f"""
            Crea una estrategia de marketing basada en los siguientes objetivos y mensajes:
            Objetivos: {objetivos}
            Mensaje: {mensaje}
            
            Proporciona sugerencias sobre plataformas, canales y mensajes específicos para alcanzar a la audiencia.
            """

            try:
                model = gen_ai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=generation_config,
                    system_instruction="Eres un creador de campañas de marketing."
                )

                chat_session = model.start_chat(history=[])

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)  # Simulación de tiempo de espera
                    progress.progress(i + 1)

                gemini_response = chat_session.send_message(prompt)

                st.markdown(f"## Estrategia de Marketing Generada:\n{gemini_response.text}")
            except Exception as e:
                st.error(f"Ocurrió un error al generar la estrategia: {str(e)}")
