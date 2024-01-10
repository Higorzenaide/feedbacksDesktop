from dotenv import load_dotenv
import os
import streamlit as st
from supabase import create_client, Client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Agora você pode acessar suas variáveis de ambiente assim:
api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")
st.session_state.get("logado", False)
if 'id' not in st.session_state:
    st.session_state.id = None

if 'loginValidado' not in st.session_state:
    st.session_state.loginValidado = False

if 'nomeLogado' not in st.session_state:
    st.session_state.nomeLogado = False

if 'verificado' not in st.session_state:
    st.session_state.verificado = False


import os
from supabase import create_client, Client

class SupabaseClient:
    def __init__(self):
        self.url = os.environ.get("DATABASE_URL")
        self.key = os.environ.get("API_KEY")
        self.client = create_client(self.url, self.key)

    def new_user(self, email, password,nome,matricula):
        try:
            # Cria um novo usuário
            self._inserirCadastroNoBanco(nome,matricula,password,email)
        except Exception as e:
            st.write(f"Falha ao criar novo usuário: {e}")
    
    def login(self,email,password):
        try:
            response = self.client.table('users').select('id','Gestor','verificado').eq('email', email).eq('senha', password).execute()
            if response.data is None or len(response.data) == 0:
                st.write('Email ou senha, não confere')
            else:
                verificado = response.data[0]['verificado']
                st.session_state.verificado = verificado
                if st.session_state.verificado == False:
                    st.error('Seu usuário ainda não foi liberado, aguarde ou solicite a liberação.')
                    return
                st.success('Login efetuado com sucesso')
                st.session_state.loginValidado = True
                gestor_value = response.data[0]['Gestor']
                id_value = response.data[0]['id']
                st.session_state.id = id_value
                st.session_state.nomeLogado = gestor_value
        except Exception as e:
            st.write(f"Falha ao logar usuário: {e}")
    
    def _inserirCadastroNoBanco(self,nome,matricula,senha,email):
        try:
            data,count = self.client.table('users').insert({"Gestor":nome,"matricula":matricula,"senha":senha,"email":email,"verificado":False}).execute()
            st.success('Cadastro efetuado com sucesso')
            print(data,count)
        except Exception as e:
            st.error(f'Ocorreu algum erro inesperado{e}: Por favor tente novamente...')
    
    def inserirFeedback(self,date,motivo_macro,motivo,textoLivre,id_gestor,nome):
        try:
            data,count = self.client.table('feedbacks').insert({"date":date,"motivo_macro":motivo_macro,"motivo":motivo,"texto_livre":textoLivre,"id_gestor":id_gestor,"Nome_colaborador":nome}).execute()
        except Exception as e:
            st.error(f'Ocorreu algum erro inesperado{e}: Por favor tente novamente...')