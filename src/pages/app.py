import sys
sys.path.append("../")
from utils.gpt_processing import get_llm_response
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
file_path = "../../data/upload"

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

def save_uploadedfile(uploadedfile):
     
     delete_files_in_directory(file_path)
     with open(os.path.join(file_path,uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Arquivo:{} salvo em".format(uploadedfile.name))

def gera_scope(model: str):
   PROMPT_TEMPLATE = """ 
    Você é um Analista de Dados que irá atuar em um projeto de business intelligence. Baseado na transcrição da reunião abaixo, monte um documento baseado na estrutura abaixo. Este documento precisa ser inteiramente baseado na {context}.
    Segue a estrutura abaixo:
    1. Introdução
    2. Participantes da Reunião
    3. Necessidades de Técnicas:
    a. Indicadores
    i. Sistemas de origem
    ii. Banco de dados do sistema de origem
    iii. Nome da tabela
    iv. Regras para calcular o indicador
    b. Modelagem
    i. Relacionamento entre as tabelas mencionadas 
    4. Itens Pendentes de Definição:
    5. Próximos Passos:
    """
   
   resposta = get_llm_response(PROMPT_TEMPLATE, file_path, 'teste_doc_escopo.docx',model=model)
   arquivo_escopo = "../../data/upload" + 'teste_doc_escopo.docx'

   return arquivo_escopo, resposta
 
uploaded_files = st.file_uploader("Escolha seus arquivos", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    save_uploadedfile(uploaded_file)

llm_model = st.radio(
    "Defina qual modelo será usado:",
    ["ChatGPT", "Google Gemini"],
    index=0,
)    

if llm_model == "ChatGPT":
   model = 'openai'
else:
   model = 'google'

st.write("Você selecionou:", llm_model)

if st.button("Gera Documento"):
  response, caminho = gera_scope(model)
  st.write(response)
  st.write("Arquivo gerado em:" + caminho)