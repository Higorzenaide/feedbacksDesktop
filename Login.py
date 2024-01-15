
#Imports
import streamlit as st
from models.dataBase import SupabaseClient
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,headerLogin,lerJsonGif,mostrarGif,loginefetuado,menuHorizontal
from Outras_paginas.Cadastro import main as mainCadastro

#sessão principal
def main():

    #Chamando a função de configurações iniciais
    configuracoesIniciais()
    
    #Definindo as variaveis em cookies
    definirVariaveisDaSessao()

    #Se loginEfetuado mostre imagem e mais nada
    if st.session_state.logado:
        loginefetuado()
        return
    
    #Menu horizontal ['Login' ou 'Cadastro']
    menu = menuHorizontal()
    if menu == 'Cadastro':
        mainCadastro()
        return
    
    #Instanciando o Banco de dados
    supabase_instance = SupabaseClient()

    #Imagem e titulo SideBart
    imagemSideBar()

    #Botão de logout
    logout()

    #Header de login
    headerLogin()

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

    #Botão clicado chama a função que valida o login
    if input_button:
        supabase_instance.login(input_email,input_pass)
        #Reseta formulário
        st.session_state['input_email'] = ''
        st.session_state['input_pass'] = ''

if __name__ == '__main__':
    main()