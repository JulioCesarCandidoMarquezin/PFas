import streamlit as st
import requests

def insert_user(name, password):

    api_url = 'http://localhost:5000/auth/register'

    data_to_send = {'name': name, 'password': password}

    response = requests.post(api_url, data=data_to_send)

    message = response.json().get('message')

    return response.status_code == 200, message

# Configuração da página de cadastro

st.title("Página de Cadastro")

nome = st.text_input("Nome")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):
    sucess, message = insert_user(nome, senha)
    if sucess:
        st.success(message)
    else:
        st.error(message)