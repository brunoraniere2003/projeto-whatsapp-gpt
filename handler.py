import json

def lambda_handler(event, context):
    # Processa o evento recebido
    print("Evento recebido:", event)
    
    # Lógica de processamento vai aqui
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processado com sucesso!')
    }
