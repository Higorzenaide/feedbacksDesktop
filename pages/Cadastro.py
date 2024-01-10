import streamlit as st
from models.dataBase import SupabaseClient
import string

def senha_valida(senha):
    caracteres_especiais = string.punctuation  # Obtem todos os caracteres especiais

    # Verifica se pelo menos um caractere especial está presente na senha
    if any(char in caracteres_especiais for char in senha):
        if len(senha) >= 6:
            return True
    else:
        return False


def main():
    supabase_instance = SupabaseClient()
    st.sidebar.title("GESTÃO DE FEEDBACK´S COP")
    st.header("Insira os dados para efetuar o seu cadastro")
    with st.form(key="include"):
        input_name = st.text_input(label="Insira o seu Nome completo")
        input_email = st.text_input(label="Insira o seu E-mail")
        input_matricula = st.number_input("Insira a matrícula", step=1, format="%d",max_value=100000000)
        input_pass = st.text_input(label="Insira a sua senha", type="password")
        confirmar_senha = st.text_input(label="Confirme sua senha",type="password")
        input_button = st.form_submit_button("Cadastrar")
            
    if input_button:
        if len(input_name) > 5 and '' in input_name:
            pass
        else:
            st.error('insira um nome válido')
            return
    
        if '@' in input_email:
            pass
        else:
            st.error('E-mail inserido inválido')
            return
        
        validadorDeMatricula = input_matricula
        validadorDeMatricula = str(validadorDeMatricula)
        if len(validadorDeMatricula) >=2:
            pass
        else:
            st.error('Insira uma matricula válida')
            return
        
        if confirmar_senha == input_pass:
            pass
        else:
            st.error('Senhas não conferem')
            return
        
        validadorDeSenha = senha_valida(input_pass)
        if validadorDeSenha:
            pass
        else:
            st.error('A senha deve conter pelomenos 6 caracteres sendo 1 especial')
            return


        supabase_instance.new_user(input_email,input_pass,input_name,input_matricula)
if __name__ == '__main__':
    main()
