import streamlit as st
import cv2
import numpy as np
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Image Translator AI - Demo", page_icon="🌍")

st.title("🌍 Image-to-Image Translator AI")
st.markdown("""
    This is a professional demo for the **Localization Engine v1.0**.
    It uses **EasyOCR** for text detection and **Google Translate** for localization.
""")

# Inicializar el motor OCR (Caché para evitar recargas lentas)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'es'], gpu=False)

reader = load_ocr()

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("Configuration")
target_lang = st.sidebar.selectbox("Target Language", ["es", "en", "fr", "it", "de"], index=0)
cleaning_mode = st.sidebar.checkbox("Enable B/W Logic (Noise Reduction)", value=True)

# --- CARGA DE IMAGEN ---
uploaded_file = st.file_uploader("Choose an image (Manga, Label, Document)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convertir archivo a imagen de OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    orig_image = image.copy()
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, channels="BGR")

    # --- PROCESAMIENTO ---
    with st.spinner("Analyzing image and translating..."):
        # 1. OCR Detection
        results = reader.readtext(image)
        
        # 2. Lógica de traducción y "quemado" en imagen
        for (bbox, text, prob) in results:
            if prob > 0.4:  # Filtro de confianza
                # Traducir texto
                translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
                
                # Obtener coordenadas para el dibujo
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                
                # Limpieza (Borrador blanco sobre el texto original)
                cv2.rectangle(image, top_left, bottom_right, (255, 255, 255), -1)
                
                # Inserción de texto traducido (Simplicado para Demo)
                cv2.putText(image, translated, (top_left[0], top_left[1] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    with col2:
        st.subheader("Translated Result")
        st.image(image, channels="BGR")
        
    # --- RESULTADOS DETALLADOS ---
    st.divider()
    st.subheader("📊 Extraction Data (IT/OT Insights)")
    for (_, text, _) in results:
        st.write(f"**Detected:** {text}")