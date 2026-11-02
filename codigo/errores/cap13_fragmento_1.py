# Fragmento ilustrativo (el programa completo va más abajo)
import os

url_webhook = os.getenv("DISCORD_WEBHOOK_URL")
if not url_webhook:
    print("[MODO PRUEBA] Falta DISCORD_WEBHOOK_URL.")
