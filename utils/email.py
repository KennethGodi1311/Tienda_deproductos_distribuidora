import smtplib
from email.mime.text import MIMEText

def enviar_codigo(correo_destino, codigo):

    remitente = "TU_CORREO@gmail.com"
    password = "TU_APP_PASSWORD"  # 🔥 NO TU PASSWORD NORMAL

    mensaje = MIMEText(f"Tu código de recuperación es: {codigo}")
    mensaje["Subject"] = "Recuperación de contraseña"
    mensaje["From"] = remitente
    mensaje["To"] = correo_destino

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(mensaje)
        servidor.quit()
        return True
    except Exception as e:
        print(e)
        return False