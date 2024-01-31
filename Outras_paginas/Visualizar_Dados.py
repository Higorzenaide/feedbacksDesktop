import streamlit as st
from models.dataBase import SupabaseClient
    
def main():
    if st.session_state.loginValidado:
            if st.session_state.supervisao == False:
                st.error('Seu perfil não está habilitado para inserir feedbacks')
                return
            else:
                with st.spinner("Carregando dados..."):
                    instanceSupa = SupabaseClient()
                    instanceSupa.visualizarDadosUser(st.session_state.id)
    else:
        st.header('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                  '&nbsp;&nbsp;****EFETUE LOGIN PARA CONTINUAR****')
    
if __name__ == '__main__':
    main()