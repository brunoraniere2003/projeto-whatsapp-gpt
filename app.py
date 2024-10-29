from flask import Flask, jsonify, request
import requests  # Import para fazer requisições HTTP
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel
from z_api.whatsapp_api import extrair_dados_webhook, enviar_mensagem

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

@app.route('/webhook', methods=['POST'])
def webhook():
    dados = request.json
    
    # Extrai dados
    numero, mensagem = extrair_dados_webhook(dados)
    
    # Verifica se a mensagem é válida
    if mensagem == "Mensagem de grupo ignorada":
        return jsonify({"status": mensagem}), 200
    if not numero:
        return jsonify({"error": "Número de telefone ausente"}), 400
    if not mensagem:
        return jsonify({"error": "Mensagem de texto ausente"}), 400

    # Envia a mensagem de volta
    resultado = enviar_mensagem(numero, mensagem)
    return jsonify(resultado), 200 if "status" in resultado else 500

if __name__ == '__main__':
    app.run(debug=True)