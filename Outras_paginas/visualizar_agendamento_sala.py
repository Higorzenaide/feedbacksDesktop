import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.dataBase import SupabaseClient



def main():
    instanciarSupaBase = SupabaseClient()
    imagem_url = "images/visureuniao.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    
    event_date = st.date_input("Selecione a data do agendamento:")
    data_atual = event_date
    data_formatada = data_atual.strftime("%Y-%m-%d")
    instanciarSupaBase.visualizarAgendamentos(data_formatada)

if __name__ == '__main__':
    main()