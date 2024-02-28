import streamlit as st

st.title('Exposição das Fotos')
st.divider()

tab5, tab6, tab7, tab8 = st.tabs(["CINEAFRO", "Roda de conversa", "Oficina de Argila", 'Mural'])

with tab5:
    st.header('CINEAFRO')

    from pages.Cineafro import carousel
    
with tab6:
    st.header('Roda de conversa')
    
with tab7:
    st.header('Oficina de Argila')
    

with tab8:
    st.header('Mural')