from flask import Flask, jsonify, request
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel
from z_api.whatsapp_api import extrair_dados_webhook, enviar_mensagem
from gpt_integration.openai_api import gpt_requests  # Função para interagir com o GPT e responder via WhatsApp

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
    
    # Extrai número e mensagem do webhook
    numero, mensagem = extrair_dados_webhook(dados)
    
    # Verifica se a mensagem é válida
    if mensagem == "Mensagem de grupo ignorada":
        return jsonify({"status": mensagem}), 200
    if not numero:
        return jsonify({"error": "Número de telefone ausente"}), 400
    if not mensagem:
        return jsonify({"error": "Mensagem de texto ausente"}), 400

    # Processa a mensagem com o GPT e envia resposta ao usuário
    response = gpt_requests(dados, n=5)  # Envia a mensagem e o histórico para o GPT
    
    # Retorna resultado da operação
    return jsonify(response), 200 if "status" in response else 500

if __name__ == '__main__':
    app.run(debug=True)