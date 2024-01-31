import requests
from datetime import datetime
import json
import streamlit as st
import time

URL = "https://api-dte3.onrender.com/"

class IniciarAPI:
    def __init__(self, rota):
        self.url = f"{URL}{rota}"  # Concatena a rota à URL
        self.rota = rota
    
    def fazerLogin(self, dados):

        # Use self.url como a URL completa e envie dados como JSON
        response = requests.get(self.url, json=dados)
        # Verificar o status da resposta
        retorno_json = response.json()
        dicionario = retorno_json[0]

        if response.status_code == 200:
            if "error" in dicionario:
                st.error("Email ou senha, não conferem!")
                return False
            else:
                return dicionario
        else:
            st.error("Ocorreu algum erro ao estabelecer a conexão com o banco de dados!")

    def criarNovoUsuario(self,dados):
        response = requests.post(self.url,json=dados)
        retorno_json = response.json()
        dicionario = retorno_json[0]

        if response.status_code == 200:
            if "error" in dicionario:
                st.error(dicionario)
                return dicionario
            else:
                return dicionario
        else:
            st.error("Ocorreu algum erro ao estabelecer a conexão com o banco de dados!")

    def inserirFeedback(self,dados):
        try:
            response = requests.post(self.url,json=dados)
            retorno_json = response.json()
            dicionario = retorno_json[0]

            if response.status_code == 200:
                if "error" in dicionario:
                    st.error(dicionario)
                    return dicionario
                else:
                    return dicionario
            else:
                st.error("Ocorreu algum erro ao estabelecer a conexão com o banco de dados!")
                return {dicionario}
        except Exception as e:
            error = str(e)
            st.error(f'ocoreeu algum erro {error}')
    
    def visualizarFeedbacks(self,id):
        try:
            response = requests.get(self.url,json=id)
            retorno_json = response.json()
            dicionario = retorno_json
            if response.status_code == 200:
                if "error" in dicionario:
                    st.error(dicionario)
                    return dicionario
                else:
                    return dicionario
            else:
                st.error("Ocorreu algum erro ao estabelecer a conexão com o banco de dados!")
                return {dicionario}
        except Exception as e:
            error = str(e)
            st.error(f'ocoreeu algum erro {error}')

    def inserirAgendamentoSalaReuniao(self,dados):
        try:
            response = requests.post(self.url,json=dados)
            retorno_json = response.json()
            dicionario = retorno_json[0]
            if response.status_code == 200:
                if "erro" in dicionario:
                    st.error(dicionario)
                    return dicionario
                else:
                    return dicionario
            else:
                st.error("Ocorreu algum erro ao estabelecer a conexão com o banco de dados!")
                return {dicionario}
        except Exception as e:
            error = str(e)
            st.error(f'ocoreeu algum erro {error}')

    def visualizarAgendamentos(self,data_agendamento):
        try:
            response = requests.get(self.url+f'/{data_agendamento}')
            
            retorno = response.json()
            dicionario = retorno 

            if response.status_code == 200:
                if 'error' in dicionario:
                    st.error("Não há agendamentos para está data!")
                    return False
                else:
                    return dicionario
        except Exception as e:
            st.error(f'Ocorreu algum erro {str(e)}')
    
    def visualizarAgendamentosParaEditar(self,dados):
        try:
            response = requests.get(self.url,json=dados)
            retornoapi = response.json()
            
            if response.status_code == 200:
                if 'error' in retornoapi:
                    return False
                else:
                    return retornoapi
        except Exception as e:
            error = str(e)
            st.error(f'Ocorreu um erro com a comunicação com a API {error}')

    def excluirAgendamento(self,id):
        try:
            response = requests.post(self.url,json=id)
            retornoapi = response.json()
            if response.status_code == 200:
                if 'error' in retornoapi:
                    st.error('Ocorreu algum erro')
                    st.write(response)
                else:
                    return retornoapi
        except Exception as e:
            error = str(e)
            st.error(f'Ocorreu um erro com a comunicação com a API {error}')

    def editarAgendamentos(self,dados):
        try:
            response = requests.post(self.url,json=dados)
            retornoapi = response.json()
            print(f'------------------retorno-----------------{retornoapi}')
            if response.status_code == 200:
                print('entrou--------------------------')
                if 'error' in retornoapi[0]:
                    st.error(f'Conflito de horários.')
                    time.sleep(3)
                else:
                    st.success("Agendamento alterado com sucesso")
                    time.sleep(2)
                    return retornoapi
        except Exception as e:
            error = str(e)
            st.error(f'Ocorreu um erro com a comunicação com a API {error}')