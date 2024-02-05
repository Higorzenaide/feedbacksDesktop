import time
from datetime import datetime
from models.api import IniciarAPI as api
import streamlit as st

def editarTicketSmart():
    dados = st.session_state.dados2
    num_ticket = dados["N° ticket"]
    id_ticket = dados["id"]
    gestor = dados["gestor"]
    with st.form("editar_ticket"):
        st.write(f'Atualize as informações do ticket: {num_ticket} // Inserido por: {gestor}')
        tratado = st.selectbox(f'O ticket foi tratado?',["Sim"])
        hora_fim = st.text_input(f'Atualize o horário de fim. UTILIZE O PADRÃO ABAIXO: ',value="00:00:00")
    
        input_button = st.form_submit_button("Confirmar")
    
    if input_button:
        tratado = True
        hora_fim = datetime.strptime(hora_fim, "%H:%M:%S").time()
        hora_fim_str = hora_fim.strftime("%H:%M:%S")
        dados = {
            "hora_fim":hora_fim_str,"normalizado":tratado,"id":id_ticket
        }
        instanciarAPI = api('EditarTicketSmart')
        retorno = instanciarAPI.editarTicketSmart(dados)
        st.sucess("Dados Editados com sucesso")
        st.session_state.editarTicketSmart = False
        time.sleep(3)
        st.rerun()
if __name__ == '__main__':
    editarTicketSmart()