#Imports
import streamlit as st
from models.dataBase import SupabaseClient
from datetime import datetime, timedelta
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,headerLogin,lerJsonGif,mostrarGif

#variaveis
data_minima = datetime(1900, 1, 1)
data_maxima = datetime.now()

def main():

    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    
    with st.form(key="include"):
        input_name = st.text_input(label="Insira o seu nome completo do colaborador")
        input_email = st.text_input(label="Insira o seu nome no Smart Omini")
        input_email = st.text_input(label="Insira o CPF do colaborador -> (Apenas números)")
        input_cargo = st.selectbox("Insira o cargo do colaborador",['selecione','Auxiliar COP','Analista COP'])
        data_nascimento = st.date_input("Insira a data de nascimento do colaborador", min_value=data_minima, max_value=data_maxima)
        confirmar_senha = st.text_input(label="Número de telefone pessoal")
        input_button = st.form_submit_button("Cadastrar")

if __name__ == '__main__':
    main()