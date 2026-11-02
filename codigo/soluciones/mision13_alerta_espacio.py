# Archivo: mision13_alerta_espacio.py

import json
import os
from pathlib import Path
import shutil
import requests

UMBRAL_LIBRE = 99.0


def medir_disco(ruta):
    uso = shutil.disk_usage(ruta)
    libre_gb = round(uso.free / 1024**3, 2)
    porcentaje = round((uso.free / uso.total) * 100, 1)
    return libre_gb, porcentaje


def enviar_aviso_discord(texto):
    carga = {"username": "Taller Python", "content": texto}
    url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not url:
        print("[MODO PRUEBA] Falta DISCORD_WEBHOOK_URL.")
        print("Se habría enviado este JSON a Discord:")
        print(
            json.dumps(carga, indent=2, ensure_ascii=False)
        )
        return False
    try:
        resp = requests.post(url, json=carga, timeout=10)
        resp.raise_for_status()
        print("[ENVIADO] Alerta entregada a Discord.")
        return True
    except requests.RequestException as err:
        print(f"[ERROR RED] No se pudo enviar: {err}")
        return False


def main():
    libre_gb, porcentaje = medir_disco(Path.cwd())
    print(f"Espacio libre: {libre_gb} GB ({porcentaje} %)")
    if porcentaje >= UMBRAL_LIBRE:
        print("Todo en orden: no hace falta avisar.")
        return
    texto = (
        f"**[Disco casi lleno]** Quedan {libre_gb} GB "
        f"libres ({porcentaje} % del total)."
    )
    enviar_aviso_discord(texto)


if __name__ == "__main__":
    main()
