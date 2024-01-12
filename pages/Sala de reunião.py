import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais
import calendar
from datetime import datetime, time, timedelta
def main():
    

   # Título da aplicação
    st.title("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Calendário de Eventos")
    st.header('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                  '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;****EM DESENVOLVIMENTO****')


    # Obter o ano e o mês atual
    today = datetime.today()
    year = st.number_input("Digite o ano:", int(today.year - 1), int(today.year + 1), today.year)
    month = st.number_input("Digite o mês:", 1, 12, today.month)

    # Criar o objeto de calendário para o mês e ano fornecidos
    cal = calendar.monthcalendar(year, month)

    # Criar o cabeçalho do calendário
    header = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

    # Iniciar o layout da tabela
    table = "<table style='width:100%'><tr>"

    # Adicionar o cabeçalho à tabela
    for day in header:
        table += f"<th>{day}</th>"
    table += "</tr>"

    # Adicionar os dias do mês à tabela
    for week in cal:
        table += "<tr>"
        for day in week:
            if day == 0:
                table += "<td></td>"
            else:
                table += f"<td>{day}</td>"
        table += "</tr>"

    # Fechar a tabela
    table += "</table>"

    # Exibir a tabela no Streamlit
    st.markdown(table, unsafe_allow_html=True)

    # Dividir em colunas
    col1, col2 = st.columns(2)

    # Agendar Sala de Reunião - Coluna 1
    with col1:
        st.header("Agendar Sala de Reunião")

        # Obter detalhes do evento
        event_date = st.date_input("Selecione a data do agendamento:")
        st.write("Horário de Início:")
        start_time = st.time_input("Selecione a hora de início:", time(today.hour, today.minute))
        st.write("Horário de Término:")
        end_time = st.time_input("Selecione a hora de término:", time((today.hour + 1) % 24, today.minute))
        st.write("Detalhes do agendamento:")
        st.write(f"Data: {event_date}")
        st.write(f"Horário de Início: {start_time.strftime('%H:%M')}")
        st.write(f"Horário de Término: {end_time.strftime('%H:%M')}")
        st.write(f"Pessoa que está agendando: ")

    # Agendar Sala de Reunião - Coluna 2
    with col2:
        st.subheader("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Datas agendadas")
        st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")


        # Exibir detalhes do evento
        

# Chamar a função principal
if __name__ == '__main__':
    main()