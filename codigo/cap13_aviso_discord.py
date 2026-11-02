# Archivo: cap13_aviso_discord.py

from datetime import datetime
import json
import os
import requests

NOMBRE_BOT = "Taller Python"


def construir_carga(titulo, detalle):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    texto = f"**[{titulo}]** ({ahora})\n{detalle}"
    return {
        "username": NOMBRE_BOT,
        "content": texto,
    }


def enviar_aviso_discord(titulo, detalle):
    carga = construir_carga(titulo, detalle)
    url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

    if not url:
        print("=" * 52)
        print("[MODO PRUEBA] Falta DISCORD_WEBHOOK_URL.")
        print("Se habría enviado este JSON a Discord:")
        print("=" * 52)
        print(
            json.dumps(carga, indent=2, ensure_ascii=False)
        )
        print("=" * 52)
        return False

    try:
        resp = requests.post(url, json=carga, timeout=10)
        resp.raise_for_status()
        print(
            f"[ENVIADO] Aviso '{titulo}' entregado "
            f"(código HTTP {resp.status_code})."
        )
        return True
    except requests.RequestException as err:
        print(
            "[ERROR RED] No se pudo enviar a Discord: "
            f"{err}"
        )
        return False


def main():
    titulo = "Copia de seguridad completada"
    detalle = (
        "Se han respaldado 3 archivos en "
        "backup_2026-03-15.zip sin errores."
    )
    enviar_aviso_discord(titulo, detalle)


if __name__ == "__main__":
    main()
