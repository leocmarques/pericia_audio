import streamlit as st
import openai
from pydub import AudioSegment
import tempfile
import os

# Função para processar o áudio e dividi-lo em partes de 15 minutos
def dividir_audio_em_partes(caminho_audio):
    audio = AudioSegment.from_file(caminho_audio)
    partes = []
    for i in range(0, len(audio), 900000):  # 900000 ms = 15 minutos
        parte = audio[i:i + 900000]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            parte.export(temp_audio_file.name, format="mp3")
            partes.append(temp_audio_file.name)
    return partes

# Função para transcrever o áudio
def transcrever_audio(api_key, partes):
    openai.api_key = api_key
    texto_transcrito = ""
    for parte in partes:
        with open(parte, 'rb') as audio_file:
            response = openai.Audio.transcribe("whisper-1", audio_file)
            texto_transcrito += response['text'] + " "
        os.remove(parte)  # Remove o arquivo temporário após a transcrição
    return texto_transcrito

# Função para criar um resumo do texto transcrito
def criar_resumo(api_key, texto_transcrito):
    openai.api_key = api_key
    prompt = f"Resuma o seguinte texto de forma clara e objetiva:\n\n{texto_transcrito}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    resumo = response['choices'][0]['message']['content']
    return resumo

def main():
    st.title("Transcrição e Resumo de Áudio - Relato da Pericianda")

    # Inputs para nome, número de pessoas e assistentes
    nome = st.text_input("Nome da Pericianda", placeholder="Digite o nome")
    pessoas = st.number_input("Número de Pessoas", min_value=1, max_value=10, value=2)
    assistentes = st.number_input("Número de Assistentes Técnicos", min_value=0, max_value=10, value=0)

    # Input para a chave da API da OpenAI
    api_key = st.text_input("Chave da API da OpenAI", type="password")

    # Upload do arquivo de áudio
    uploaded_file = st.file_uploader("Envie o arquivo de áudio", type=["mp3", "wav", "m4a", "flac"])

    if st.button("Processar Áudio e Criar Resumo"):
        if api_key and uploaded_file and nome:
            with st.spinner("Processando o áudio e realizando a transcrição..."):
                try:
                    # Salva o arquivo de áudio temporariamente
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                        temp_audio_file.write(uploaded_file.read())
                        caminho_audio = temp_audio_file.name

                    # Divide o áudio em partes de 15 minutos
                    partes_audio = dividir_audio_em_partes(caminho_audio)

                    # Transcreve o áudio
                    texto_transcrito = transcrever_audio(api_key, partes_audio)

                    # Cria um resumo do texto transcrito
                    resumo = criar_resumo(api_key, texto_transcrito)

                    st.success("Transcrição e resumo concluídos!")
                    st.subheader("Texto Transcrito")
                    st.text_area("Resultado", texto_transcrito, height=300)

                    st.subheader("Resumo do Texto")
                    st.text_area("Resumo", resumo, height=200)

                    os.remove(caminho_audio)  # Remove o arquivo de áudio temporário

                except openai.error.OpenAIError as e:
                    st.error(f"Erro na transcrição ou resumo: {e}")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")
        else:
            st.warning("Por favor, insira todos os dados necessários para iniciar o processamento.")

if __name__ == "__main__":
    main()
