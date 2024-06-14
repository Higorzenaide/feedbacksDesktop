import streamlit as st
#from Outras_paginas.Inserir_Dados import main as mainInserirDados
#from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
#from Outras_paginas.cadastrar_colaborador import main as mainCadastrarColaborador
#from Outras_paginas.registrar_presenca import main as mainRegistarPresenca
#from Outras_paginas.inserir_advertencia import main as mainInserirAdvertencia
#from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,menuHorizontalSupervisorCOP,efetuarLogin,Calculasessao,fazerLogout
#from datetime import datetime
#from PIL import Image

def main():

    #Definindo as variaveis em cookies.
    #definirVariaveisDaSessao()
    st.write("O site GCP foi migrado para 'https://gestao-cop.vercel.app/home' ")
    return
    #Se o login já foi feito, mostre imagem e mais nada.
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()

    
    #Se a variavel logado for igual a False, exibe que precisa estar logado
    if st.session_state.logado == False:
        efetuarLogin()
        if st.session_state.sessao:
            st.error("Realize o login novamente, para acessar...")
            if st.session_state.rerun == False:
                st.session_state.rerun = True
                pass
            else:
                return
        else:
            return
    
    #Calcule quanto tempo de sessão
    if st.session_state.logado == True:
        Calculasessao()

    if st.session_state.logado == True:
    #Menu horizontal
        menu = menuHorizontalSupervisorCOP()
    
        if menu == 'Inserir feedbacks':
            mainInserirDados()
        elif menu == 'Visualizar feedbacks':
            mainVisualizarDados()
        elif menu == 'Colaborador':
            colaborador = st.sidebar.selectbox('Selecione uma opção', ["Cadastrar Colaborador","Cadastrar Equipamento","Editar Dados","Desligamento"])
            if colaborador == 'Cadastrar Colaborador':
                mainCadastrarColaborador()
            elif colaborador == 'Cadastrar Equipamento':
                return
            elif colaborador == 'Editar Dados':
                return
            elif colaborador == 'Editar Dados':
                return
            elif colaborador == 'Desligamento':
                return
        elif menu == 'Registrar presença':
            mainRegistarPresenca()
        elif menu == 'Inserir advertencia':
            mainInserirAdvertencia()

    #Imagem e titulo da SideBart.
    imagemSideBar()

    #Botão de logout. local_css é um função.
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    #Lendo os estilos
    local_css("estilos/styles.css")

    #Botão de logout
    logout_button_clicked = st.sidebar.button("Logout")

    #Se o botão de logout for cliclado
    if logout_button_clicked:
        fazerLogout()
        st.rerun()

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
if __name__ == '__main__':
    main()
