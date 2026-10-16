import streamlit as st
import os
import base64

# Configuración de la página (DEBE ir siempre primero)
st.set_page_config(page_title="Playlist - Cumple Hilda", page_icon="🎵", layout="centered")

# --- FUNCIÓN PARA EL FONDO ---
def agregar_fondo(imagen_path):
    # Verificamos si la imagen existe antes de intentar cargarla
    if os.path.exists(imagen_path):
        with open(imagen_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Inyectamos CSS personalizado
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Le damos un fondo semitransparente oscuro al contenedor principal para que el texto sea legible */
            .block-container {{
                background-color: rgba(0, 0, 0, 0.75);
                padding: 2rem 3rem;
                border-radius: 15px;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }}
            
            /* Aseguramos que los textos destaquen en color claro */
            h1, h2, h3, p {{
                color: #FFFFFF !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Llamamos a la función con el nombre de tu imagen
agregar_fondo("fondo.jpg")

# --- INTERFAZ PRINCIPAL ---
st.title("🎵 Reproductor - Cumple 70 de Hilda")
st.markdown("Seleccioná un tema de la lista para cargarlo en el reproductor principal.")
st.divider()

CARPETA_AUDIOS = "cdcumplehilda"

if not os.path.exists(CARPETA_AUDIOS):
    st.error(f"⚠️ No se encontró la carpeta '{CARPETA_AUDIOS}'.")
else:
    archivos_mp3 = [f for f in os.listdir(CARPETA_AUDIOS) if f.endswith(".mp3")]
    archivos_mp3.sort()

    if not archivos_mp3:
        st.info("No se encontraron archivos MP3 en la carpeta.")
    else:
        # 1. Inicializamos el estado para saber qué pista está sonando
        if "pista_actual" not in st.session_state:
            st.session_state.pista_actual = archivos_mp3[0]

        # --- REPRODUCTOR PRINCIPAL ---
        st.subheader("🎧 Reproduciendo ahora:")
        
        titulo_actual = st.session_state.pista_actual.replace(".mp3", "").replace("_", " ").title()
        st.markdown(f"**{titulo_actual}**")
        
        ruta_actual = os.path.join(CARPETA_AUDIOS, st.session_state.pista_actual)
        st.audio(ruta_actual, format="audio/mp3", autoplay=True)
        
        st.divider()

        # --- PLAYLIST Y DESCARGAS ---
        st.subheader("💽 Lista de Temas")
        
        def cambiar_tema(nuevo_tema):
            st.session_state.pista_actual = nuevo_tema

        for archivo in archivos_mp3:
            titulo = archivo.replace(".mp3", "").replace("_", " ").title()
            
            col_play, col_dl = st.columns([3, 1])
            
            with col_play:
                if st.session_state.pista_actual == archivo:
                    st.button(f"🔊 {titulo} (Sonando)", key=f"play_{archivo}", disabled=True, use_container_width=True)
                else:
                    st.button(
                        f"▶️ {titulo}", 
                        key=f"play_{archivo}", 
                        on_click=cambiar_tema, 
                        args=(archivo,), 
                        use_container_width=True
                    )
                    
            with col_dl:
                ruta_archivo = os.path.join(CARPETA_AUDIOS, archivo)
                with open(ruta_archivo, "rb") as file:
                    st.download_button(
                        label="⬇️ Descargar",
                        data=file,
                        file_name=archivo,
                        mime="audio/mpeg",
                        key=f"dl_{archivo}",
                        use_container_width=True
                    )