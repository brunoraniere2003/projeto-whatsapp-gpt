import requests

# Configurações da Z-API
ZAPI_URL = "https://api.z-api.io/instances/3D699FAFFEADD094C8E42E5479B6AFF4/token/6797E7BEE32128FFAD4EEF61/send-text"
CLIENT_TOKEN = "F885b84cd15ed441da1a4395a2aafea14S"

def extrair_dados_webhook(dados):
    """
    Extrai o número e a mensagem do payload do webhook.
    Retorna o número e a mensagem.
    """
    is_group = dados.get("isGroup", True)
    if is_group:
        return None, "Mensagem de grupo ignorada"
    
    numero = dados.get("phone")
    mensagem = dados.get("text", {}).get("message")
    print("Número:", numero, "Mensagem:", mensagem)
    return numero, mensagem

def enviar_mensagem(numero, mensagem):
    """
    Envia uma mensagem para o número especificado usando a Z-API.
    Retorna o status da resposta.
    """
    headers = {
        "Content-Type": "application/json",
        "client-token": CLIENT_TOKEN
    }
    payload = {
        "phone": numero,
        "message": mensagem
    }
    resposta = requests.post(ZAPI_URL, headers=headers, json=payload)
    
    if resposta.status_code == 200:
        return {"status": "Mensagem enviada com sucesso"}
    else:
        return {"error": "Erro ao enviar mensagem", "status_code": resposta.status_code}