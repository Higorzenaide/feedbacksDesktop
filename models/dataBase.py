from dotenv import load_dotenv
import os
import json
import streamlit as st
from supabase import create_client, Client
import pandas as pd
import time
from models.funcoes import DefinirSessao
import datetime
import pytz

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
            with st.spinner("Realizando o login..."):
                response = self.client.table('users').select('id','Gestor','verificado','supervisao','treinamentos').eq('email', email).eq('senha', password).execute()
                if response.data is None or len(response.data) == 0:
                    st.error('Email ou senha, não confere')
                else:
                    verificado = response.data[0]['verificado']
                    st.session_state.verificado = verificado
                    
                    if st.session_state.verificado == False:
                        st.error('Seu usuário ainda não foi liberado, aguarde ou solicite a liberação.')
                        st.success('Para solicitar liberação solicite: +55 (19) 92002-1690 - Higor Zeinaide | +55 (19) 98399-2678 - Danilo Vargas')
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
                    DefinirSessao()
                    st.experimental_rerun()
        except Exception as e:
            st.write(f"Falha ao logar usuário: {e}")
    
    def _inserirCadastroNoBanco(self,nome,matricula,senha,email):
        try:
            data,count = self.client.table('users').insert({"Gestor":nome,"matricula":matricula,"senha":senha,"email":email,"verificado":False,"supervisao":False,"treinamentos":False}).execute()
            st.success('Cadastro efetuado com sucesso')
        except Exception as e:
            errorMensagem = st.error(f'Ocorreu algum erro inesperado{e}: Por favor tente novamente...')
            time.sleep(5)
            errorMensagem.empty()
    
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

    def inserirAgendamentoSalaReuniao(self, dados_agendamento):
        try:
            with st.spinner("Realizando Agendamento..."):
                # Carregar os dados do JSON
                agendamento = json.loads(dados_agendamento)

                # Extrair dados do dicionário
                data_agendamento = agendamento["data"]
                hora_inicio = agendamento["hora_inicio"]
                hora_fim = agendamento["hora_termino"]
                id_gestor = agendamento["id_usuario"]
                Gestor01 = agendamento["Gestor"]

                retorno = self.conflitos(data_agendamento,hora_inicio,hora_fim)
                
                # Inserir dados no Supabase
                if retorno:
                    data, count = self.client.table('sala_de_reuniao').insert({
                        "data_agendamento": data_agendamento,
                        "hora_inicio": hora_inicio,
                        "hora_fim": hora_fim,
                        "id_gestor": id_gestor,
                        "Gestor": Gestor01
                    }).execute()

                    Sucess = st.success('Agendamento efetuado com sucesso')
                    Sucess.empty()
                    return True 
                else:
                    pass    
        except Exception as e:
                errorMensagem = st.error(f'Ocorreu algum erro inesperado {e}: Por favor, tente novamente...')
                time.sleep(5)
                errorMensagem.empty()
    
    def conflitos(self,data_agendamento,hora_inicio,hora_fim):
        try:
            response,data = self.client.table('sala_de_reuniao').select('data_agendamento','hora_inicio','hora_fim').eq('data_agendamento', data_agendamento).execute()
            # Converter a resposta para um DataFrame do pandas
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            # Criar DataFrame a partir da lista de dicionários
            df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim'])
            # Converter as strings de hora para objetos datetime.time
            df['hora_inicio'] = pd.to_datetime(df['hora_inicio']).dt.time
            df['hora_fim'] = pd.to_datetime(df['hora_fim']).dt.time
            novo_horario_inicio = datetime.datetime.strptime(hora_inicio, '%H:%M:%S').time()
            novo_horario_fim = datetime.datetime.strptime(hora_fim, '%H:%M:%S').time()

            # Verificar se há conflito de horário
            conflito = any(
                ((novo_horario_inicio >= df['hora_inicio']) & (novo_horario_inicio < df['hora_fim'])) |
                ((novo_horario_fim > df['hora_inicio']) & (novo_horario_fim <= df['hora_fim'])) |
                ((novo_horario_inicio <= df['hora_inicio']) & (novo_horario_fim >= df['hora_fim']))
            )

            if conflito:
                st.error("Conflito de horário! Escolha outro horário para o agendamento.")
                return False
            else:
                return True
                # Insira o novo agendamento no banco de dados aqui

        except Exception as e:
            st.write(e)


    def conflitos2(self, data_agendamento, hora_inicio, hora_fim):
        try:
            # Obter dados da tabela sala_de_reuniao
            response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim').eq('data_agendamento', data_agendamento).execute()

            # Converter a resposta para um DataFrame do pandas
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            
            # Criar DataFrame a partir da lista de dicionários
            df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim'])

            # Utilizar datetime.strptime para converter as strings em objetos time
            novo_horario_inicio = hora_inicio
            novo_horario_fim = hora_fim

            # Converter colunas hora_inicio e hora_fim para objetos datetime.time
            df['hora_inicio'] = pd.to_datetime(df['hora_inicio']).dt.time
            df['hora_fim'] = pd.to_datetime(df['hora_fim']).dt.time

            # Verificar se há conflito de horário
            conflito = any(
                ((novo_horario_inicio >= df['hora_inicio']) & (novo_horario_inicio < df['hora_fim'])) |
                ((novo_horario_fim > df['hora_inicio']) & (novo_horario_fim <= df['hora_fim'])) |
                ((novo_horario_inicio <= df['hora_inicio']) & (novo_horario_fim >= df['hora_fim']))
            )

            if conflito:
                st.error("Conflito de horário! Escolha outro horário para o agendamento.")
                return False
            else:
                return True
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
            return False

    def visualizarAgendamentos(self, data_agendamento):
        try:
            with st.spinner("Carregando agendamentos..."):
                response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor', 'created_at').eq('data_agendamento', data_agendamento).execute()

                # Converter a resposta para um DataFrame do pandas
                response_string = response[1]
                resposta = json.loads(json.dumps(response_string))

                # Criar DataFrame a partir da lista de dicionários
                df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor', 'created_at'])
                # Renomear as colunas
                df = df.rename(columns={'data_agendamento': 'Data de agendamento',
                                        'hora_inicio': 'Horário de início',
                                        'hora_fim': 'Horário de término',
                                        'Gestor': 'Nome do responsável',
                                        'created_at': 'Agendado em'})
                # Ajustar o fuso horário de created_at para o fuso horário desejado (por exemplo, 'America/Sao_Paulo')
                df['Agendado em'] = pd.to_datetime(df['Agendado em']).dt.tz_convert('America/Sao_Paulo')

                # Formatando a data sem o fuso horário
                df['Agendado em'] = df['Agendado em'].dt.strftime('%Y-%m-%d %H:%M:%S')

                st.write(df)
        except Exception as e:
                st.error("Não há nenhum agendamento nesta data selecionada...")

    def visualizarAgendamentosParaEditar(self,id,data):
        try:
            with st.spinner("Carregando edição de agendamentos..."):
                response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor','id').eq('id_gestor', id).eq('data_agendamento', data).execute()
                response_string = response[1]
                if response_string == '' or response_string == None or response_string == []:
                    st.error('Você não tem nenhuma agendamento feito nesta data...')
                return(response_string)
        except Exception as e:
            st.error('Você não tem nenhuma agendamento feito nesta data...')
            return

    def editarAgendamento(self, id,data):
        # try:
        #     with st.spinner("Carregando edição de agendamentos..."):
        #         response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor','id').eq('id_gestor', id).eq('data_agendamento', data).execute()
        #         response_string = response[1]
        #         if response_string == '' or response_string == None or response_string == []:
        #             st.error('Você não tem nenhuma agendamento feito nesta data...')
        # except Exception as e:
        #     st.error('Você não tem nenhuma agendamento feito nesta data...')
        #     return
        if 'agenda' not in st.session_state:
            st.session_state.agenda = False

        def visu():
            response = self.visualizarAgendamentosParaEditar(id,data)
            st.session_state.agenda = response

        Visualizar = st.button("Visualizar")
        if Visualizar:
            visu()

        # Converter a resposta para um DataFrame do pandas
        
        if st.session_state.agenda != False:
            response_string = st.session_state.agenda
            resposta = json.loads(json.dumps(response_string))

            # Criar DataFrame a partir da lista de dicionários
            df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor','id'])
            
            # Definir o número de colunas desejado
            num_colunas = 1
            
            for index in range(len(df)):
                st.write(f"Edição para agendamento N° : {index + 1}")
                col = st.columns(num_colunas)
                novos_valores = []
                # Lista para armazenar os novos valores
                
                for i, campo_nome in enumerate(df.columns):
                    chave = f"{index}_{campo_nome}"

                    if campo_nome == 'hora_inicio' or campo_nome == 'hora_fim':
                        novo_valor = col[i % num_colunas].time_input(f"Nova {campo_nome}:", pd.to_datetime(df[campo_nome].iloc[index]).time(), key=chave)
                    elif campo_nome == 'data_agendamento':
                        novo_valor = col[i % num_colunas].date_input(f"Nova {campo_nome}:", pd.to_datetime(df[campo_nome].iloc[index]).date(), key=chave)
                    elif campo_nome == 'Gestor':
                        # Campo do nome do Gestor é desabilitado para edição
                        novo_valor = col[i % num_colunas].text_input(f"{campo_nome}:", df[campo_nome].iloc[index], key=chave, disabled=True)
                    else:
                        novo_valor = col[i % num_colunas].text_input(f"{campo_nome} do agendamento:", df[campo_nome].iloc[index], key=chave,disabled=True)


                    # Adicionar o novo valor à lista
                    novos_valores.append(novo_valor)

                # Botões para confirmar a edição e excluir para cada linha
                col1, col2, col3 = st.columns(3)
                col1.empty()
                with col2:
                    btn_confirmar = col[0].button(f"Confirmar Edição de N° {index + 1}")
                    btn_excluir = col[0].button(f"Excluir Edição de N° {index + 1}")

                if btn_confirmar:
                    with st.spinner("Atualizando agendamento...."):
                        retorno = self.conflitos2(novos_valores[0], novos_valores[1], novos_valores[2])
                        if retorno:
                                novos_valores = [
                            str(novos_valores[0]),  # Convertendo data para string
                            str(novos_valores[1]),  # Convertendo hora_inicio para string
                            str(novos_valores[2]),  # Convertendo hora_fim para string
                            novos_valores[3],        # Gestor permanece como está (string)
                            int(novos_valores[4])    # Convertendo id para inteiro
                            ]
                                data, count = self.client.table('sala_de_reuniao').update({'data_agendamento': novos_valores[0],
                                    'hora_inicio': novos_valores[1],
                                    'hora_fim': novos_valores[2]
                                }).eq('id', novos_valores[4]).execute()
                                st.success("Agendamento editado com sucesso!")
                                visu()
                                st.experimental_rerun()
                            # Adicione aqui a lógica para confirmar a edição no seu banco de dados
                        
                if btn_excluir:
                        with st.spinner("Excluindo agendamento..."):
                            data, count = self.client.table('sala_de_reuniao').delete().eq('data_agendamento',novos_valores[0]).eq('hora_inicio', novos_valores[1]).eq('hora_fim',novos_valores[2]).execute()
                            st.success("Linha excluída com sucesso!")
                            visu()
                            st.experimental_rerun()
                        
        else:
            st.write("Necessário clicar em visualizar.....")
                






            
