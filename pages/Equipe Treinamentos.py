import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,logout

def main():
    configuracoesIniciais()
    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    logout()

if __name__ == '__main__':
    main()