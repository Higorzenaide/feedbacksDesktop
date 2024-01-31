import time
from datetime import datetime, time, timedelta
from models.api import IniciarAPI as api
import streamlit as st

def main():
    print("entrou dentro")
    params = st.session_state.dados
    today = datetime.today()
    data_agendamento = params["data_agendamento"]
    data_agendamento_dt = datetime.strptime(data_agendamento, '%d/%m/%y')        
    hora_inicio = params["hora_inicio"]
    hora_fim = params["hora_fim"]
    id = params["id"]
    Nome = params["gestor"]
    st.header("Editar seu agendamento")

    # Data do agendamento
    event_date = st.date_input("Selecione a data do agendamento:", value=data_agendamento_dt)

    # Horário de início
    st.write("Horário de Início:")
    hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S').time()
    start_time = st.time_input("Selecione a hora de início:", value=hora_inicio_obj)

    # Horário de término
    st.write("Horário de Término:")
    hora_fim_obj = datetime.strptime(hora_fim, '%H:%M:%S').time()
    end_time = st.time_input("Selecione a hora de término:", value=hora_fim_obj)

    # Nome da pessoa que está agendando
    st.write(f'Pessoa que está editando: {st.session_state.nomeLogado}')
    pessoa = st.session_state.nomeLogado

    confirmar = st.button("Confirmar")

    if confirmar:
        instanciarapi = api('EditarAgendamento')
        event_date = event_date.strftime("%Y-%m-%d")
        start_time_str = start_time.strftime("%H:%M:%S")
        end_time_str = end_time.strftime("%H:%M:%S")
        dados = {"data_agendamento":event_date,"hora_inicio": start_time_str,"hora_fim":end_time_str,"id": id,"Gestor": 
        Nome, "id_gestor":st.session_state.id}
        print(dados)
        st.session_state.editar = False
        try:
            with st.spinner("Efetuando alteração..."):
                retorno = instanciarapi.editarAgendamentos(dados)
                st.rerun()
        except Exception as e:
            print(e)
        st.rerun()
if __name__ == '__main__':
    main()