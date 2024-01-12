from dotenv import load_dotenv
import os
import streamlit as st
from supabase import create_client, Client
import pandas as pd


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Agora você pode acessar suas variáveis de ambiente assim:
api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")
st.session_state.get("logado", False)

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
            response = self.client.table('users').select('id','Gestor','verificado','supervisao','treinamentos').eq('email', email).eq('senha', password).execute()
            if response.data is None or len(response.data) == 0:
                st.write('Email ou senha, não confere')
            else:
                verificado = response.data[0]['verificado']
                st.session_state.verificado = verificado
                
                if st.session_state.verificado == False:
                    st.error('Seu usuário ainda não foi liberado, aguarde ou solicite a liberação.')
                    return
                
                id_value = response.data[0]['id']
                st.session_state.id = id_value
                supervisao = response.data[0]['supervisao']
                st.session_state.supervisao = supervisao
                treinamentos = response.data[0]['treinamentos']
                st.session_state.treinamentos = treinamentos
                st.session_state.logado = True
                st.success('Login efetuado com sucesso')
                st.session_state.loginValidado = True
                gestor_value = response.data[0]['Gestor']
                st.session_state.nomeLogado = gestor_value
        except Exception as e:
            st.write(f"Falha ao logar usuário: {e}")
    
    def _inserirCadastroNoBanco(self,nome,matricula,senha,email):
        try:
            data,count = self.client.table('users').insert({"Gestor":nome,"matricula":matricula,"senha":senha,"email":email,"verificado":False,"supervisao":False,"treinamentos":False}).execute()
            st.success('Cadastro efetuado com sucesso')
            print(data,count)
        except Exception as e:
            st.error(f'Ocorreu algum erro inesperado{e}: Por favor tente novamente...')
    
    def inserirFeedback(self,date,motivo_macro,motivo,textoLivre,id_gestor,nome):
        try:
            data,count = self.client.table('feedbacks').insert({"date":date,"motivo_macro":motivo_macro,"motivo":motivo,"texto_livre":textoLivre,"id_gestor":id_gestor,"Nome_colaborador":nome}).execute()
            st.success('Dados inseridos com sucesso')
        except Exception as e:
            st.error(f'Ocorreu algum erro inesperado{e}: Por favor tente novamente...')

    def visualizarDadosUser(self,id):
        try:
            if id == None or id == '':
                st.header('Faça login para vizualizar dados')
                return
            response = self.client.table('feedbacks').select('motivo_macro','motivo','Nome_colaborador','date').eq('id_gestor', id).execute()
            # Converter a resposta para um DataFrame do pandas
            data = pd.DataFrame(response)
            result= response.data
            st.write(result)
        except Exception as e:
            st.write(e)

