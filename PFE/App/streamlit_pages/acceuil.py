import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_pages.acceuil_pg import transcription,traduction

def page(session_state):
    selected = option_menu(
    menu_title=None,
    options=["Trancription","Traduction"],
    icons=["soundwave","translate","text-paragraph"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    )

    if selected == "Trancription":
        transcription.main(session_state)
    if selected == "Traduction":
        traduction.main(session_state)