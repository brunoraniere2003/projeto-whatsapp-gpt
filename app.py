from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# from firebase.firebase_init import initialize_firebase
# from firebase.store import save_message, get_last_messages
# from gpt_integration.gpt_request import get_gpt_response

app = Flask(__name__)
# CORS(app)

# db = initialize_firebase()
# print("Conexão com Firebase bem-sucedida!")

@app.route('/')
def hello():
    # Teste: Salvar mensagem no Firestore
    # save_message("123456789", "Teste de mensagem", "Resposta do GPT")
    return "Mensagem salva no Firestore!"

# @app.route('/gpt')
# def gpt():
#     response = get_gpt_response("Diga uma raça de cachorro")
#     return response

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     print(request.headers)  # Log dos cabeçalhos recebidos
#     data = request.get_json()
    
#     if not data:
#         print("Nenhum dado recebido")  # Verifica se há dados
#         return jsonify({"error": "Nenhum dado recebido"}), 400
    
#     print(f"Dados recebidos: {data}")  # Log dos dados JSON
    
#     user_phone = data.get('phone')
#     user_message = data.get('message')
    
#     if not user_phone or not user_message:
#         print("Dados incompletos")  # Verifica se os dados são completos
#         return jsonify({"error": "Dados incompletos"}), 400
    
#     gpt_response = get_gpt_response(user_message)
    
#     save_message(user_phone, user_message, gpt_response)
    
#     send_whatsapp_message(user_phone, gpt_response)
    
#     return jsonify({"response": gpt_response}), 200

# def send_whatsapp_message(phone, message):
#     url = "https://api.z-api.io/instances/3D699FAFFEADD094C8E42E5479B6AFF4/token/6797E7BEE32128FFAD4EEF61/send-messages"
#     payload = {
#         "phone": phone,  # Número completo com código de país
#         "message": message
#     }
#     headers = {
#         "Content-Type": "application/json",
#         "Client-Token": "F885b84cd15ed441da1a4395a2aafea14S"  # Adicione o Client-Token aqui
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print(response.status_code)
#     print(response.json())
#     return response.json()

if __name__ == '__main__':
    app.run(port=5000, debug=True)