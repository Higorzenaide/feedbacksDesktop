import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,definirVariaveisDaSessao,local_css,imagemSideBar,Calculasessao,fazerLogout,menuHorizontalSalaDeReuniao,efetuarLogin
from Outras_paginas.editar_agendamento_sala import main as mainEditarAgendamentoSala
from Outras_paginas.visualizar_agendamento_sala import main as mainVisualizarAgendamentoSala
from Outras_paginas.realizarAgendamento_salareuniao import main as mainSalaReuniao
from datetime import datetime

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

    #Botão de logout. local_css é um função.
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    #Lendo os estilos
    local_css("estilos/styles.css")

    #Botão de logout
    logout_button_clicked = st.sidebar.button("Logout", key="logout")

    #Se o botão de logout for cliclado
    if logout_button_clicked:
        fazerLogout()
        st.experimental_rerun()

    if menu == 'Realizar Agendamento':
        if st.session_state.logado == False:
            efetuarLogin()
            return
        mainSalaReuniao()
    elif menu == 'Visualizar agendamentos':
        mainVisualizarAgendamentoSala()
        return
    elif menu == 'Editar seu Agendamento':
        mainEditarAgendamentoSala()
        return
    
    #Calcule quanto tempo de sessão
    Calculasessao()

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

# Chamar a função principal
if __name__ == '__main__':
    main()