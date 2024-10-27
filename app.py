from flask import Flask
from flask_cors import CORS
from firebase.firebase_init import initialize_firebase

app = Flask(__name__)
CORS(app)

# Tenta conectar ao Firebase
db = initialize_firebase()
print("Conexão com Firebase bem-sucedida!")

@app.route('/')
def hello():
    return "Conexão com Firebase testada com sucesso!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)