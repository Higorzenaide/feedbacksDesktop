import streamlit as st
from datetime import datetime, time
from models.api import IniciarAPI as api
def mainInserirTicket():
    data = st.date_input("Informe a data do ocorrido: ")
    motivo = st.selectbox("Informe o motivo: ", ["Selecione o Motivo", "Lentidão", "Demora para cair técnicos aos atendentes", "Plataforma indisponível", "Mensagem não envia"])
    ticket = st.text_input("Informe o numero do ticket aberto: ")
    hora_inicio = st.text_input("Informe a hora de inicio, UTILIZE O PADRÃO ABAIXO:",value="00:00:00")
    normalizado = st.checkbox("Normalizado")
    if normalizado == True:
        hora_fim = st.text_input("Informe a hora de normalização, UTILIZE O PADRÃO ABAIXO:",value="00:00:00")
    nao_normal = st.checkbox("Não Normalizado")
    inserir = st.button("Inserir")
    # Criar uma data fictícia
        
    if inserir:
        data_formatada = data.strftime("%Y-%m-%d")
        
        if motivo == 'Selecione o Motivo':
            st.error("Necessário selecionar um motivo valido...")
            return
        
        if ticket == '' or ticket == None:
            st.error("Necessário inserir o número do ticket")
            return
        
        if hora_inicio == '' or hora_inicio == None:
            st.error("Necessário inserir um horário de inicio")
            return
        
        if normalizado == True and nao_normal == True:
            st.error("Selecione apenas uma opção: Normalizado / Não Normalizado")
            return
        
        if normalizado == False and nao_normal == False:
            st.error("Selecione uma opção: Normalizado / Não Normalizado")
            return
        
        if normalizado == True:
            if hora_inicio == "00:00:00" or hora_fim == "00:00:00":
                st.error("Você deve informar uma hora válida, diferente de -> 00:00:00")
                return
        
        if hora_inicio == "00:00:00":
            st.error("Você deve informar uma hora válida, diferente de -> 00:00:00")
            return
        
        try:
            hora_inicio = datetime.strptime(hora_inicio, "%H:%M:%S").time()
            hora_inicio_str = hora_inicio.strftime("%H:%M:%S")
        except Exception as e:
            st.error("A hora inicio inserida está em um formato inválido...")
            return
        
        if normalizado == True:
            try:
                hora_fim = datetime.strptime(hora_fim, "%H:%M:%S").time()
                hora_fim_str = hora_inicio.strftime("%H:%M:%S")
            except Exception as e:
                st.error("A hora fim inserida está em um formato inválido...")
                return
            
        if normalizado == True:
            try:
                dados = {
                    "date":data_formatada,"ticket":ticket,"hora_inicio":hora_inicio_str,"hora_fim":hora_fim_str,
                    "normalizado":True,"motivo":motivo,"id":st.session_state.id,"nome_gestor":st.session_state.nomeLogado
                }   
                instanciarAPI = api('InserirTicketSmart')
                instanciarAPI.inserirTicket(dados)
            except Exception as e:
                st.error(f'Ocorreu algum erro: {e}')
        elif nao_normal == True:
            try:
                dados = {
                    "date":data_formatada,"ticket":ticket,"hora_inicio":hora_inicio_str,"hora_fim":"02:00:00",
                    "normalizado":False,"motivo":motivo,"id":st.session_state.id,"nome_gestor":st.session_state.nomeLogado
                }   
                instanciarAPI = api('InserirTicketSmart')
                instanciarAPI.inserirTicket(dados)
            except Exception as e:
                st.error(f'Ocorreu algum erro: {e}')

        
if __name__ == '__main__':
    mainInserirTicket()