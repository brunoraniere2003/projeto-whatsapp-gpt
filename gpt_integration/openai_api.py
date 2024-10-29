import openai
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
        if registro[1] == telefone:
            historico.append({"role": "user", "content": registro[2]})
            historico.append({"role": "assistant", "content": registro[3]})

    # Adiciona a nova mensagem do usuário
    historico.append({"role": "user", "content": msg_usuario})

    # Mensagem de contexto para o GPT
    system_message = {
        "role": "system",
        "content": "Você está conversando com um usuário, responda de forma útil e direta. Não ultrapasse 15 tokens."
    }

    # Envia a conversa ao modelo GPT-3.5
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message] + historico
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