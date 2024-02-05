import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from datetime import datetime, time
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,menuHorizontalInserirTicket,efetuarLogin,Calculasessao,fazerLogout
from Outras_paginas.inserir_ticket import mainInserirTicket
from models.api import IniciarAPI as api
import pandas as pd
from Outras_paginas.eidtar_ticket_smart import editarTicketSmart
def main():
    data = st.selectbox("Selecione o mês que deseja visualizar: ",["selecione","Janeiro","Fevereiro","Março",
                        "Abriu","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"])
    if data == 'selecione':
        return
    
    if data == 'Janeiro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-01-01/data_fim/2024-02-01')
    elif data == 'Fevereiro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-02-01/data_fim/2024-03-01')
    elif data == 'Março':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-03-01/data_fim/2024-04-01')
    elif data == 'Abriu':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-04-01/data_fim/2024-05-01')
    elif data == 'Maio':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-05-01/data_fim/2024-06-01')
    elif data == 'Junho':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-06-01/data_fim/2024-07-01')
    elif data == 'Julho':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-07-01/data_fim/2024-08-01')
    elif data == 'Agosto':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-08-01/data_fim/2024-09-01')
    elif data == 'Setembro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-09-01/data_fim/2024-10-01')
    elif data == 'Outubro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-10-01/data_fim/2024-11-01')
    elif data == 'Novembro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-11-01/data_fim/2024-12-01')
    elif data == 'Dezembro':
        instanciarAPI = api('VisualizarTicketsSmart/data_inicio/2024-12-01/data_fim/2025-01-01')
    else:
        return
    
    retorno = instanciarAPI.visualizarTickets()
    retorno = pd.DataFrame(retorno)
    if retorno.empty:
        st.error("Não há nenhum ticket nessa data selecionada...")
        return
    retorno = retorno.rename(columns={"data_incidente":"Data","hora_fim":"Hora fim",
                                      "hora_inicio":"Hora inicio","id":"Id registro","nome_gestor":"Gestor:",
                                      "normalizado":"Tratado?","num_ticket":"N° ticket"})
    
    retorno["Data"] = pd.to_datetime(retorno['Data'])
    retorno['Data'] = retorno['Data'].dt.strftime('%d/%m/%y')
    retorno = retorno.reindex(["Data","Hora inicio","Hora fim","Tratado?","N° ticket","Gestor:","Id registro"],axis=1)
    data_inserida_list = retorno["Gestor:"].tolist()
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

    retorno['Gestor:'] = nome_formatado_completo
    colms = st.columns((1, 1, 1, 1, 1,1,1))
    retorno["Alterar"] = ''
    retorno02 = retorno
    retorno02 = retorno02.drop("Id registro",axis=1)
    cabecalhos_do_dataframe  = retorno02.columns.values.tolist()
    for col,campo_nome in zip(colms,cabecalhos_do_dataframe):
        col.write(campo_nome)
    
    mapeamento = {True: "Sim", False: "Não"}
    mapeamento02 = {"02:00:00":"Em Aberto"}
    retorno["Tratado?"] = retorno["Tratado?"].map(mapeamento)
    retorno["Hora fim"] = retorno["Hora fim"].apply(lambda x: mapeamento02[x] if x == "02:00:00" else x)
    for index, row in retorno.iterrows():
        col1, col2, col3, col4, col5,col6,col8 = st.columns((1, 1, 1, 1, 1,1,1))
        col1.write(row["Data"])
        col2.write(row["Hora inicio"])
        col3.write(row["Hora fim"])
        col4.write(row["Tratado?"])
        col5.write(row["N° ticket"])
        col6.write(row["Gestor:"])
        idDoTicket = str(row["Id registro"])
        num_ticket = row["N° ticket"]
        inserido_por = row["Gestor:"]
        on_click_alterar = None
        
        if row["Tratado?"] == "Não":
            button_space_alterar = col8.empty()
            on_click_alterar = button_space_alterar.button("Alterar", 'btnAlterar' + str(row["Id registro"]))
        
        if on_click_alterar:
            st.session_state.editarTicketSmart = True
            dados = {
                "N° ticket":num_ticket,"id":idDoTicket,"gestor":inserido_por
            }
            
            st.session_state.dados2 = dados
            st.rerun()
            
            
if __name__ == '__main__':
    main()