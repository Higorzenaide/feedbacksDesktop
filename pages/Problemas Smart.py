import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from datetime import datetime, time
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,menuHorizontalInserirTicket,efetuarLogin,Calculasessao,fazerLogout
from Outras_paginas.inserir_ticket import mainInserirTicket
from Outras_paginas.visualizar_tickets import main as MainVisualizarTickets
from Outras_paginas.eidtar_ticket_smart import editarTicketSmart
def main():
    
    #Definindo as variaveis em cookies.
    definirVariaveisDaSessao()
    
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()

    #Imagem no sideBar
    imagemSideBar()
    
    #Calcule quanto tempo de sessão
    if st.session_state.logado == True:
        Calculasessao()

    #Chamando o menu Horizontal
    menu = menuHorizontalInserirTicket()

    if menu == 'Inserir ticket':
        st.session_state.editarTicketSmart = False
        if st.session_state.logado == False:
            efetuarLogin()
            return
        else:
            mainInserirTicket()
    elif menu == 'Visualizar tickets':
        if st.session_state.editarTicketSmart == True:
            if st.session_state.logado == False:
                efetuarLogin()
                st.session_state.editarTicketSmart = False
                st.error("Você precisa efetuar login para acessar...")
                # #Lendo os estilos
                #Botão de logout. local_css é um função.
                def local_css(file_name):
                    with open(file_name) as f:
                        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                local_css("estilos/styles.css")
                st.button("Voltar")
            elif st.session_state.supervisao == False:
                st.error("Você não tem permissão para executar está ação...")
                return
            else:
                editarTicketSmart()
        else:
            MainVisualizarTickets()


    #Se o usuário estiver logado informao tempo de sessão.
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