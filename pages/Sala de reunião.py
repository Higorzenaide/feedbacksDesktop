import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,logout,definirVariaveisDaSessao,local_css,menuHorizontalSalaDeReuniao
from Outras_paginas.editar_agendamento_sala import main as mainEditarAgendamentoSala
from Outras_paginas.visualizar_agendamento_sala import main as mainVisualizarAgendamentoSala
import calendar
from models.dataBase import SupabaseClient
from datetime import datetime, time, timedelta
import json
def main():

    #Definindo as variaveis em cookies.
    definirVariaveisDaSessao()

    #Chamando a função de configurações iniciais, caso não tenha sido iniciado por outra pagina.
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()

    

   # Título da aplicação
    menu = menuHorizontalSalaDeReuniao()

    if menu == 'Realizar Agendamento':
        imagem_url = "images/REUNIAO.png"  # Substitua pela URL da sua imagem
        st.image(imagem_url, use_column_width=True)
        pass
    elif menu == 'Visualizar agendamentos':
        mainVisualizarAgendamentoSala()
        return
    elif menu == 'Editar seu Agendamento':
        mainEditarAgendamentoSala()
        return
    

    #Botão de logout. local_css é um função.
    local_css("estilos/styles.css")
    logout_button_clicked = st.sidebar.button("Logout", key="logout")

    if logout_button_clicked:
        st.session_state.logado = False
        st.experimental_rerun()

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
    st.header("Agendar Sala de Reunião")

    # Obter detalhes do evento
    event_date = st.date_input("Selecione a data do agendamento:")
    st.write("Horário de Início:")
    start_time = st.time_input("Selecione a hora de início:", time(today.hour, today.minute))
    st.write("Horário de Término:")
    end_time = st.time_input("Selecione a hora de término:", time((today.hour + 1) % 24, today.minute))
    st.write(f'Pessoa que está agendando: {st.session_state.nomeLogado}')
    pessoa = st.session_state.nomeLogado
    agendar = st.button("Agendar")
    instanciarSupaBase = SupabaseClient()

    if agendar:
        data_atual = event_date
        data_formatada = data_atual.strftime("%Y-%m-%d")
        start_time_str = start_time.strftime("%H:%M:%S")
        end_time_str = end_time.strftime("%H:%M:%S")
        
        # Criar um dicionário com os dados
        dados_agendamento = {
            "data": data_formatada,
            "hora_inicio": start_time_str,
            "hora_termino": end_time_str,
            "id_usuario": st.session_state.id,
            "Gestor":pessoa
        }

        # Serializar o dicionário para JSON
        dados_agendamento_json = json.dumps(dados_agendamento)

        # Passar o JSON para a função
        instanciarSupaBase.inserirAgendamentoSalaReuniao(dados_agendamento_json)


        

# Chamar a função principal
if __name__ == '__main__':
    main()