import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import os

# Inicializar tradutor e reconhecimento de fala
translator = Translator()
recognizer = sr.Recognizer()

# Função para converter áudio para o formato WAV (se necessário)
def converter_para_wav(audio_file):
    try:
        audio = AudioSegment.from_file(audio_file)
        temp_wav = "temp_audio.wav"
        audio.export(temp_wav, format="wav")
        return temp_wav
    except Exception as e:
        return f"Erro ao converter áudio: {e}"

# Função para transcrever áudio
def transcrever_audio(audio_path, idioma):
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        texto = recognizer.recognize_google(audio_data, language=idioma)
        return texto
    except Exception as e:
        return f"Erro na transcrição: {e}"

# Função para traduzir texto
def traduzir_texto(texto, origem, destino="pt"):
    try:
        traducao = translator.translate(texto, src=origem, dest=destino)
        return traducao.text
    except Exception as e:
        return f"Erro na tradução: {e}"

# Função principal
def main():
    st.title("Transcrição e Tradução de Áudio")

    # Entrada de áudio para transcrição e tradução
    st.header("Envie um arquivo de áudio")
    audio_file = st.file_uploader("Envie um arquivo de áudio (formatos suportados: MP3, WAV, etc.):", type=["wav", "mp3", "ogg", "flac"])
    idioma_audio = st.selectbox("Idioma do Áudio", ["Português", "Inglês", "Espanhol", "Francês", "Alemão"])

    # Mapeando os idiomas para os códigos da API
    idioma_map = {
        "Português": "pt-BR",
        "Inglês": "en-US",
        "Espanhol": "es-ES",
        "Francês": "fr-FR",
        "Alemão": "de-DE"
    }

    if audio_file and st.button("Transcrever Áudio"):
        with open("uploaded_audio", "wb") as f:
            f.write(audio_file.read())

        audio_path = converter_para_wav("uploaded_audio")
        if isinstance(audio_path, str) and audio_path.startswith("Erro"):
            st.error(audio_path)
        else:
            transcricao = transcrever_audio(audio_path, idioma_map[idioma_audio])
            st.write("### Transcrição:")
            st.write(transcricao)

            if transcricao and st.button("Traduzir Transcrição"):
                traducao = traduzir_texto(transcricao, origem=idioma_map[idioma_audio].split("-")[0])
                st.write("### Tradução:")
                st.write(traducao)

            # Remover arquivo temporário
            if os.path.exists(audio_path):
                os.remove(audio_path)

if __name__ == "__main__":
    main()
