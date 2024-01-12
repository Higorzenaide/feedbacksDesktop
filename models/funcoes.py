import streamlit as st
from PIL import Image
import string
import os

def definirVariaveisDaSessao():
        #Variaveis em cookie
    if 'treinamentos' not in st.session_state:
        st.session_state.treinamentos = False
    if 'logado' not in st.session_state:
        st.session_state.logado = False
    if 'verificado' not in st.session_state:
        st.session_state.verificado = False
    if 'id' not in st.session_state:
        st.session_state.id = None
    if 'loginValidado' not in st.session_state:
        st.session_state.loginValidado = False
    if 'nomeLogado' not in st.session_state:
        st.session_state.nomeLogado = False
    if 'supervisao' not in st.session_state:
        st.session_state.supervisao = False


def configuracoesIniciais():
    #Configurações da pagina
    st.set_page_config(
        page_title="Gestão COP",
        page_icon="🚀",
        layout="centered",  # Ou "centered" se preferir centralizar o conteúdo
        initial_sidebar_state="expanded",  # Ou "collapsed" para a barra lateral recolhida
    )

def imagemSideBar():
     # Caminho relativo ao diretório de trabalho do aplicativo Streamlit
    imagem_path = "feedbacksDesktop/images/logo3.jpeg"

    # Obtendo o diretório de trabalho atual
    diretorio_trabalho = os.getcwd()

    # Construindo o caminho completo para a imagem
    caminho_completo = os.path.join(diretorio_trabalho, imagem_path)

    if os.path.exists(caminho_completo):
        imagem = Image.open(caminho_completo)
        st.sidebar.image(imagem, use_column_width=True)
        st.sidebar.subheader("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GESTÃO COP")
    else:
        st.sidebar.error(f"Arquivo de imagem não encontrado: {caminho_completo}")


def senha_valida(senha):
    caracteres_especiais = string.punctuation  # Obtem todos os caracteres especiais

    # Verifica se pelo menos um caractere especial está presente na senha
    if any(char in caracteres_especiais for char in senha):
        if len(senha) >= 6:
            return True
    else:
        return False
