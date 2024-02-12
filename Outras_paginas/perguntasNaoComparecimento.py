import pandas as pd
import streamlit as st
from datetime import datetime
from supabase import create_client, Client
import io
from PIL import Image
import os
import time
from dotenv import load_dotenv
def OpcoesInformarNaoComparecimento():
    st.info("Ainda em desenvolvimento....")
    st.session_state.informarNaoCompHoraInicio
    data_formatada = st.session_state.informarNaoCompDataAgendada.replace("/", "-")
    # Converter a string para datetime
    hora_inicio_datetime = datetime.strptime(st.session_state.informarNaoCompHoraInicio, "%H:%M:%S")

    # Obter a data atual
    data_atual_e_hora_atual = datetime.now()

    # Formatar a data
    hora_formatada = data_atual_e_hora_atual.strftime("%H:%M:%S")

    # Converter a string formatada para datetime
    hora_formatada_dt = datetime.strptime(hora_formatada, "%H:%M:%S")

    # Calcular a diferença
    diferenca = hora_inicio_datetime - hora_formatada_dt

    # Extrair a diferença apenas em horas
    diferenca_em_horas = abs(diferenca.total_seconds() / 3600)

    # Agora você tem a diferença apenas em horas

    numero_formatado_str = "{:.2f}".format(diferenca_em_horas)
    if hora_formatada_dt < hora_inicio_datetime:
        st.info("A hora atual é menor do que a hora de incio, Potando você não pode informar um não comparecimento.")
        st.session_state.informarNaoComp = False
        st.button("Voltar")
        return
    else:
        pass
    if diferenca_em_horas > 0.25:
        st.info(f'O(A) {st.session_state.informarNaoCompPessoaQueAgendou} agendou a sala com o inicio as {st.session_state.informarNaoCompHoraInicio} resultando uma diferença maior do que 15 minutos, você já pode informar não comparecimento a este Gestor.')
        vazia = st.checkbox("A sala está vazia, e sem nenhum item, como: mochila, notebook etc. Correto?")
        voltar = st.button("Voltar")
        if voltar:
            st.session_state.informarNaoComp = False
            st.rerun()
        if vazia == True:
            image = st.camera_input("Insira uma foto da sala vázia como evidencia: ")
            if image != None:
                # Converter o objeto UploadedFile para uma imagem PIL
                image_pil = Image.open(io.BytesIO(image.read()))

                # Salvar a imagem temporariamente em disco
                path_temporario = "temp_image.jpg"
                image_pil.save(path_temporario)
                button = st.button("Enviar", disabled=False)

                if button:
                    load_dotenv()

                    # Agora você pode acessar suas variáveis de ambiente assim:
                    api_key = os.getenv("API_KEY")
                    database_url = os.getenv("DATABASE_URL")
                    supabase: Client = create_client(database_url, api_key)
                    res = supabase.storage.get_bucket("naoComparecimento")
                    path_on_supastorage = ""

                    with open(path_temporario, 'rb') as f:
                        res = supabase.storage.from_("naoComparecimento").upload(file=f, path=f'{st.session_state.informarNaoCompPessoaQueAgendou} / {data_formatada} / {st.session_state.informarNaoCompHoraInicio}', file_options={"content-type": "image/jpeg"})
                        if res.status_code != 200:
                            st.error("Erro ao fazer o upload da imagem para o banco de dados.")
                        else:
                            st.success("Imagem enviada com sucesso para o banco de dados.")
                            time.sleep(2)
                            st.session_state.informarNaoComp = False
                            st.rerun()

    # else:
    #     st.info(f'A diferença entre O(A) {st.session_state.informarNaoCompPessoaQueAgendou} agendou é menor do que 15m você não pode informar não comparecimento.')
    #     return
    


if __name__ == '__main__':
    OpcoesInformarNaoComparecimento()