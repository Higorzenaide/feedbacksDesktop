import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from Outras_paginas.cadastrar_colaborador import main as mainCadastrarColaborador
from Outras_paginas.registrar_presenca import main as mainRegistarPresenca
from Outras_paginas.inserir_advertencia import main as mainInserirAdvertencia
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,menuHorizontalSupervisorCOP,efetuarLogin,Calculasessao,fazerLogout
from datetime import datetime, timedelta
from PIL import Image

def main():
    definirVariaveisDaSessao()
    
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()

    # select = st.sidebar.selectbox('&nbsp;',['Selecione','Cadastrar colaborador','Inserir feedbacks','Visualizar feedbacks','Registrar presença','Inserir advertencia'])
    imagemSideBar()
    # st.sidebar.button('Sair')
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("estilos/styles.css")

    logout_button_clicked = st.sidebar.button("Logout", key="logout")

    if logout_button_clicked:
        fazerLogout()
        st.experimental_rerun()
    
    if st.session_state.logado == False:
        efetuarLogin()
        if st.session_state.sessao:
            st.error("Sessão expirada, realize o login novamente...")
            if st.session_state.rerun == False:
                st.session_state.rerun = True
                st.experimental_rerun()
            else:
                return
        else:
            return
    
    Calculasessao()

    if st.session_state.logado == True:
        if 'last_active_time' in st.session_state:
            elapsed_time = datetime.now() - st.session_state.last_active_time
            elapsed_minutes = elapsed_time.total_seconds() / 60  # Convert seconds to minutes
            formatted_time = "{:.2f}".format(elapsed_minutes)
            st.sidebar.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
            st.sidebar.markdown(f'<span style="font-size: small;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tempo de sessão: {formatted_time.split(".")[0]} minutos</span>', unsafe_allow_html=True)
    else:
        st.experimental_rerun()


    menu = menuHorizontalSupervisorCOP()
    if menu == 'Inserir feedbacks':
        mainInserirDados()
    elif menu == 'Visualizar feedbacks':
        mainVisualizarDados()
    elif menu == 'Cadastrar colaborador':
        mainCadastrarColaborador()
    elif menu == 'Registrar presença':
        mainRegistarPresenca()
    elif menu == 'Inserir advertencia':
        mainInserirAdvertencia()




if __name__ == '__main__':
    main()