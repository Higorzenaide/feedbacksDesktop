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

    
    #Calcule quanto tempo de sessão
    if st.session_state.logado == True:
        Calculasessao()


    menu = menuHorizontalInserirTicket()

    if menu == 'Inserir ticket':
        st.session_state.editarTicketSmart = False
        #Se a variavel logado for igual a False, exibe que precisa estar logado.
        if st.session_state.logado == False:
            efetuarLogin()
            if st.session_state.sessao:
                if st.session_state.rerun == False:
                    st.session_state.rerun = True
                    pass
                else:
                    return
            else:
                return
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
            else:
                editarTicketSmart()
        else:
            MainVisualizarTickets()
            

    #Imagem e titulo da SideBart.
    imagemSideBar()

    #Botão de logout. local_css é um função.
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # #Lendo os estilos
    # local_css("estilos/styles.css")

    # #Botão de logout
    # logout_button_clicked = st.sidebar.button("Logout")

    #Se o botão de logout for cliclado
    # if logout_button_clicked:
    #     fazerLogout()
    #     st.rerun()

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