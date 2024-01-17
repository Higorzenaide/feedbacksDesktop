import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.dataBase import SupabaseClient
from models.funcoes import efetuarLogin

def main():
    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

    #Selecionar a data que deseja visualizar
    event_date = st.date_input("Selecione a data que deseje editar o agendamento:")

    #Formatando a data
    data_atual = event_date
    data_formatada = data_atual.strftime("%Y-%m-%d")

    instanciarSupa = SupabaseClient()


    if st.session_state.logado == False:
            efetuarLogin()
            return
    instanciarSupa.editarAgendamento(st.session_state.id,data_formatada)

if __name__ == '__main__':
    main()