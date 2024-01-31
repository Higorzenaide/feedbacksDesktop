from dotenv import load_dotenv
import os
import json
import streamlit as st
from supabase import create_client, Client
import pandas as pd
import time
from models.funcoes import DefinirSessao
from models.api import IniciarAPI as api
import datetime
import pytz
import streamlit as st
import datetime
import time
from datetime import datetime, time, timedelta

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
            dados = {"nome":nome,"email":email,"matricula":matricula,"senha":password}

            instanciarAPI = api("FazerCadastro")
            retorno = instanciarAPI.criarNovoUsuario(dados)
            if 'Sucess' in retorno:
                st.session_state.cadastroEfetuado = True 
                return True
            else:
                return False
        except Exception as e:
            error = str(e)
            st.error(f'Ocorreu algum erro: {error}')
            return False

    def login(self,email,password):
        try:
            dados = {"email":email,"senha":password}
            instanciarAPI = api("ConsultarLogin")
            retorno = instanciarAPI.fazerLogin(dados)

            if retorno == False:
                return
                
            verificado = retorno["verificado"]
            st.session_state.verificado = verificado

            if st.session_state.verificado == False:
                        st.error('Seu usuário ainda não foi liberado, aguarde ou solicite a liberação.')
                        st.success('Para solicitar liberação solicite: +55 (19) 92002-1690 - Higor Zeinaide | +55 (19) 98399-2678 - Danilo Vargas')
                        return
                
            id_value = retorno["id"]
            st.session_state.id = id_value

            supervisao = retorno["supervisao"]
            st.session_state.supervisao = supervisao

            treinamentos = retorno["treinamentos"]
            st.session_state.treinamentos = treinamentos

            gestor_value = retorno["Gestor"]
            st.session_state.nomeLogado = gestor_value

            st.session_state.logado = True
            st.session_state.loginValidado = True

            DefinirSessao()
            st.rerun()
        except Exception as e:
            st.write(f"Falha ao logar usuário: {e}")
    
    def inserirFeedback(self,motivo_macro,motivo,textoLivre,id_gestor,nome):
        try:
            dados = {"motivo_macro":motivo_macro,
                     "motivo":motivo,
                     "pontos":textoLivre,
                     "id_gestor":id_gestor,
                     "Nome_colaborador":nome}
            
            instanciarBanco = api("InserirFeedback")
            retornoapi = instanciarBanco.inserirFeedback(dados)
        except Exception as e:
            st.error("Ocorreu algum erro na comunicação API")
        if "Sucess" in retornoapi:
            st.success("Dados inseridos com sucesso")
            return True
        else:
            st.error(f'Ocorreu algum erro inesperado {retornoapi}')

    def visualizarDadosUser(self,id):
        try:
            if id == None or id == '':
                st.header('Faça login para vizualizar dados')
                return
            dados = {"id":id}
            instanciarAPI = api('VisualizarFeedbacks')
            retorno = instanciarAPI.visualizarFeedbacks(dados)
            retorno = pd.DataFrame(retorno)
            data_inserida_list = retorno["data_inserida"].tolist()
            retorno = retorno.drop("data_inserida", axis=1)
            lista_formata = []
            for i in data_inserida_list:
                date, time = i.split('T')
                lista_formata.append([date])
                # Adicionar a nova coluna 'data_agendada' ao DataFrame
            retorno['data_inserida'] = lista_formata
            retorno = retorno.rename(columns={"data_inserida":"Data",
                                              "motivo":"Motivo",
                                              "motivo_macro":"Motivo Macro",
                                              "nome_colaborador":"Nome",
                                              "nome_supervisor":"Supervisor"})
            retorno.set_index('Data', inplace=True)
            retorno = retorno.drop("Supervisor", axis=1)
            st.write(retorno)
        except Exception as e:
            st.write(e)

    def inserirAgendamentoSalaReuniao(self, dados_agendamento):
        try:
            with st.spinner("Realizando agendamento..."):
                data_agendamento = dados_agendamento["data"]
                hora_inicio = dados_agendamento["hora_inicio"]
                hora_fim = dados_agendamento["hora_termino"]
                id = dados_agendamento["id_usuario"]
                Gestor = dados_agendamento["Gestor"]

                dados = {"data_agendamento":data_agendamento,"hora_inicio":hora_inicio,"hora_fim":hora_fim,"id":id,"Gestor":Gestor}
                instanciarBanco = api('FazerAgendamento')
                retorno = instanciarBanco.inserirAgendamentoSalaReuniao(dados)
        except Exception as e:
            error = str(e)
            st.write(error)
            
        if "error" in retorno:
            st.error(f'Horario conflitando com outro horario já agendado inicio: {retorno["horario_inicio"]} até {retorno["horario_fim"]}')
            return
        else:
            return True
    
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
            response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim','id_gestor').eq('data_agendamento', data_agendamento).execute()

            # Converter a resposta para um DataFrame do pandas
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            
            # Filtrar os dados onde "id_gestor" é diferente de st.session_state.id
            resposta_filtrada = [item for item in resposta if item.get('id_gestor') != st.session_state.id]

            # Criar DataFrame a partir da lista de dicionários filtrada
            df = pd.DataFrame(resposta_filtrada, columns=['data_agendamento', 'hora_inicio', 'hora_fim'])
            # Criar DataFrame a partir da lista de dicionários
            # df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim'])

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
                instanciarAPI = api('/VisualizarAgendamentos')
                retorno = instanciarAPI.visualizarAgendamentos(data_agendamento)
                if retorno == False:
                    return
                df = pd.DataFrame(retorno)
                df = df.drop("id_gestor", axis=1)
                df = df.rename(columns={"data_agendamento":"Data agendada",
                                        "hora_inicio":"Horário de início",
                                        "hora_fim":"Horário de término",
                                        "Gestor":"Agendado por:",
                                        "created_at":"Agendado em"})
                
                df['Agendado em'] = pd.to_datetime(df['Agendado em']).dt.tz_convert('America/Sao_Paulo')
                df['Agendado em'] = df['Agendado em'].dt.strftime('%d/%m/%y - %H:%M:%S')
                
                df = df.reindex(["Data agendada", "Horário de início", "Horário de término", "Agendado por:", "Agendado em"],axis=1)
                df['Data agendada'] = pd.to_datetime(df['Data agendada'])
                df['Data agendada'] = df['Data agendada'].dt.strftime('%d/%m/%y')
                df = df.sort_values(by='Horário de início')
                df.set_index('Data agendada', inplace=True)
                st.write(df)
        except Exception as e:
            st.error(str(e))

    def visualizarAgendamentosParaEditar(self,id,data):
        try:
            dados = {
                "id": id,
                "data_agendamento": data
            }
            instanciarAPI = api('VisualizarParaEditar')
            retorno = instanciarAPI.visualizarAgendamentosParaEditar(dados)
            if 'error' in retorno:
                st.error('Você não tem nenhum agendamento feito nesta data...')
            else:
                return retorno
        except Exception as e:
            st.error('Você não tem nenhum agendamento feito nesta data...')
            return False

    def editarAgendamento(self, id,data):
            with st.spinner("Carregando seus agendamentos..."):
                response = self.visualizarAgendamentosParaEditar(id,data)
                if response == False:
                    return
            
            retorno = pd.DataFrame(response)
            retorno = retorno.rename(columns={
                "Gestor":"Nome",
                "data_agendamento":"Data",
                "hora_fim":"Término",
                "hora_inicio":"Inicio",
                "id":"Id"
            })

            # Converta 'Data' para datetime
            retorno['Data'] = pd.to_datetime(retorno['Data'])
            # Agora, você pode usar o método .dt para formatar a coluna 'Data'
            retorno['Data'] = retorno['Data'].dt.strftime('%d/%m/%y')

            retorno = retorno.reindex(["Id", "Nome", "Inicio", "Término", "Data"],axis=1)

            data_inserida_list = retorno["Nome"].tolist()
            nome_formatado = []
            for i in data_inserida_list:
                partes = i.split(" ")
                if partes:
                    Nome = partes[0]
                    nome_formatado.append([Nome])

            nome_formatado_completo = []
            for i in nome_formatado:
                for j in i:
                    nome_formatado_completo.append(j)

            retorno['Nome'] = nome_formatado_completo
            colms = st.columns((1,1,1,1,1,1,1))
            retorno["Excluir"] = ''
            retorno["Alterar"] = ''
            cabecalhos_do_dataframe  = retorno.columns.values.tolist()
            for col,campo_nome in zip(colms,cabecalhos_do_dataframe):
                col.write(campo_nome)

            for index, row in retorno.iterrows():
                col1, col2, col3, col4, col5,col6,col7 = st.columns((1, 1, 1, 1, 1,1,1))
                col1.write(row["Id"])
                col2.write(row["Nome"])
                col3.write(row["Inicio"])
                col4.write(row["Término"])
                col5.write(row["Data"])
                button_space_excluir = col6.empty()
                on_click_excluir = button_space_excluir.button("Excluir",'btnExcluir' + str(row["Id"]))
                button_space_alterar = col7.empty()
                on_click_alterar = button_space_alterar.button("Alterar", 'btnAlterar' + str(row["Id"]))
                id01 = str(row["Id"])

                if on_click_excluir:
                    with st.spinner("Realizando exclusão...."):
                        instanciarBanco = api('ExcluirAgendamento')
                        id = {"id":id01}
                        instanciarBanco.excluirAgendamento(id) 
                        st.rerun()
                
                if on_click_alterar:
                    data_agendamento = str(row["Data"])
                    hora_inicio = str(row["Inicio"])
                    hora_fim = str(row["Término"])
                    id = str(row["Id"])
                    gestor = str(row["Nome"])

                    dados = {"data_agendamento":data_agendamento,
                            "hora_inicio":hora_inicio,
                            "hora_fim":hora_fim,
                            "id":id,
                            "Gestor":gestor}
                    
                    dados = {"data_agendamento":data_agendamento,"hora_inicio":hora_inicio,"hora_fim":hora_fim,"id":id,"gestor":gestor}
                    st.session_state.editar = True
                    st.session_state.dados = dados
                    st.rerun()
        # colunas = st.columns(len(cabecalhos_do_dataframe))

        

        # for i, col in enumerate(colunas):
        #     # Escreva o cabeçalho
        #     col.write(retorno.columns[i])

        #     # Escreva os valores abaixo do cabeçalho
        #     for valor in retorno.iloc[:, i]:
        #         col.write(valor)
        # if 'agenda' not in st.session_state:
        #     st.session_state.agenda = False

        # def visu():
        #     response = self.visualizarAgendamentosParaEditar(id,data)
        #     st.session_state.agenda = response

        # Visualizar = st.button("Visualizar")
        # if Visualizar:
        #     visu()

        # # Converter a resposta para um DataFrame do pandas
        
        # if st.session_state.agenda != False:
        #     response_string = st.session_state.agenda
        #     resposta = json.loads(json.dumps(response_string))

        #     # Criar DataFrame a partir da lista de dicionários
        #     df = pd.DataFrame(resposta, columns=['data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor','id'])
            
        #     # Definir o número de colunas desejado
        #     num_colunas = 1
            
        #     for index in range(len(df)):
        #         st.write(f"Edição para agendamento N° : {index + 1}")
        #         col = st.columns(num_colunas)
        #         novos_valores = []
        #         # Lista para armazenar os novos valores
                
        #         for i, campo_nome in enumerate(df.columns):
        #             chave = f"{index}_{campo_nome}"

        #             if campo_nome == 'hora_inicio' or campo_nome == 'hora_fim':
        #                 novo_valor = col[i % num_colunas].time_input(f"Nova {campo_nome}:", pd.to_datetime(df[campo_nome].iloc[index]).time(), key=chave)
        #             elif campo_nome == 'data_agendamento':
        #                 novo_valor = col[i % num_colunas].date_input(f"Nova {campo_nome}:", pd.to_datetime(df[campo_nome].iloc[index]).date(), key=chave)
        #             elif campo_nome == 'Gestor':
        #                 # Campo do nome do Gestor é desabilitado para edição
        #                 novo_valor = col[i % num_colunas].text_input(f"{campo_nome}:", df[campo_nome].iloc[index], key=chave, disabled=True)
        #             else:
        #                 novo_valor = col[i % num_colunas].text_input(f"{campo_nome} do agendamento:", df[campo_nome].iloc[index], key=chave,disabled=True)


        #             # Adicionar o novo valor à lista
        #             novos_valores.append(novo_valor)

        #         # Botões para confirmar a edição e excluir para cada linha
        #         col1, col2, col3 = st.columns(3)
        #         col1.empty()
        #         with col2:
        #             btn_confirmar = col[0].button(f"Confirmar Edição de N° {index + 1}")
        #             btn_excluir = col[0].button(f"Excluir Edição de N° {index + 1}")

        #         if btn_confirmar:
        #             with st.spinner("Atualizando agendamento...."):
        #                 retorno = self.conflitos2(novos_valores[0], novos_valores[1], novos_valores[2])
        #                 if retorno:
        #                         novos_valores = [
        #                     str(novos_valores[0]),  # Convertendo data para string
        #                     str(novos_valores[1]),  # Convertendo hora_inicio para string
        #                     str(novos_valores[2]),  # Convertendo hora_fim para string
        #                     novos_valores[3],        # Gestor permanece como está (string)
        #                     int(novos_valores[4])    # Convertendo id para inteiro
        #                     ]
        #                         data, count = self.client.table('sala_de_reuniao').update({'data_agendamento': novos_valores[0],
        #                             'hora_inicio': novos_valores[1],
        #                             'hora_fim': novos_valores[2]
        #                         }).eq('id', novos_valores[4]).execute()
        #                         st.success("Agendamento editado com sucesso!")
        #                         visu()
        #                         st.experimental_rerun()
        #                     # Adicione aqui a lógica para confirmar a edição no seu banco de dados
                        
        #         if btn_excluir:
        #                 with st.spinner("Excluindo agendamento..."):
        #                     data, count = self.client.table('sala_de_reuniao').delete().eq('data_agendamento',novos_valores[0]).eq('hora_inicio', novos_valores[1]).eq('hora_fim',novos_valores[2]).execute()
        #                     st.success("Linha excluída com sucesso!")
        #                     visu()
        #                     st.experimental_rerun()
                        
        # else:
        #     st.write("Necessário clicar em visualizar.....")
    
    def opcoes(self):
        print("entrou dentro")
        params = st.experimental_get_query_params()
        today = datetime.today()

        data_agendamento = params["data_agendamento"][0]
        data_agendamento_dt = datetime.strptime(data_agendamento, '%d/%m/%y')        
        hora_inicio = params["hora_inicio"][0]
        hora_fim = params["hora_fim"][0]
        id = params["id"][0]
        Nome = params["gestor"][0]
        st.header("Editar seu agendamento")
        with st.form("sla", clear_on_submit=True):
            # Data do agendamento
            event_date = st.date_input("Selecione a data do agendamento:", value=data_agendamento_dt)

            # Horário de início
            st.write("Horário de Início:")
            hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S').time()
            start_time = st.time_input("Selecione a hora de início:", value=hora_inicio_obj)

            # Horário de término
            st.write("Horário de Término:")
            hora_fim_obj = datetime.strptime(hora_fim, '%H:%M:%S').time()
            end_time = st.time_input("Selecione a hora de término:", value=hora_fim_obj)

            # Nome da pessoa que está agendando
            st.write(f'Pessoa que está editando: {st.session_state.nomeLogado}')
            pessoa = st.session_state.nomeLogado

            if st.form_submit_button("confirmar"):
                # st.experimental_set_query_params()
                # st.session_state.editar = False
                # instanciarapi = api('EditarAgendamento')
                # event_date = datetime.strptime(data_agendamento_dt, '%Y-%m-%d').strftime("%Y-%m-%d")
                # start_time_str = start_time.strftime("%H:%M:%S")
                # end_time_str = end_time.strftime("%H:%M:%S")
                # dados = {"data_agendamento":event_date,"hora_inicio":start_time_str,"hora_fim":end_time_str,"id":id,"Gestor":Nome,"id_gestor":st.session_state.id}
                # st.write(dados)
                # print(dados)
                # return
                st.success("clicou")
                print('clicou')

                






            
