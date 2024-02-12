import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,definirVariaveisDaSessao,local_css,imagemSideBar,Calculasessao,fazerLogout,menuHorizontalSalaDeReuniao,efetuarLogin,informativoAgendamentoSala
from Outras_paginas.editar_agendamento_sala import main as mainEditarAgendamentoSala
from Outras_paginas.visualizar_agendamento_sala import main as mainVisualizarAgendamentoSala
from Outras_paginas.realizarAgendamento_salareuniao import main as mainSalaReuniao
from datetime import datetime
from Outras_paginas.confirmaredicaoagendamento import main as mainEditar
from Outras_paginas.informarNaoComparecimento import informarNaoComparecimento
from Outras_paginas.perguntasNaoComparecimento import OpcoesInformarNaoComparecimento
def main():

    #Definindo as variaveis em cookies.
    definirVariaveisDaSessao()

    #Chamando a função de configurações iniciais, caso não tenha sido iniciado por outra pagina.
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()
    
   # Menu horizontal
    menu = menuHorizontalSalaDeReuniao()

    #Imagem SideBar
    imagemSideBar()

    if menu == 'Realizar Agendamento':
        if st.session_state.logado == False:
            st.session_state.editar = False
            efetuarLogin()
            return
        if st.session_state.agendamentoSala == True:
            st.session_state.informarNaoComp = False
            informativoAgendamentoSala()
            st.session_state.agendamentoSala = False
        else:
            mainSalaReuniao()
    elif menu == 'Visualizar agendamentos':
        st.session_state.informarNaoComp = False
        st.session_state.editar = False
        mainVisualizarAgendamentoSala()
        return
    elif menu == 'Editar seu Agendamento':
        if st.session_state.editar == True:
            st.session_state.informarNaoComp = False
            retorno = mainEditar()
        else:
            retorno = mainEditarAgendamentoSala()
    elif menu == 'Informar não comparecimento':
        if st.session_state.informarNaoComp == True:
            OpcoesInformarNaoComparecimento()
        else:
            informarNaoComparecimento()
            st.session_state.informarNaoComp = False
    
    #Calcule quanto tempo de sessão
    Calculasessao()

# Chamar a função principal
if __name__ == '__main__':
    main()