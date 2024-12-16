import streamlit as st
from googletrans import Translator, LANGUAGES
import speech_recognition as sr

# Inicializar tradutor e reconhecimento de fala
translator = Translator()
recognizer = sr.Recognizer()

# Lista de idiomas suportados
languages = {name.title(): code for code, name in LANGUAGES.items()}

# Função para traduzir texto
def traduzir_texto(texto, origem, destino):
    try:
        traducao = translator.translate(texto, src=origem, dest=destino)
        return traducao.text
    except Exception as e:
        return f"Erro na tradução: {e}"

# Função para transcrever áudio
def transcrever_audio(audio_file, idioma):
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        texto = recognizer.recognize_google(audio_data, language=idioma)
        return texto
    except Exception as e:
        return f"Erro na transcrição: {e}"

# Função principal
def main():
    st.title("Tradutor Multilíngue com IA e Áudio")
    
    # Entrada de texto para tradução
    st.header("Tradução de Texto")
    texto_original = st.text_area("Digite o texto para traduzir:")
    idioma_origem = st.selectbox("Idioma Original", list(languages.keys()))
    idioma_destino = st.selectbox("Idioma de Destino", list(languages.keys()))
    
    if st.button("Traduzir Texto"):
        if texto_original.strip():
            traducao = traduzir_texto(
                texto_original,
                origem=languages[idioma_origem],
                destino=languages[idioma_destino],
            )
            st.write("### Tradução:")
            st.write(traducao)
        else:
            st.error("Por favor, insira um texto para traduzir.")
    
    # Entrada de áudio para transcrição e tradução
    st.header("Transcrição e Tradução de Áudio")
    audio_file = st.file_uploader("Envie um arquivo de áudio (formato WAV):", type=["wav"])
    idioma_audio = st.selectbox("Idioma do Áudio", list(languages.keys()))
    
    if audio_file and st.button("Transcrever Áudio"):
        transcricao = transcrever_audio(audio_file, languages[idioma_audio])
        st.write("### Transcrição:")
        st.write(transcricao)
        
        if transcricao and st.button("Traduzir Transcrição"):
            traducao_audio = traduzir_texto(
                transcricao,
                origem=languages[idioma_audio],
                destino=languages[idioma_destino],
            )
            st.write("### Tradução do Áudio:")
            st.write(traducao_audio)

if __name__ == "__main__":
    main()
