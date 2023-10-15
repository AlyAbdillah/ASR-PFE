# Importation des bibliothèques nécessaires
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_pages import acceuil, utilisateur, historique

# Fonction principale de l'application
def app(session_state):
    # Création du menu latéral (sidebar)
    with st.sidebar:
        # Création d'un menu déroulant avec des icônes pour chaque option
        # Le menu permet de naviguer entre différentes pages
        selected = option_menu(None, ['Acceuil', 'Utilisateur', 'Historique'], 
            icons=['house', 'person', 'clock-history'], menu_icon="cast", default_index=0,)

    # Affiche la page d'accueil si l'option 'Acceuil' est sélectionnée
    if selected == 'Acceuil':
        acceuil.page(session_state)

    # Affiche la page utilisateur si l'option 'Utilisateur' est sélectionnée
    if selected == 'Utilisateur':
        utilisateur.page(session_state)
        
    # Affiche la page d'historique si l'option 'Historique' est sélectionnée
    if selected == 'Historique':
        historique.page(session_state)
