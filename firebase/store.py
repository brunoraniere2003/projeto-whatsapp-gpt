from firebase_admin import firestore

# Função para buscar as últimas mensagens
def get_last_messages(user_phone):
    db = firestore.client()
    messages = db.collection('messages').where('phone', '==', user_phone).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5).stream()
    return [message.to_dict() for message in messages]

# Função para salvar nova mensagem
def save_message(user_phone, user_message, gpt_response):
    db = firestore.client()
    db.collection('messages').add({
        'phone': user_phone,
        'user_message': user_message,
        'gpt_response': gpt_response,
        'timestamp': firestore.SERVER_TIMESTAMP
    })