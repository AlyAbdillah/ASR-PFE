# Importation des bibliothèques et modules nécessaires
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json
import main
from streamlit_option_menu import option_menu

# Clé de l'API Firebase
API_KEY = " AIzaSyADuN0g7FyrFAFparKM2-zJxlOfoKiqLQk "

# Fonction pour initialiser Firebase
def init_firebase():
    cred = credentials.Certificate("login-2579b-3dd3dc8c16f1.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

# Fonction pour authentifier un utilisateur
def authenticate(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    return r.json()

# Fonction principale de l'application
def app():
    # Initialisation de Firebase
    init_firebase()

    # Initialisation de l'état de session si ce n'est pas déjà fait
    if 'session_state' not in st.session_state:
        st.session_state.session_state = {"username": "", "useremail": "", "signout": False, "signedout": False}

    session_state = st.session_state.session_state

    # Fonction pour se connecter
    def connexion():
        data = authenticate(email, password)
        if "localId" in data:
            session_state["username"] = data["localId"]
            session_state["useremail"] = email
            session_state["signout"] = True
            session_state["signedout"] = True
        else:
            st.warning("Échec de la connexion.")

    # Fonction pour se déconnecter
    def deconnexion():
        session_state["signout"] = False
        session_state["signedout"] = False
        session_state["username"] = ""

    # Écran de connexion et d'inscription
    if not session_state['signedout']:
        choice = option_menu(None, ["Se connecter", "S'inscrire"], 
        icons=[], 
        menu_icon="cast", default_index=0, orientation="horizontal")

        if choice == "Se connecter":
            email = st.text_input("Adresse Email")
            password = st.text_input("Mot de passe", type="password")
            st.button("Se connecter",on_click=connexion)
        else:
            username = st.text_input("Nom d'utilisateur")
            email = st.text_input("Adresse Email")
            password = st.text_input("Mot de passe", type="password")
            if len(password) < 6:
                st.warning("Le mot de passe doit comporter au moins 6 caractères.")
            else:
                if st.button("S'inscrire"):
                    try:
                        user = auth.create_user(email=email, password=password,uid=username)
                        st.success("Compte créé avec succès.")
                        st.markdown('Connectez-vous avec votre email et mot de passe.')
                    except Exception as e:
                        st.warning(f"Erreur lors de la création du compte: {e}")

    # Si l'utilisateur est connecté
    if session_state['signout']:
        main.app(session_state)
        st.sidebar.button("Déconnexion",on_click=deconnexion)

if __name__ == "__main__":
    app()
