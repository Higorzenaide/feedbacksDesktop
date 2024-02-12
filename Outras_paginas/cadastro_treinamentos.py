#Imports
import streamlit as st
from models.dataBase import SupabaseClient
from datetime import datetime, timedelta
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,efetuarLogin,logout,headerLogin,lerJsonGif,mostrarGif



def CadastroTreinamentosColaborador():
    # Variáveis
    data_minima = datetime(1900, 1, 1)
    data_maxima = datetime.now()
    #Se a variavel logado for igual a False, exibe que precisa estar logado
    if st.session_state.logado == False:
        if st.session_state.sessao:
            if st.session_state.rerun == False:
                st.session_state.rerun = True
                pass
            else:
                return
        else:
            return
        
    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

    with st.form(key="include"):
        input_nome = st.text_input(label="Insira o nome completo do colaborador")
        input_smart_omni = st.text_input(label="Insira o nome no Smart Omini")
        input_cpf = st.text_input(label="Insira o CPF do colaborador -> (Apenas números)")
        input_cargo = st.selectbox("Insira o cargo do colaborador", ['selecione', 'Auxiliar COP', 'Analista COP'])
        data_nascimento = st.date_input("Insira a data de nascimento do colaborador", min_value=data_minima, max_value=data_maxima)
        numero_telefone = st.text_input(label="Número de telefone pessoal")
        supervisor = st.selectbox(label="Insira o nome do supervisor")
    
        input_button = st.form_submit_button("Cadastrar")

if __name__ == '__main__':
    CadastroTreinamentosColaborador()