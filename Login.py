
#Imports
import streamlit as st
from models.dataBase import SupabaseClient
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,headerLogin,lerJsonGif,mostrarGif,loginefetuado,menuHorizontal,local_css,Calculasessao
from Outras_paginas.Cadastro import main as mainCadastro

#sessão principal
def main():

    #Definindo as variaveis em cookies.
    definirVariaveisDaSessao()

    #Chamando a função de configurações iniciais, caso não tenha sido iniciado por outra pagina.
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()
    
    #Se o login já foi feito, mostre imagem e mais nada.
    if st.session_state.logado:
        loginefetuado()
        return
    
    #Menu horizontal ['Login' ou 'Cadastro']
    menu = menuHorizontal()
    if menu == 'Cadastro':
        mainCadastro()
        return
    
    #Imagem e titulo da SideBart.
    imagemSideBar()

    #Header de login
    headerLogin()

    #Botão de logout. local_css é um função.
    local_css("estilos/styles.css")
    logout_button_clicked = st.sidebar.button("Logout", key="logout")

    # Se botão logout clicado.
    if logout_button_clicked:
        st.session_state.logado = False
        st.experimental_rerun()

    #Separando a page em colunas
    col1, col2 = st.columns(2)
    
    #Formulário
    with col1:
        with st.form("login", clear_on_submit=True):
            input_email = st.text_input(label="Insira o seu E-mail")
            input_pass = st.text_input(label="Insira a sua senha", type="password")
            input_button = st.form_submit_button("Logar")

    #Passando onde está o GIF
    lottie_codding = lerJsonGif("gifs/Animacao01.json")
    #Mostrando Gif
    with col2:
        mostrarGif(lottie_codding)

    #Instanciando o Banco de dados, para chamar a função.
    supabase_instance = SupabaseClient()
    #Botão clicado chama a função que valida o login
    if input_button:
        supabase_instance.login(input_email,input_pass)
        
        #Reseta formulário
        st.session_state['input_email'] = ''
        st.session_state['input_pass'] = ''

if __name__ == '__main__':
    main()