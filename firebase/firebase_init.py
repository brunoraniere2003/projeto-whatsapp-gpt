import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

def initialize_firebase():
    load_dotenv()  # Carrega o .env

    # Verifica se o Firebase já foi inicializado
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db