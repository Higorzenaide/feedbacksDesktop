import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from Outras_paginas.cadastrar_colaborador import main as mainCadastrarColaborador
from Outras_paginas.registrar_presenca import main as mainRegistarPresenca
from Outras_paginas.inserir_advertencia import main as mainInserirAdvertencia
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,menuHorizontalSupervisorCOP,efetuarLogin

from PIL import Image

def main():
    definirVariaveisDaSessao()
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
        st.session_state.logado = False
        st.experimental_rerun()
    
    if st.session_state.logado == False:
        efetuarLogin()
        return
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