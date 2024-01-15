import streamlit as st
from PIL import Image
import string
import os
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

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
    if 'cadastroEfetuado' not in st.session_state:
        st.session_state.cadastroEfetuado = False


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
    imagem_path = "images/logo4.png"

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

def logout():
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("estilos/styles.css")

    with st.sidebar:
        st.button("logout")

def headerLogin():
    imagem_url = "images/login.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

def logado():
    imagem_url = "images/logado.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

def loginefetuado():
    imagem_url = "images/loginefetuado.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

def cadastroEfetuado():
    imagem_url = "images/cadastroEfetuado.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

def efetuarLogin():
    imagem_url = "images/efetuarlogin.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

def lerJsonGif(filepath: str):
        with open(filepath, "r") as f:
         return json.load(f)

def mostrarGif(parametro):
    st_lottie(parametro,width=400,
    height=None,
    speed=1,)

def menuHorizontal():
    selected2 = option_menu(None, ["Login", "Cadastro"], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    return selected2

def menuHorizontalSupervisorCOP():
    selected2 = option_menu(None, ["Cadastrar colaborador", "Inserir feedbacks","Visualizar feedbacks","Registrar presença","Inserir advertencia","Inserir escala"], 
        icons=['person', 'graph-up-arrow', "list-task", 'inbox-fill','hand-thumbs-down-fill','calendar2-week'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    return selected2