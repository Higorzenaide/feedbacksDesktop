import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import Calculasessao
from models.dataBase import SupabaseClient
from datetime import datetime


def main():

    #Instanciar SupaBase
    instanciarSupaBase = SupabaseClient()

    #Exibe imagem Hearder
    imagem_url = "images/visureuniao.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    st.write("O site da sala de reunião foi migrado para o site 'https://gestao-cop.vercel.app/sala_reuniao'")
    return
    #Selecionar a data que deseja visualizar
    event_date = st.date_input("Selecione a data do agendamento:")

    #Formatando a data
    data_atual = event_date
    data_formatada = data_atual.strftime("%Y-%m-%d")

    #Chama a função para visualizar os agendamentos
    instanciarSupaBase.visualizarAgendamentos(data_formatada)
    
    #Se o usuário estiver logado informao tempo de sessão
    if st.session_state.logado == True:
        if 'last_active_time' in st.session_state:
            elapsed_time = datetime.now() - st.session_state.last_active_time
            elapsed_minutes = elapsed_time.total_seconds() / 60  # Convert seconds to minutes
            formatted_time = "{:.2f}".format(elapsed_minutes)
            st.sidebar.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
            st.sidebar.markdown(f'<span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tempo de sessão: {formatted_time.split(".")[0]} minutos</span>', unsafe_allow_html=True)
    else:
        pass

if __name__ == '__main__':
    main()
