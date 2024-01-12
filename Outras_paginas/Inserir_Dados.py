import streamlit as st
from datetime import datetime
from models.dataBase import SupabaseClient

def main():

    if 'loginValidado' not in st.session_state:
        st.session_state.loginValidado = False
    if st.session_state.loginValidado:
        if st.session_state.logado == True:
            if st.session_state.supervisao == False:
                st.error('Seu perfil não está habilitado para inserir feedbacks')
                return
            else:
                feedback_form()
    else:
        st.header('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                  '&nbsp;&nbsp;****EFETUE LOGIN PARA CONTINUAR****')

def feedback_form():
    if 'motivoMicro' not in st.session_state:
        st.session_state.motivoMicro = False

    # Obter a data e hora atuais
    data_atual = datetime.now()
    data_atual = data_atual.date()
    data_formatada = data_atual.strftime("%Y-%m-%d")
    st.header(f'Olá, {st.session_state.nomeLogado} insira os dados sobre seu feedback aplicado.')
    input_name = st.text_input(label="Insira o nome completo do colaborador que foi aplicado o feedback:")
    # Monitorando a seleção do primeiro selectbox
    motivoMacro = st.selectbox('Motivo MACRO do feedback', ['selecione', 'Feedback Positivo', 'Feedback Construtivo', 'Feedback de Desempenho', 'Feedback de Desenvolvimento Profissional', 'Feedback de Colaboração', 'Feedback de Progresso', 'Feedback de Inovação'])
    # Determinando as opções do segundo selectbox com base na seleção do primeiro

    if motivoMacro == 'Feedback Positivo':
        motivoMicro_opcoes = ['selecione', 'Reconhecimento de conquistas e realizações notáveis.', 'Elogios pelo bom trabalho ou por cumprir metas', 'Destaque para habilidades específicas demonstradas.', 'Feedback de Desenvolvimento Profissional']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback Construtivo':
        motivoMicro_opcoes = ['selecione', 'Sugestões claras para melhoria em áreas específicas.', 'Comparação de resultados atuais com desempenho passado.', 'Destaque para áreas de desempenho excepcional.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback de Desempenho':
        motivoMicro_opcoes = ['selecione', 'Avaliação do desempenho em relação a metas e objetivos.', 'Identificação de oportunidades de desenvolvimento.', 'Apresentação de soluções ou estratégias para superar desafios.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback de Desenvolvimento Profissional':
        motivoMicro_opcoes = ['selecione', 'Recomendações para cursos de treinamento ou workshops.', 'Sugestões de leituras ou recursos educacionais.', 'Identificação de competências a serem aprimoradas.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback de Colaboração':
        motivoMicro_opcoes = ['selecione', 'Reconhecimento de colaboração eficaz com colegas.', 'Destaque para contribuições positivas à equipe.', 'Incentivo à comunicação eficaz e trabalho em equipe.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback de Progresso':
        motivoMicro_opcoes = ['selecione', 'Acompanhamento do progresso em relação a objetivos estabelecidos.', 'Celebração de marcos alcançados ao longo do tempo.', 'Incentivo para manter o foco e a persistência.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    elif motivoMacro == 'Feedback de Inovação':
        motivoMicro_opcoes = ['selecione', 'Reconhecimento de ideias inovadoras ou soluções criativas.', 'Estímulo à geração de novas ideias e abordagens.', 'Valorização da contribuição para a melhoria contínua.']
        motivoMicro = st.selectbox('Motivo do feedback', motivoMicro_opcoes)
        if motivoMicro != 'selecione':
            st.session_state.motivoMicro = True
        else:
            st.session_state.motivoMicro = False
    else:
        st.session_state.motivoMicro = False

    if st.session_state.motivoMicro == True:
        texto_livre = st.text_input(label='Escreva pontos sobre o feedback realizado')


    # Adicionando um botão para acionar a ação
    if st.button("Enviar"):
        if motivoMacro == 'selecione':
            st.error('Selecione um motivo MACRO')
            return
        
        if motivoMicro == 'selecione':
            st.error('Selecione um motivo')
            return
        
        if texto_livre == '' or texto_livre == None:
            st.error('Escreve pelomenos um ponto abordado')
            return
        else:
            if len(texto_livre.strip()) > 20:
                pass
            else:
                st.error('Escreva pelomenos 20 caracteres nos pontos abordados')
                return
        supaBaseInstance = SupabaseClient()
        supaBaseInstance.inserirFeedback(data_formatada,motivoMacro,motivoMicro,texto_livre,st.session_state.id,input_name)


if __name__ == "__main__":
    main()
