import streamlit as st
from models.dataBase import SupabaseClient
from datetime import datetime
import pandas as pd
def informarNaoComparecimento():
    st.info("Ainda em desenvolvimento....")
    #Instanciar SupaBase
    instanciarSupaBase = SupabaseClient()
    
    # Obter a data atual
    data_atual = datetime.now()

    # Formatar a data
    data_formatada = data_atual.strftime("%Y-%m-%d")
    
    #Chama a função para visualizar os agendamentos
    retorno = instanciarSupaBase.visualizarAgendamentosInformarNaoComparecimento(data_formatada)
    retorno = pd.DataFrame(retorno)
    
    retorno = retorno.drop("id_gestor", axis=1)
    
    retorno = retorno.rename(columns={"data_agendamento":"Data agendada",
                                        "hora_inicio":"Horário de início",
                                        "hora_fim":"Horário de término",
                                        "Gestor":"Agendado por:",
                                        "created_at":"Agendado em"})
                
    retorno['Agendado em'] = pd.to_datetime(retorno['Agendado em']).dt.tz_convert('America/Sao_Paulo')
    retorno['Agendado em'] = retorno['Agendado em'].dt.strftime('%d/%m/%y - %H:%M:%S')
                
    retorno = retorno.reindex(["Data agendada", "Horário de início", "Horário de término", "Agendado por:", "Agendado em"],axis=1)
    retorno['Data agendada'] = pd.to_datetime(retorno['Data agendada'])
    retorno['Data agendada'] = retorno['Data agendada'].dt.strftime('%d/%m/%y')
    data_inserida_list = retorno["Agendado por:"].tolist()
    
    nome_formatado = []
    for i in data_inserida_list:
        partes = i.split(" ")
        if partes:
            Nome = partes[0]
            nome_formatado.append([Nome])

            nome_formatado_completo = []
    for i in nome_formatado:
        for j in i:
            nome_formatado_completo.append(j)

    retorno['Agendado por:'] = nome_formatado_completo
    
    colms = st.columns((1, 1, 1, 1,1))
    
    retorno["Informar:"] = ''
    
    retorno02 = retorno
    
    retorno02 = retorno02.drop("Agendado em",axis=1)
    
    cabecalhos_do_dataframe  = retorno02.columns.values.tolist()
    
    for col,campo_nome in zip(colms,cabecalhos_do_dataframe):
        col.write(campo_nome)
    
    for index, row in retorno.iterrows():
        col1, col2, col3, col4,col05 = st.columns((1, 1, 1, 1,1))
        col1.write(row["Data agendada"])
        col2.write(row["Horário de início"])
        col3.write(row["Horário de término"])
        col4.write(row["Agendado por:"])
        
        button_space_alterar = col05.empty()
        on_click_alterar = button_space_alterar.button("informar", 'btnAlterar' + str(row["Horário de início"]))
        
        if on_click_alterar:
            st.session_state.informarNaoComp = True
            st.session_state.informarNaoCompHoraInicio = str(row["Horário de início"])
            st.session_state.informarNaoCompPessoaQueAgendou = str(row["Agendado por:"])
            st.session_state.informarNaoCompDataAgendada = str(row["Data agendada"])
            st.session_state.informarNaoCompHoraFim = str(row["Horário de término"])
            st.session_state.informarNaoCompDataAtual = data_formatada
            st.rerun()
if __name__ == '__main__':
    informarNaoComparecimento()