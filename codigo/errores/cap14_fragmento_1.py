# Fragmento ilustrativo (el programa completo va más abajo)
import os
import requests

url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/openai/chat/completions"
)
clave = os.getenv("GEMINI_API_KEY")

cabeceras = {
    "Authorization": f"Bearer {clave}",
    "Content-Type": "application/json",
}
carga = {
    "model": "gemini-3.6-flash",
    "messages": [
        {
            "role": "system",
            "content": "Responde en 3 viñetas.",
        },
        {"role": "user", "content": "Texto a resumir..."},
    ],
    "temperature": 0.2,
}
resp = requests.post(
    url, headers=cabeceras, json=carga, timeout=30
)
