import streamlit as st
import requests
def login(name, password):

    api_url = 'http://localhost:5000/auth/login'
    
    data_to_send = {'name': name, 'password': password}

    response = requests.post(api_url, data=data_to_send)

    return response.status_code == 200

# Configuração da página de login
st.title("Página de Login")

name = st.text_input("name")
password = st.text_input("password", type="password")

if st.button("Login"):
    if login(name, password):
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha inválidos.")