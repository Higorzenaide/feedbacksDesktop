import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from Outras_paginas.cadastrar_colaborador import main as mainCadastrarColaborador
from Outras_paginas.registrar_presenca import main as mainRegistarPresenca
from Outras_paginas.inserir_advertencia import main as mainInserirAdvertencia
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao

from PIL import Image

def main():
    definirVariaveisDaSessao()
    configuracoesIniciais()
    select = st.sidebar.selectbox('&nbsp;',['Selecione','Cadastrar colaborador','Inserir feedbacks','Visualizar feedbacks','Registrar presença','Inserir advertencia'])
    #Caminho da imagem
    imagem_path = "F:\\Feedbacks\\feedbacksDesktop\\images\\logo3.jpeg"
    imagem = Image.open(imagem_path)

    # Dividir a página em colunas
    col1, col2, col3 = st.sidebar.columns([1, 1, 1])

    # Coluna 1: Adicionar imagem à barra lateral
    with col1:
        st.sidebar.image(imagem, use_column_width=True)
        st.sidebar.subheader("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GESTÃO COP")

    st.sidebar.button('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                      '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sair&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                      '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    if select == 'Inserir feedbacks':
        mainInserirDados()
    elif select == 'Visualizar feedbacks':
        mainVisualizarDados()
    elif select == 'Cadastrar colaborador':
        mainCadastrarColaborador()
    elif select == 'Registrar presença':
        mainRegistarPresenca()
    elif select == 'Inserir advertencia':
        mainInserirAdvertencia()




if __name__ == '__main__':
    main()