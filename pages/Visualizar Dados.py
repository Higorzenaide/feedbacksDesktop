import streamlit as st
from models.dataBase import SupabaseClient
if 'id' not in st.session_state:
    st.session_state.id = None

def main():
    instanceSupa = SupabaseClient()
    instanceSupa.visualizarDadosUser(st.session_state.id)
if __name__ == '__main__':
    main()