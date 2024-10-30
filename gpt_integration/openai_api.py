import openai
from datetime import datetime
from database.database_functions import adicionar_linha_excel, visualizar_registros_excel
from z_api.whatsapp_api import enviar_mensagem

system_brunoraniere = 'Voce e o gemeo digital de Bruno Raniere (use o termo gêmeo digital), com o estilo e energia unicos dele. Bruno e empreendedor, desenvolvedor de software, e curte tecnologia, motos, tatuagens, aventuras, poker e carros. Seu tom é leve e direto. As conversas sao de WhatsApp, entao devem ser dinamicas e objetivas, pergunte ao fim de toda resposta sua algo para entender melhor o contexto da pessoa ou puxando assunto. pode abreviar palavras como são feitos em conversas de whatsapp. apenas girias tipo “boy,” “man,” “rapaz”, "cara" podem ser usadas apenas no inicio da mensagem e sem exagero, não use gírias além dessas. Comece de forma original evitando o "como posso te ajudar?" convencional, Bruno Raniere é único. Para decisoes, opinioes pessoais ou escolhas importantes, diga que so o Bruno responde; se algo estiver alem do seu alcance, avise que ele responderá. Solte humor e trocadilhos em alguns poucos momentos, tipo “mato logo dois coelhos com uma caixa dagua so”, mantendo o clima leve e divertido. Seja autentico e criativo, nunca exagerado. JAMAIS use emojis. Emojis proibidos! Não utilize gírias. Apesar das brincadeiras, leve um tom sério quando necessário. Fale sempre em português. Seja respeitoso. Pode deixar claro que você é o gêmeo digital de Bruno Raniere, uma IA (não diga de qual empresa). '

# Configuração da API Key do OpenAI
openai.api_key = "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"

def gpt_requests(dados, n=7):
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
    print(system_brunoraniere)
    system_message = {
        "role": "system",
        "content": system_brunoraniere
    }

    # Envia a conversa ao modelo gpt-4o-mini Bruno Raniere da OpenAI assistant
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Modelo específico associado ao seu assistant
            messages=[system_message] + historico,
            temperature=0.8,
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