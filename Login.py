import streamlit as st
from dotenv import load_dotenv
from models.dataBase import SupabaseClient
import os

def main():
    supabase_instance = SupabaseClient()
    st.set_page_config(
        page_title="Feedbacks DESKTOP",
        page_icon="🚀",
        layout="centered",  # Ou "centered" se preferir centralizar o conteúdo
        initial_sidebar_state="expanded",  # Ou "collapsed" para a barra lateral recolhida
    )

    st.sidebar.title("GESTÃO DE FEEDBACK´S COP")
    st.header('Seja Bem-vindo')
    with st.form(key="include_senha"):
        input_email = st.text_input(label="Insira o seu E-mail")
        input_pass = st.text_input(label="Insira a sua senha", type="password")
        input_button = st.form_submit_button("Logar")

    if input_button:
        if '@' in input_email:
            pass
        else:
            st.error('E-mail inserido inválido')
            return

        # Faça algo com os dados do formulário
        supabase_instance.login(input_email,input_pass)

if __name__ == '__main__':
    main()