import streamlit as st

def page(session_state):
    
    st.title("Informations personnelles")

    # Afficher des informations personnelles
    if st.button("Afficher les informations"):
        st.write(f"Nom complet : {session_state['username']}")
        st.write(f"Email : {session_state['useremail']}")
        # ... d'autres champs à affiche
    