import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

def initialize_firebase():
    load_dotenv()  # Carrega o .env

    # Teste para verificar se a variável foi carregada
    print("Caminho do Firebase Credentials:", os.getenv('FIREBASE_CREDENTIALS'))
    
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    return db