from flask import Flask, jsonify, request
import requests  # Import para fazer requisições HTTP
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel

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

    # Verifica se a mensagem é de um grupo
    is_group = dados.get("isGroup", True)
    if is_group:
        return jsonify({"status": "Mensagem de grupo ignorada"}), 200

    # Extrai número e mensagem
    numero = dados.get("phone", {}).get("text")
    mensagem = dados.get("message", {}).get("text")
    print("Número:", numero, "Mensagem:", mensagem)

    # Valida dados
    if not numero:
        return jsonify({"error": "Número de telefone ausente"}), 401
    if not mensagem:
        return jsonify({"error": "Mensagem de texto ausente"}), 400

    # Envia a mesma mensagem de volta
    headers = {
        "Content-Type": "application/json",
        "client-token": CLIENT_TOKEN
    }
    payload = {
        "phone": numero,
        "message": mensagem
    }
    resposta = requests.post(ZAPI_URL, headers=headers, json=payload)

    # Retorna o resultado do envio
    if resposta.status_code == 200:
        return jsonify({"status": "Mensagem enviada com sucesso"}), 200
    else:
        return jsonify({"error": "Erro ao enviar mensagem"}), 500

if __name__ == '__main__':
    app.run(debug=True)