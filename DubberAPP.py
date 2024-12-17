import streamlit as st
import whisper
import librosa
import soundfile as sf
from gtts import gTTS

# Função para transcrever áudio usando Whisper
def transcribe_audio_whisper(audio_path, input_language=None):
    try:
        model = whisper.load_model("base")  # Use "base", "small", "medium", "large" dependendo dos recursos
        options = {"language": input_language} if input_language else {}
        result = model.transcribe(audio_path, **options)
        return result["text"]
    except Exception as e:
        return f"Erro na transcrição: {e}"

# Função para salvar áudio em formato de fala (usando gTTS)
def save_audio(text, language, filename="output.mp3"):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(filename)
        return filename
    except Exception as e:
        return f"Erro ao gerar áudio: {e}"

# Função para converter qualquer áudio para WAV usando Librosa
def convert_to_wav(input_path, output_path="converted_audio.wav"):
    try:
        data, samplerate = librosa.load(input_path, sr=None)  # sr=None mantém a taxa original
        sf.write(output_path, data, samplerate)
        return output_path
    except Exception as e:
        return f"Erro ao converter áudio: {e}"

# Configurações do Streamlit
st.title("Dublador de Áudio com Whisper")
st.write("Envie um arquivo de áudio ou digite texto para gerar um áudio dublado!")

tab1, tab2 = st.tabs(["Texto", "Áudio"])

# Texto para fala
with tab1:
    st.header("Texto para Fala")
    text_input = st.text_area("Digite o texto que deseja converter em áudio", "")
    language_text = st.selectbox(
        "Escolha o idioma para o áudio (código ISO 639-1)",
        ["en", "pt", "es", "fr", "de", "it"]
    )
    if st.button("Gerar Áudio do Texto"):
        if not text_input.strip():
            st.error("Por favor, insira algum texto.")
        else:
            audio_file = save_audio(text_input, language_text)
            if audio_file.endswith(".mp3"):
                st.audio(audio_file, format="audio/mp3")
                st.success("Áudio gerado com sucesso!")
            else:
                st.error(audio_file)

# Áudio para fala
with tab2:
    st.header("Áudio para Fala")
    uploaded_file = st.file_uploader("Envie um arquivo de áudio (.mp3, .wav)", type=["mp3", "wav"])
    
    # Opção de idioma de entrada
    input_language = st.selectbox(
        "Selecione o idioma do áudio de entrada",
        ["Auto", "en", "pt", "es", "fr", "de", "it"],
        index=0
    )
    input_language = None if input_language == "Auto" else input_language
    
    # Opção de idioma de saída
    language_audio = st.selectbox(
        "Selecione o idioma para a dublagem (saída)",
        ["en", "pt", "es", "fr", "de", "it"]
    )
    
    if uploaded_file and st.button("Gerar Áudio do Arquivo"):
        try:
            # Salvar o arquivo enviado
            audio_path = f"uploaded_{uploaded_file.name}"
            with open(audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Converter para WAV se necessário
            if not audio_path.endswith(".wav"):
                audio_path = convert_to_wav(audio_path)

            # Transcrever áudio com Whisper
            st.info("Transcrevendo o áudio com Whisper...")
            transcribed_text = transcribe_audio_whisper(audio_path, input_language)
            st.write(f"Transcrição: {transcribed_text}")

            # Gerar dublagem
            st.info("Gerando a dublagem...")
            dubbed_audio_file = save_audio(transcribed_text, language_audio)
            if dubbed_audio_file.endswith(".mp3"):
                st.audio(dubbed_audio_file, format="audio/mp3")
                st.success("Áudio dublado gerado com sucesso!")
            else:
                st.error(dubbed_audio_file)

        except Exception as e:
            st.error(f"Erro ao processar o áudio: {e}")
