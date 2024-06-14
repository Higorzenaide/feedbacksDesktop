
import streamlit as st
from Outras_paginas.Inserir_Dados import main as mainInserirDados
from Outras_paginas.Visualizar_Dados import main as mainVisualizarDados
from models.funcoes import configuracoesIniciais,logout,definirVariaveisDaSessao,local_css,menuHorizontalSalaDeReuniao,efetuarLogin
from Outras_paginas.editar_agendamento_sala import main as mainEditarAgendamentoSala
from Outras_paginas.visualizar_agendamento_sala import main as mainVisualizarAgendamentoSala
import calendar
from models.dataBase import SupabaseClient
from datetime import datetime, time, timedelta
import json
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def main():

    #Header da pagina
    imagem_url = "images/REUNIAO.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

    st.write("O site da sala de reunião foi migrado para o site 'https://gestao-cop.vercel.app/sala_reuniao'")
    return
    
    # Obter o ano e o mês atual
    today = datetime.today()
    year = st.number_input("Digite o ano:", int(today.year - 1), int(today.year + 1), today.year)
    month = st.number_input("Digite o mês:", 1, 12, today.month)

    # Criar o objeto de calendário para o mês e ano fornecidos
    cal = calendar.monthcalendar(year, month)

    # Criar o cabeçalho do calendário
    header = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]

    # Iniciar o layout da tabela
    table = "<table style='width:100%'><tr>"

    # Adicionar o cabeçalho à tabela
    for day in header:
        table += f"<th>{day}</th>"
    table += "</tr>"

    # Adicionar os dias do mês à tabela
    for week in cal:
        table += "<tr>"
        for day in week:
            if day == 0:
                table += "<td></td>"
            else:
                table += f"<td>{day}</td>"
        table += "</tr>"

    # Fechar a tabela
    table += "</table>"

    # Exibir a tabela no Streamlit
    st.markdown(table, unsafe_allow_html=True)

   # Definindo estilo para o cabeçalho
    st.markdown(
        """
        <style>
            .header-text {
                font-size: 24px;
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Agendar Sala de Reunião - Coluna 1
    st.markdown('<p class="header-text">Agendar Sala de Reunião</p>', unsafe_allow_html=True)

    # Data do agendamento
    event_date = st.date_input("Selecione a data do agendamento:")

    #Horario de inicio
    st.write("Horário de Início:")
    start_time = st.time_input("Selecione a hora de início:", time(today.hour, today.minute))

    #Horario de termino
    st.write("Horário de Término:")
    end_time = st.time_input("Selecione a hora de término:", time((today.hour + 1) % 24, today.minute))

    #Nome da pessoa que está agendando
    st.write(f'Pessoa que está agendando: {st.session_state.nomeLogado}')
    pessoa = st.session_state.nomeLogado

    #Botão agendar
    agendar = st.button("Agendar")

    #Instanciando o SupaBase
    instanciarSupaBase = SupabaseClient()

    if agendar:
        data_atual = event_date
        data_formatada = data_atual.strftime("%Y-%m-%d")
        start_time_str = start_time.strftime("%H:%M:%S")
        end_time_str = end_time.strftime("%H:%M:%S")
        
        # Criar um dicionário com os dados
        dados_agendamento = {
            "data": data_formatada,
            "hora_inicio": start_time_str,
            "hora_termino": end_time_str,
            "id_usuario": st.session_state.id,
            "Gestor":pessoa
        }

        # Serializar o dicionário para JSON
        dados_agendamento_json = json.dumps(dados_agendamento)

        # Passar o JSON para a função
        retorno = instanciarSupaBase.inserirAgendamentoSalaReuniao(dados_agendamento_json)
        
        with st.spinner("Gerando PDF..."):
            if retorno:
                # Gerar PDF
                pdf_stream = BytesIO()
                pdf = SimpleDocTemplate(pdf_stream, pagesize=letter)

                # Lista para armazenar os elementos do PDF
                elementos_pdf = []

                # Adicionar conteúdo ao PDF
                elementos_pdf.append(Paragraph("Relatório de Agendamento", getSampleStyleSheet()['Title']))
                elementos_pdf.append(Spacer(1, 12))

                # Adicionar imagem ao PDF (substitua "caminho_para_sua_imagem.png" pelo caminho real da sua imagem)
                imagem_path = "images/AGENDAMENTOREALIZADO.png"
                elementos_pdf.append(Image(imagem_path, width=4*inch, height=1*inch))
                elementos_pdf.append(Spacer(1, 30))
                elementos_pdf.append(Paragraph(f"Data: {data_formatada}", getSampleStyleSheet()['Normal']))
                elementos_pdf.append(Spacer(1, 15))
                elementos_pdf.append(Paragraph(f"Hora de Início: {start_time_str}", getSampleStyleSheet()['Normal']))
                elementos_pdf.append(Spacer(1, 15))
                elementos_pdf.append(Paragraph(f"Hora de Término: {end_time_str}", getSampleStyleSheet()['Normal']))
                elementos_pdf.append(Spacer(1, 15))
                elementos_pdf.append(Paragraph(f"Pessoa que está agendando: {pessoa}", getSampleStyleSheet()['Normal']))

                # Adicione mais informações ou imagens conforme necessário

                # Construir o PDF
                pdf.build(elementos_pdf)

                # Download do PDF
                st.markdown("### Download do PDF:")
                st.markdown(f"[Clique aqui se quiser baixar o pdf do agendamento](data:application/pdf;base64,{base64.b64encode(pdf_stream.getvalue()).decode()})", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
