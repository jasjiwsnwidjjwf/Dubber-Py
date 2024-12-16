import streamlit as st
import speech_recognition as sr

# Função para gravar áudio
def gravar_audio(tempo=5, fs=16000):
    st.info("Gravando...")
    grava = sd.rec(int(tempo * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    # Salvar o áudio em formato WAV
    with io.BytesIO() as audio_file:
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(grava.tobytes())
        audio_file.seek(0)
        return audio_file

# Função para transcrever o áudio
def transcrever_audio(arquivo_audio, idioma):
    # Usando o reconhecedor de fala
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(arquivo_audio) as source:
        audio = recognizer.record(source)
        texto = recognizer.recognize_google(audio, language=idioma)
        return texto

# Função principal do Streamlit
def app():
    st.title("Transcrição de Áudio para Texto")

    st.write("""
        Gravação de áudio ou upload para transcrição em texto.
        Suporte para múltiplos idiomas.
    """)

    # Seletor de idioma
    idioma = st.selectbox("Escolha o Idioma do Áudio", ["en", "pt", "es", "fr", "de", "it"])

    # Escolha entre gravar ou fazer upload
    gravar = st.radio("Escolha uma opção", ("Gravar", "Carregar Arquivo"))

    if gravar == "Gravar":
        tempo = st.slider("Duração da Gravação (segundos)", 1, 10, 5)
        if st.button("Iniciar Gravação"):
            arquivo_audio = gravar_audio(tempo=tempo)
            st.audio(arquivo_audio, format='audio/wav')
            
            if st.button("Transcrever Áudio"):
                texto = transcrever_audio(arquivo_audio, idioma)
                st.write(texto)

    if gravar == "Carregar Arquivo":
        arquivo_audio = st.file_uploader("Carregar Arquivo de Áudio", type=["mp3", "wav"])
        if arquivo_audio:
            st.audio(arquivo_audio, format='audio/wav')
            if st.button("Transcrever Áudio"):
                texto = transcrever_audio(arquivo_audio, idioma)
                st.write(texto)

if __name__ == "__main__":
    app()
