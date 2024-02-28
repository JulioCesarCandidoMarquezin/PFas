import streamlit as st

# Exiba o conteúdo HTML no Streamlit
def carousel():
    # Leia o conteúdo do arquivo HTML
    with open('resources/carrossel/carrossel.html', "r", encoding='utf-8') as file:
        html_content = file.read()

    with open('resources/carrossel/carrossel.css', "r", encoding='utf-8') as file:
        css_content = file.read()

    with open('resources/carrossel/carrossel.js', "r", encoding='utf-8') as file:
        js_content = file.read()

    return st.components.v1.html(
        html_content + f"<style>{css_content}</style><script>{js_content}</script>",
        scrolling=True,
        height=800
    )

carousel()