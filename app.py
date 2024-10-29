from flask import Flask, jsonify, request
import requests  # Import para fazer requisições HTTP
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel, enviar_mensagem_whatsapp

app = Flask(__name__)

# Configurações da Z-API
ZAPI_URL = "https://api.z-api.io/instances/3D699FAFFEADD094C8E42E5479B6AFF4/token/6797E7BEE32128FFAD4EEF61/send-text"
CLIENT_TOKEN = "F885b84cd15ed441da1a4395a2aafea14S"

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

@app.route('/ver-registros', methods=['GET'])
def ver_registros():
    try:
        registros = visualizar_registros_excel()
        return jsonify(registros), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.json
    numero = dados.get("numero")
    mensagem = dados.get("mensagem")
    
    resultado = enviar_mensagem_whatsapp(numero, mensagem)
    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True)