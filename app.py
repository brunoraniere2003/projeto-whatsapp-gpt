from flask import Flask, jsonify
from flask_cors import CORS
from firebase.firebase_init import initialize_firebase
from firebase.store import save_message
from random import randint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db = initialize_firebase()
print("Conexão com Firebase bem-sucedida!")

@app.route('/')
def hello():
    return "Conexão com Firebase testada com sucesso!"

@app.route('/test-firebase')
def test_firebase():
    try:
        db = initialize_firebase()
        # Teste básico: cria uma coleção de teste
        number = randint(1, 100)
        db.collection('test').add({'numero': number, 'status': 'conectado'})
        return "Conexão com Firebase testada com sucesso! Número salvo: " + str(number)
    except Exception as e:
        return f"Erro ao conectar ao Firebase: {str(e)}"

# Endpoint de teste para salvar mensagem
@app.route('/test-save-message')
def test_save_message():
    user_phone = str(randint(100000000, 999999999))
    user_message = "MENSAGEM DE TESTE"
    gpt_response = "Resposta do GPT"
    
    try:
        save_message(user_phone, user_message, gpt_response)
        return jsonify({"status": "success", "message": "Mensagem salva no NOVOOOO!"}), 200
    except Exception as e:
        print(f"Erro ao salvar mensagem: {e}")  # Log do erro completo
        return jsonify({"status": "error", "message": str(e)}), 500  # Retorna a mensagem do erro

if __name__ == '__main__':
    app.run(port=5000, debug=True)