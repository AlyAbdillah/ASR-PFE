import streamlit as st
from streamlit_option_menu import option_menu
from firebase_admin import firestore
from streamlit_pages.acceuil_pg import transcription

def page(session_state):
    selected = option_menu(
    menu_title=None,
    options=["Trancription","Traduction"],
    icons=["soundwave","translate","text-paragraph"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    )
    transcription.init()
    if selected == "Trancription":
        # Fonction pour récupérer l'historique de la base de données Firestore
        def fetch_history_from_firebase(db, username):
            transcriptions = db.collection("transcriptions").where("username", "==", username).stream()
            history = []
            for transcription in transcriptions:
                entry = transcription.to_dict()
                history.append(entry)
            return history

        # Fonction pour afficher l'historique dans Streamlit
        def display_history(username, bucket):
            if username:
                db = transcription.get_db()
                history = fetch_history_from_firebase(db, username)
                if not history:
                    st.write("Aucun enregistrement trouvé.")
                for i, entry in enumerate(history):
                    st.write(f"Enregistrement {i+1}")
                    st.text_area("Transcription",value=entry["transcription"], height=250, key= f"Enregistrement {i+1}")

        bucket = transcription.get_bucket()
        display_history(session_state['username'], bucket)
    
    if selected == "Traduction":
        # Fonction pour récupérer l'historique de la base de données Firestore
        def fetch_history_from_firebase(db, username):
            traductions = db.collection("traductions").where("username", "==", username).stream()
            history = []
            for traduction in traductions:
                entry = traduction.to_dict()
                history.append(entry)
            return history
        def display_history(username):
            if username:
                db = transcription.get_db()
                history = fetch_history_from_firebase(db, username)
                if not history:
                    st.write("Aucun traduction trouvé.")
                for i, entry in enumerate(history):
                    st.write(f"Traduction {i+1}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_area("Texte original:", value=entry["original"], height=250, key="text_to_translate"+str(i))
                    with col2:
                        st.text_area("Texte traduit:", value=entry["traduit"], height=250, key="translated_text"+str(i))

        display_history(session_state['username'])