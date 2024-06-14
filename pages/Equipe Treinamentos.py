import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,logout,definirVariaveisDaSessao

def main():
    definirVariaveisDaSessao()
    st.write("O site GCP foi migrado para 'https://gestao-cop.vercel.app/home' ")
    return
    if st.session_state.configuracoesIniciais == False:
        configuracoesIniciais()

    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("estilos/styles.css")

    logout_button_clicked = st.sidebar.button("Logout", key="logout")

    if logout_button_clicked:
        st.session_state.logado = False
        st.experimental_rerun()

if __name__ == '__main__':
    main()
