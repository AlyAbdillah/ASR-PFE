import os
import datetime
from faster_whisper import WhisperModel
import torch
import streamlit as st
from pytube import YouTube
import firebase_admin
from firebase_admin import credentials, firestore, storage

def init():
    cred = credentials.Certificate("login-2579b-3dd3dc8c16f1.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred, {
    'storageBucket': 'login-2579b.appspot.com'
    })
init()
db = firestore.client()
bucket = storage.bucket()

def get_db():
    return db

def get_bucket():
    return bucket

def transcribe(audio_file):
    #Liste des models possibles 
    model_list = ['tiny','base','small','medium','large','large-v2']
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = WhisperModel(model_list[3], device=device, compute_type="int8")
    """Transcrire le fichier audio en texte."""
    segments, _ = model.transcribe(audio_file, beam_size=5)
    return segments

# Fonction pour sauvegarder les données dans Firebase
def save_to_firebase(audio_file_path, transcription, username):
    # Sauvegarder l'audio dans Firebase Storage
    blob = bucket.blob(f'audio/{username}/{os.path.basename(audio_file_path)}')
    blob.upload_from_filename(audio_file_path)

    # Sauvegarder la transcription dans Firestore
    doc_ref = db.collection("transcriptions").add({
        "transcription": transcription,
        "audio_path": blob.path,
        "username": username
    })

def save_audio_file(audio_bytes, file_extension):
    """Sauvegarde les bytes audio dans un fichier."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name


def transcribe_audio(file_path):
    """Transcrire le fichier audio spécifié."""
    return transcribe(file_path)


def main(session_state):
    """Fonction principale pour exécuter l'application Whisper."""
    st.title("Transcription")

    tab1, tab2 = st.tabs(["Youtube", "Upload audio"])

    # Onglet d'enregistrement audio
    with tab1:
        URL = st.text_input('Entrer le URL YouTube video:')
        if URL == '':
            st.warning("En attente de l'URL.")

        with st.expander('Example URL'):
            st.code('https://www.youtube.com/watch?v=twG4mr6Jov0')

    # Onglet de téléchargement audio
    with tab2:
        audio_file = st.file_uploader("Télécharger un audio", type=["mp3", "mp4", "wav", "m4a"])

    # Action du bouton Transcrire
    if st.button("Transcrire"):
        if URL:
            yt_name=YouTube(URL).title
            yt_file = YouTube(URL).streams.filter(only_audio=True).first().download(filename=yt_name+'.mp3')
            file_name = yt_name+'.mp3'
            segments = transcribe_audio(file_name)
        else:
            file_extension = audio_file.type.split('/')[1]
            audio_file_path = save_audio_file(audio_file.read(), file_extension)
            segments = transcribe_audio(audio_file_path)

        if segments:
            transcript_text = ''
            for segment in segments:
                transcript_text += segment.text + "\n"
            
            st.markdown("""
                        <style>
                            textarea {
                                border-right: 2px solid !important;
                                animation: typing !important;
                                animation-duration: 1.5s !important;
                                animation-timing-function: steps(30, end) !important;
                                animation-fill-mode: forwards !important;
                                font-size: 16px !important;
                                padding: 10px !important;
                            }
                            @keyframes typing {
                            from { width: 0 }
                            to { width: 100% }
                            }

                        </style>
                    """, unsafe_allow_html=True)
            st.text_area("Transcription",value=transcript_text, height=300)
            if URL:
                st.audio(yt_file)
                save_to_firebase(yt_file, transcript_text, session_state['username'] )
            else:
                st.audio(audio_file)
                save_to_firebase(audio_file_path, transcript_text, session_state['username'])
            if st.download_button("Télécharger la transcription", file_name="transcription.docx", data=transcript_text):
                if URL:
                    os.remove(file_name)
                else:
                    os.remove(audio_file_path) 
