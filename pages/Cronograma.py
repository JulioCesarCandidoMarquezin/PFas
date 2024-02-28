import streamlit as st
from resources import Crud

def get_all_events():
    with Crud.app.app_context():  # Entre no contexto da aplicação Flask
        return Crud.get_events()

def get_events_by_date(date):
    with Crud.app.app_context():  # Entre no contexto da aplicação Flask
        return Crud.get_events_by_date(date=date)

st.title('Cronograma')

# Obtenha todos os eventos
all_events = get_all_events()

# Selecione a data a partir de um seletor
data_selecionada = st.date_input("Selecione uma data")

if st.button('Todos os eventos'):
    all_events = get_all_events()

    # Exiba todos os eventos
    try:
        events = all_events.json['events']

        if events: 
            st.write('Todos eventos')
            for event in events:
                st.write(f"Título: {event['title']}, Descrição: {event['description']}, Data: {event['date']}")

    except KeyError:
        st.write(f"Nenhum evento programado")

else:
# Verifique se há eventos para a data selecionada
    if data_selecionada:
        # Obtenha os eventos para a data selecionada
        events_for_date = get_events_by_date(date=data_selecionada)
        # Exiba os eventos para a data selecionada
        try:
            events = events_for_date.json['events']

            if events: 
                st.write(f"Eventos em {data_selecionada}:")
                for event in events:
                    st.write(f"Título: {event['title']}, Descrição: {event['description']}, Data: {event['date']}")

        except KeyError:
            st.write(f"Nenhum evento programado para {data_selecionada}")