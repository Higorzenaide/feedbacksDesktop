import streamlit as st
from models.dataBase import SupabaseClient
from models.funcoes import efetuarLogin
import streamlit as st


def main():
    imagem_url = "images/desenvolvimento1.png"  # Substitua pela URL da sua imagem
    st.image(imagem_url, use_column_width=True)

    instanciarSupa = SupabaseClient()

    if st.session_state.logado == False:
        efetuarLogin()
        return
    #Selecionar a data que deseja visualizar
    event_date = st.date_input("Selecione a data que deseje editar o agendamento:")

    #Formatando a data
    data_atual = event_date
    data_formatada = data_atual.strftime("%Y-%m-%d")
    retorno = instanciarSupa.editarAgendamento(st.session_state.id,data_formatada)
    if retorno:
        return True
if __name__ == '__main__':
    main()