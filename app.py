import streamlit as st
import google.generativeai as gen_ai
import requests
import io
from PIL import Image
import concurrent.futures
import random
from googletrans import Translator
import time

# Configura Streamlit
st.set_page_config(page_title="CREADOR DE MARKETING CON INGENIAR", page_icon=":rocket:", layout="centered")

# Obtén la clave API de las variables de entorno
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
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
    tipo_contenido = st.selectbox("Selecciona el tipo de contenido:", ["Artículo", "Publicación para Redes Sociales", "Boletín", "Anuncio"])

    # Generador de imágenes
    user_prompt = st.text_input("¿Qué imagen deseas generar?")

    # Definir la API y los headers de Hugging Face
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response

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

    if st.button("Generar Imágenes"):
        if user_prompt:
            # Crear el objeto traductor
            translator = Translator()
            translated_prompt = translator.translate(user_prompt, src='es', dest='en').text
            
            # Variar ligeramente el prompt para las dos imágenes
            prompt_suffix_1 = f" with vibrant colors {random.randint(1, 1000)}"
            prompt_suffix_2 = f" with a dreamy atmosphere {random.randint(1, 1000)}"
            prompt_1 = translated_prompt + prompt_suffix_1
            prompt_2 = translated_prompt 
            
            # Generar las imágenes en paralelo usando concurrent.futures
            with st.spinner("Generando imágenes..."):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_image_1 = executor.submit(query, {"inputs": prompt_1})
                    future_image_2 = executor.submit(query, {"inputs": prompt_2})
                    
                    # Obtener los resultados
                    image_bytes_1 = future_image_1.result()
                    image_bytes_2 = future_image_2.result()

            # Manejo de errores
            if image_bytes_1.status_code == 429 or image_bytes_2.status_code == 429:
                st.error("Error 429: Has alcanzado el límite de uso gratuito. Considera suscribirte a IngenIAr mensual.")
            else:
                # Comprobar si hay otros errores
                if image_bytes_1.status_code != 200 or image_bytes_2.status_code != 200:
                    st.error("Hubo un problema al generar las imágenes. Intenta de nuevo más tarde.")
                else:
                    # Abrir las imágenes desde las respuestas
                    st.session_state.image_1 = Image.open(io.BytesIO(image_bytes_1.content))
                    st.session_state.image_2 = Image.open(io.BytesIO(image_bytes_2.content))

    # Si las imágenes ya se han generado, mostrarlas
    if 'image_1' in st.session_state and 'image_2' in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(st.session_state.image_1, caption="Imagen 1", use_column_width=True)
        
        with col2:
            st.image(st.session_state.image_2, caption="Imagen 2", use_column_width=True)

        # Crear botones de descarga para ambas imágenes
        buf1 = io.BytesIO()
        buf2 = io.BytesIO()
        st.session_state.image_1.save(buf1, format="PNG")
        st.session_state.image_2.save(buf2, format="PNG")
        buf1.seek(0)
        buf2.seek(0)

        col1.download_button(
            label="Descargar Imagen 1",
            data=buf1,
            file_name="imagen_1.png",
            mime="image/png"
        )

        col2.download_button(
            label="Descargar Imagen 2",
            data=buf2,
            file_name="imagen_2.png",
            mime="image/png"
        )

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
