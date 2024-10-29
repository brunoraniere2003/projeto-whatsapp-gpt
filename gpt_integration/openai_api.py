import openai
# from assistants import assistant_brunoraniere
from datetime import datetime
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel
from z_api.whatsapp_api import enviar_mensagem

# Configuração da API Key do OpenAI
openai.api_key = "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"

def gpt_requests(dados, n=5):
    """
    Recebe dados do webhook, consulta as últimas `n` linhas no Excel,
    compila as interações e envia para o modelo GPT da OpenAI.
    """
    # Extrair informações do webhook
    nome = dados.get("senderName")
    telefone = dados.get("phone")
    msg_usuario = dados.get("text", {}).get("message")
    
    # Validação inicial
    if not telefone or not msg_usuario:
        print("Dados insuficientes para continuar o processamento.")
        return {"error": "Dados insuficientes para continuar o processamento."}

    # Consulta as últimas `n` linhas do Excel
    print(visualizar_registros_excel()[-n:])
    registros = visualizar_registros_excel()[-n:]

    # Compila o histórico de mensagens
    historico = []
    for registro in registros:
        # Assume que cada registro contém (nome, telefone, msg_usuario, msg_gpt, hora)
        if registro['numero'] == telefone:
            historico.append({"role": "user", "content": registro['msg_usuario']})
            historico.append({"role": "assistant", "content": registro['msg_gpt']})

    # Adiciona a nova mensagem do usuário
    historico.append({"role": "user", "content": msg_usuario})

    # Mensagem de contexto para o GPT
    # system_brunoraniere = assistant_brunoraniere()
    system_message = {
        "role": "system",
        "content": "Você é um assistant virtual que simula a personalidade de Bruno Raniere."
    }

    # Envia a conversa ao modelo gpt-4o-mini Bruno Raniere da OpenAI assistant
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Modelo específico associado ao seu assistant
            messages=[system_message] + historico,
            # temperature=1.5,       # Mais criatividade nas respostas
            # max_tokens=100          # Limite de tokens para respostas curtas e objetivas
        )   
        msg_gpt = response['choices'][0]['message']['content']

        # Adiciona a resposta ao Excel
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        adicionar_linha_excel(nome, telefone, msg_usuario, msg_gpt, hora)

        # Envia a resposta para o WhatsApp via Z-API
        enviar_mensagem(telefone, msg_gpt)

        print("Resposta do GPT:", msg_gpt)
        return {"status": "Mensagem enviada com sucesso", "resposta": msg_gpt}

    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        return {"error": str(e)}