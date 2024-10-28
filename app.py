from flask import Flask, jsonify, request
from database.database_functions import adicionar_linha_excel

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Servidor Flask funcionando!"})

@app.route('/adicionar', methods=['POST'])
def adicionar():
    dados = request.json
    nome = dados.get("nome")
    numero = dados.get("numero")
    msg_usuario = dados.get("msg_usuario")
    msg_gpt = dados.get("msg_gpt")
    
    adicionar_linha_excel(nome, numero, msg_usuario, msg_gpt)
    return jsonify({"message": "Linha adicionada com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True)