# Archivo: cap13_aviso_correo.py

from email.message import EmailMessage
import os
import smtplib


def leer_config_smtp():
    servidor = os.getenv("SMTP_SERVIDOR", "smtp.gmail.com")
    puerto_txt = os.getenv("SMTP_PUERTO", "465")
    usuario = os.getenv("SMTP_USUARIO", "").strip()
    clave = os.getenv("SMTP_CLAVE", "").strip()
    destino = os.getenv("SMTP_DESTINO", "").strip()

    try:
        puerto = int(puerto_txt)
    except ValueError:
        puerto = 465

    return {
        "servidor": servidor,
        "puerto": puerto,
        "usuario": usuario,
        "clave": clave,
        "destino": destino,
    }


def crear_mensaje(remitente, destino, asunto, cuerpo):
    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destino
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    return msg


def enviar_correo(asunto, cuerpo):
    cfg = leer_config_smtp()
    faltan = not (
        cfg["usuario"] and cfg["clave"] and cfg["destino"]
    )

    if faltan:
        rem_sim = cfg["usuario"] or "taller@ejemplo.local"
        dest_sim = cfg["destino"] or "destino@ejemplo.local"
        msg = crear_mensaje(
            rem_sim, dest_sim, asunto, cuerpo
        )
        print("=" * 52)
        print("[MODO PRUEBA] Faltan variables SMTP_*.")
        print("Se habría enviado este correo electrónico:")
        print("=" * 52)
        print(
            f"Servidor: {cfg['servidor']}:{cfg['puerto']}"
        )
        print(f"De:       {msg['From']}")
        print(f"Para:     {msg['To']}")
        print(f"Asunto:   {msg['Subject']}\n")
        print(cuerpo)
        print("=" * 52)
        return False

    msg = crear_mensaje(
        cfg["usuario"], cfg["destino"], asunto, cuerpo
    )
    try:
        with smtplib.SMTP_SSL(
            cfg["servidor"], cfg["puerto"], timeout=10
        ) as smtp:
            smtp.login(cfg["usuario"], cfg["clave"])
            smtp.send_message(msg)
        print(
            "[ENVIADO] Correo entregado a "
            f"{cfg['destino']}."
        )
        return True
    except Exception as err:
        print(f"[ERROR SMTP] Fallo al enviar correo: {err}")
        return False


def main():
    asunto = "Resumen automático del taller"
    cuerpo = (
        "Hola,\n\n"
        "El inventario semanal ha terminado.\n"
        "- Archivos revisados: 7\n"
        "- Espacio recuperable: 4128 bytes\n\n"
        "Un saludo,\nTu script de Python."
    )
    enviar_correo(asunto, cuerpo)


if __name__ == "__main__":
    main()
