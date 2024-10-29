import streamlit as st
import openai
from pydub import AudioSegment
import tempfile
import os

os.system("apt-get update && apt-get install -y ffmpeg")

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

# Função para criar um resumo baseado no estilo solicitado
def criar_resumo(api_key, transcricao_final, nome, pessoas, assistentes):
    openai.api_key = api_key
    
    instrucao = f"""
    Considere e aprenda minha escrita de um relato da pericianda a partir do exemplo abaixo. logo mais terei uma demanda para você:

    Relato da Pericianda

    No ato pericial, Aline relata que estava gestante de 39 semanas, com cesárea programada para ocorrer em 03/11/2022 por desejo materno, a ser realizada pelo Dr Fábio Eduardo
    Benatti. Estava em trabalho de parto em 31/10/2022 e por esse motivo o procedimento foi antecipado e realizado neste dia pelo referido médico.
    Antes da gestação, relata que apresentava ansiedade e obesidade. Durante a gravidez, além de tratamento para ansiedade com medicação (Sertralina 50 mg,1x ao dia), apresentou
    também diagnóstico de hipertensão gestacional, no último trimestre.
    A pericianda relata que não houve intercorrências durante a internação e o parto e que não observou falhas no atendimento até então. Sua filha nasceu bem e permaneceu aos
seus cuidados no pós-parto.
Após o procedimento, a pericianda ficou aos cuidados dos  médicos plantonistas do hospital, que a examinaram nos dois dias após o parto. Ela relata que apresentou dores
abdominais, tendo comunicado a enfermagem e a equipe médica, que a examinaram e por não haverem outros achados além da dor, suspeitaram que esta seria esperada devido ao
procedimento cirúrgico, que ainda era recente.
Foram prescritas medicações para dor, que não chegavam a aliviar completamente as queixas álgicas. Nega quaisquer outros sintomas, tais como: aumento de sangramento vaginal,
 febre, náuseas e vômitos, vermelhidão ou secreção purulenta em ferida operatória.
Em 02/11/2022, 2 dias após o parto, a Dra Gabriela Sarmiento M Amaral (CRM 153607) realizou exame físico completo, diante das queixas de dor abdominal. Não foram observadas
alterações na ferida operatória ou no exame ginecológico. No entanto, ao realizar o exame abdominal direcionado, constatou que o abdome apresentava um pouco de distensão,
compatível com a presença de gases. A pericianda relata que foi bem avaliada e examinada por esta profissional. Diante da ausência de outros sintomas e dos achados no
exame físico, foi então de alta com medicação para dor e para gases e orientada a andar para aliviar esse desconforto.
Após a alta, relata que o desconforto abdominal piorou ao longo dos dias subsequentes, além disso, se sentia mais edemaciada e refere que passou a apresentar saída de secreção
amarelada e sem odor, através da ferida operatória. Notava ainda vermelhidão em bordos de ferida operatória. Esses sintomas dificultavam até mesmo a amamentação. Neste momento,
diante da dor abdominal e desses novos achados, retornou ao hospital 6 dias após a alta para nova avaliação.
Naquele dia, 08/11/2022, o Dr. Fábio, que realizou a cesariana, estava de plantão e atendeu a pericianda no pronto-socorro. Ela relata que ele a avaliou e, diante dos sinais e
sintomas que a mesma apresentava, passou a suspeitar de infecção de ferida operatória e a internou para investigação dos sintomas e prescrição de antibioticoterapia endovenosa.
Ela não relata falha no atendimento neste momento.
No dia 09/11/2022, iniciou quadro de náuseas e vômitos, que a preocuparam mais. Nesse momento, já estava realizando tratamento com antibiótico, porém a dor abdominal persistia.
Durante a internação, a paciente aguardava para realizar uma tomografia de abdome, que havia sido pedida na admissão como parte dos exames de investigação. No entanto, foi
informada pela equipe de enfermagem que a solicitação desse exame não foi encontrada. Sendo assim, a realizou no dia seguinte, 10/11/2022.
Neste dia, por volta das 18 horas, iniciou quadro de sangramento vaginal intenso, foi acolhida pela equipe de enfermagem que comunicou as médicas de plantão. As mesmas
avaliaram a paciente e informaram que diante dos achados no exame físico, a mesma precisaria ser encaminhada para um procedimento de retirada do útero (histerectomia),
pois sua vida estaria em risco.
O procedimento de Histerectomia aconteceu na mesma noite, pelas médicas plantonistas, Dra Laiz e Dra Isabela, com a necessidade de anestesia geral e transfusão de bolsas
de sangue, devido a intensa perda de sangue. Diante da gravidade do quadro, a pericianda foi encaminhada para a Unidade de Terapia Intensiva no pós operatório, onde permaneceu
por cerca de 7 dias. Relata ter sido bem tratada pela equipe da UTI, médicos e enfermagem.
Após a estabilização do quadro, melhora clínica e laboratorial, ela foi de alta hospitalar e não apresentou novas intercorrências clínicas ou cirúrgicas relacionadas aos
procedimentos cirúrgicos.
Ela se queixou do aspecto estético da cicatriz cirúrgica resultante dos procedimentos realizados.
Passados alguns meses dos acontecimentos, ela relata que tentou obter o prontuário médico, para buscar respostas e esclarecimentos. No entanto, por dificuldades administrativas,
o mesmo foi disponibilizado apenas após o início da ação judicial.
Atualmente, a pericianda não utiliza medicações e mantém controle da ansiedade com terapia mensal. Relata sofrer com a impossibilidade de gestar novamente. Trabalha como
assistente financeira e relata exercer plenamente suas atividades do cotidiano e laborais.


Agora, temos a transcrição abaixo da gravação da perícia realizada com outra pericianda chamada {nome}. estavam presentes {pessoas}
pessoas, sendo a pericianda, a perita Arlete e {assistentes} assistentes técnicos. A imensa maioria das falas é da pericianda, e em
geral as perguntas são da perita. leia o documento e tente fazer um relato da pericianda o mais proximo possivel do modelo apresentado
inicialmente. Quando falo próximo, me refiro ao estilo de escrita, nao especificamente ao conteudo em si. o resumo deve ter pelo menos 7 paragrafos.

    Transcrição:
    {transcricao_final}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instrucao}
        ]
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
                    resumo = criar_resumo(api_key, texto_transcrito, nome, pessoas, assistentes)

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
