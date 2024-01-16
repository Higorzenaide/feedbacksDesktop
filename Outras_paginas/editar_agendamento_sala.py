import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.dataBase import SupabaseClient
from models.funcoes import efetuarLogin

def main():
    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    instanciarSupa = SupabaseClient()
    if st.session_state.logado == False:
            efetuarLogin()
            return
    instanciarSupa.editarAgendamento(st.session_state.id)

if __name__ == '__main__':
    main()