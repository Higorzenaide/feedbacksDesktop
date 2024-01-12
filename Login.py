#Imports
import streamlit as st
from dotenv import load_dotenv
from models.dataBase import SupabaseClient
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao
from PIL import Image


#sessão principal
def main():
    #Definindo as variaveis em cookies
    definirVariaveisDaSessao()

    #Instanciando o Banco de dados
    supabase_instance = SupabaseClient()

    #Chamando a função de configurações iniciais
    configuracoesIniciais()

    #Imagem e titulo SideBart
    imagemSideBar()

    #Adicionando seja bem-vindo e espaçamentos para alinhar
    st.header('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
              '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Seja bem-vindo')
    st.sidebar.write("&nbsp;")

    #Formulário
    with st.form(key="include_senha"):
        input_email = st.text_input(label="Insira o seu E-mail")
        input_pass = st.text_input(label="Insira a sua senha", type="password")
        input_button = st.form_submit_button("Logar")

    #Botão clicado chama a função que valida o login
    if input_button:
        supabase_instance.login(input_email,input_pass)
    
if __name__ == '__main__':
    main()