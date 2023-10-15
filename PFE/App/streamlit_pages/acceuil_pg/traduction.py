# Importer les modules nécessaires
import streamlit as st
from googletrans import Translator, LANGUAGES
from langdetect import detect
from streamlit_pages.acceuil_pg import transcription

def main(session_state):
    db = transcription.get_db()
    st.title("Traduction")
    # Appliquer du style CSS aux zones de texte
    st.markdown("""
        <style>
            textarea {
                border: 2px solid !important;
                border-radius: 8px !important;
                font-size: 16px !important;
                padding: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    # Fonction pour sauvegarder les données dans Firebase
    def save_to_firebase(traduit, original, username):
        # Sauvegarder la traduction dans Firestore
        doc_ref = db.collection("traductions").add({
            "original": original,
            "traduit": traduit,
            "username": username
        })
    # Dictionnaire des langues disponibles, et mise en majuscule de la première lettre
    languages = {value: key for key, value in LANGUAGES.items()}
    capitalized_languages = [lang.capitalize() for lang in languages.keys()]
    to_lang = st.selectbox("Traduire en:", capitalized_languages)

    # Création de deux colonnes pour le texte à traduire et le texte traduit
    col1, col2 = st.columns(2)

    # Zone de texte pour entrer le texte à traduire
    with col1:
        text_to_translate = st.text_area("Entrez le texte que vous souhaitez traduire:", height=250)

    # Fonction pour effectuer la traduction
    def translate_text(from_lang, to_lang):
        translator = Translator()
        translated = translator.translate(text_to_translate, src=from_lang.lower(), dest=languages[to_lang.lower()].lower())
        return translated.text

    # Bouton pour déclencher la traduction
    if st.button("Traduire"):
        if text_to_translate:
            try:
                from_lang = detect(text_to_translate)
            except:
                st.warning("Impossible de détecter la langue. Veuillez réessayer avec un texte plus long.")
                from_lang = 'en'  # Langue par défaut : anglais

            # Appel à la fonction de traduction
            translated_text = translate_text(from_lang, to_lang)

            # Affichage du texte traduit dans la deuxième colonne
            with col2:
                st.text_area("Texte traduit:", value=translated_text, height=250, key="translated_text")
            save_to_firebase(text_to_translate, translated_text,session_state['username'])
        else:
            st.warning("Veuillez entrer du texte à traduire.")
