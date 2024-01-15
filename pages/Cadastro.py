import streamlit as st
from models.dataBase import SupabaseClient
from models.funcoes import configuracoesIniciais,imagemSideBar,definirVariaveisDaSessao,logout,headerLogin,lerJsonGif,mostrarGif,senha_valida
from PIL import Image
import time

def main():

    #Definindo as variaveis em cookies
    definirVariaveisDaSessao()

    #Definindo as configurações iniciais
    configuracoesIniciais()

    #Imagem e titulo SideBart
    imagemSideBar()
    #Valida se o usuário está logado
    if st.session_state.logado == False:
        pass
    elif st.session_state.id != None:
        st.header('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                  '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Você já está logado')
        return
    
    imagem_url = "images/cadastre.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)
    logout()
    #Instanciando o Banco de dados
    supabase_instance = SupabaseClient()

    col1, col2 = st.columns(2)
    with col1:
        with st.form(key="include"):
            input_name = st.text_input(label="Insira o seu Nome completo:")
            input_email = st.text_input(label="Insira o seu E-mail:")
            input_matricula = st.number_input("Insira sua matrícula:", step=100, format="%d",max_value=100000000)
            input_pass = st.text_input(label="Insira uma senha:", type="password")
            confirmar_senha = st.text_input(label="Confirme sua senha:",type="password")
            input_button = st.form_submit_button("Cadastre-se")

    # Passando onde está o GIF
    lottie_codding = lerJsonGif("gifs/Animacao02.json")
    # Mostrando Gif
    with col2:
        mostrarGif(lottie_codding)

    # Se o botão for clicado
    if input_button:
        if len(input_name) > 5 and '' in input_name:
            pass
        else:
            st.error('insira um nome válido')
            return

        if '@' in input_email:
            pass
        else:
            msgError = st.error('E-mail inserido inválido')
            time.sleep(3)
            msgError.empty()
            return

        validadorDeMatricula = input_matricula
        validadorDeMatricula = str(validadorDeMatricula)
        if len(validadorDeMatricula) >= 2:
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
            st.error('A senha deve conter pelo menos 6 caracteres sendo 1 especial')
            return

        st.session_state['input_name'] = ''
        st.session_state['input_email'] = ''
        st.session_state['input_matricula'] = ''
        st.session_state['input_pass'] = ''
        st.session_state['confirmar_senha'] = ''
        supabase_instance.new_user(input_email, input_pass, input_name, input_matricula)
        
if __name__ == '__main__':
    main()
