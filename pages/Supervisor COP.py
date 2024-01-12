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
    imagemSideBar()
    select = st.sidebar.selectbox('&nbsp;',['Selecione','Cadastrar colaborador','Inserir feedbacks','Visualizar feedbacks','Registrar presença','Inserir advertencia'])

    st.sidebar.button('Sair')
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