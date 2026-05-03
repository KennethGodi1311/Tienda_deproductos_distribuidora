from twilio.rest import Client

# 🔥 TUS CREDENCIALES
ACCOUNT_SID = "TU_SID"
AUTH_TOKEN = "TU_TOKEN"
TWILIO_PHONE = "+1234567890"  # número Twilio

def enviar_sms(numero, codigo):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body=f"Tu código de recuperación es: {codigo}",
            from_=TWILIO_PHONE,
            to=numero  # Ej: +50688888888
        )

        return True

    except Exception as e:
        print(e)
        return False