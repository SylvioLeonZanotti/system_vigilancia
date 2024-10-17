from twilio.rest import Client

# Configurações de autenticação da Twilio
account_sid = 'NÃO MEXA'
auth_token = 'NÃO MEXA'
client = Client(account_sid, auth_token)
numero_destino = 'whatsapp:+551999999999'

# Função para enviar alerta via WhatsApp
def enviar_alerta_whatsapp(mensagem, numero_destino):
    try:
        message = client.messages.create(
            from_='whatsapp:+551999999999',  # Número de WhatsApp da Twilio
            body=mensagem,
            to=f'whatsapp:{numero_destino}'  # Número de destino para o WhatsApp
        )
        print(f"Alerta enviado via WhatsApp: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem via WhatsApp: {e}")

# Função para enviar alerta via SMS (opcional)
def enviar_alerta_sms(mensagem, numero_destino):
    try:
        message = client.messages.create(
            from_='+SEU_NUMERO_TWILIO',  # Seu número Twilio
            body=mensagem,
            to=numero_destino  # Número de telefone para receber o SMS
        )
        print(f"Alerta enviado via SMS: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem via SMS: {e}")
