#Imports
import streamlit as st
from dotenv import load_dotenv
from models.dataBase import SupabaseClient
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,headerLogin,lerJsonGif,mostrarGif,loginefetuado
from PIL import Image
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from Outras_paginas.Cadastro import main as mainCadastro
#sessão principal
def main():
    
    #Definindo as variaveis em cookies
    definirVariaveisDaSessao()
    if st.session_state.logado:
        loginefetuado()
        return
    
    # 2. horizontal menu
    selected2 = option_menu(None, ["Login", "Cadastro"], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal")
    
    if selected2 == 'Cadastro':
        mainCadastro()
        return
    
    #Instanciando o Banco de dados
    supabase_instance = SupabaseClient()

    #Chamando a função de configurações iniciais
    # configuracoesIniciais()

    #Imagem e titulo SideBart
    imagemSideBar()

    #Botão de logout
    logout()

    #Header de login
    headerLogin()

    col1, col2 = st.columns(2)
    #Formulário
    with col1:
    # Formulário
        with st.form("login", clear_on_submit=True):
            input_email = st.text_input(label="Insira o seu E-mail")
            input_pass = st.text_input(label="Insira a sua senha", type="password")
            input_button = st.form_submit_button("Logar")

    #Passando onde está o GIF
    lottie_codding = lerJsonGif("gifs/Animacao01.json")
    #Mostrando Gif
    with col2:
        mostrarGif(lottie_codding)

    #Botão clicado chama a função que valida o login
    if input_button:
        supabase_instance.login(input_email,input_pass)
        st.session_state['input_email'] = ''
        st.session_state['input_pass'] = ''


if __name__ == '__main__':
    main()