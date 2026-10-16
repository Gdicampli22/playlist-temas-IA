import streamlit as st
import os
import base64

# Configuración de la página
st.set_page_config(page_title="Playlist - Cumple Hilda", page_icon="🎵", layout="centered")

# --- FUNCIÓN PARA EL FONDO Y ESTILOS ---
def agregar_fondo(imagen_path):
    if os.path.exists(imagen_path):
        with open(imagen_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            .block-container {{
                background-color: rgba(0, 0, 0, 0.80);
                padding: 2rem 3rem;
                border-radius: 15px;
                margin-top: 2rem;
                margin-bottom: 2rem;
            }}
            
            h1, h2, h3, p {{
                color: #FFFFFF !important;
            }}
            
            /* Fondo oscuro y borde dorado para los botones */
            div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button {{
                background-color: #222222 !important; 
                border: 1px solid #FFD700 !important; 
            }}
            
            div[data-testid="stButton"] > button p, div[data-testid="stDownloadButton"] > button p,
            div[data-testid="stButton"] > button div, div[data-testid="stDownloadButton"] > button div {{
                color: #FFFFFF !important;
            }}

            div[data-testid="stButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover {{
                background-color: #FFD700 !important;
                border: 1px solid #FFD700 !important;
            }}
            
            div[data-testid="stButton"] > button:hover p, div[data-testid="stDownloadButton"] > button:hover p,
            div[data-testid="stButton"] > button:hover div, div[data-testid="stDownloadButton"] > button:hover div {{
                color: #000000 !important; 
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

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
        if "pista_actual" not in st.session_state:
            st.session_state.pista_actual = archivos_mp3[0]

        # --- FUNCIONES DE CONTROL ---
        def cambiar_tema_lista(nuevo_tema):
            st.session_state.pista_actual = nuevo_tema

        def cambiar_tema_idx(incremento):
            # Buscamos en qué posición está el tema actual
            idx_actual = archivos_mp3.index(st.session_state.pista_actual)
            # Calculamos el nuevo índice (el módulo % hace que si llega al final, vuelva al principio)
            nuevo_idx = (idx_actual + incremento) % len(archivos_mp3)
            st.session_state.pista_actual = archivos_mp3[nuevo_idx]

        # --- REPRODUCTOR PRINCIPAL ---
        st.subheader("🎧 Reproduciendo ahora:")
        
        titulo_actual = st.session_state.pista_actual.replace(".mp3", "").replace("_", " ").title()
        st.markdown(f"**{titulo_actual}**")
        
        ruta_actual = os.path.join(CARPETA_AUDIOS, st.session_state.pista_actual)
        st.audio(ruta_actual, format="audio/mp3", autoplay=True)
        
        # --- BOTONES ANTERIOR / SIGUIENTE ---
        col_prev, col_next = st.columns(2)
        with col_prev:
            st.button("⏮️ Tema Anterior", on_click=cambiar_tema_idx, args=(-1,), use_container_width=True)
        with col_next:
            st.button("⏭️ Tema Siguiente", on_click=cambiar_tema_idx, args=(1,), use_container_width=True)
        
        st.divider()

        # --- PLAYLIST Y DESCARGAS ---
        st.subheader("💽 Lista de Temas")

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
                        on_click=cambiar_tema_lista, 
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