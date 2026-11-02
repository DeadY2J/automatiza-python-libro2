# Archivo: cap14_cliente_ia.py

import os
from pathlib import Path
import requests

URL_API = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/openai/chat/completions"
)
MODELO = "gemini-3.6-flash"
TIMEOUT_SEG = 30


def respuesta_modo_prueba(texto_usuario):
    lineas = [
        lin.strip()
        for lin in texto_usuario.splitlines()
        if lin.strip()
    ]
    muestra = lineas[0] if lineas else "Sin contenido"
    return (
        "- [SIMULADO] Resumen generado en modo prueba.\n"
        f"- Primera línea detectada: {muestra[:50]}\n"
        f"- Longitud analizada: {len(texto_usuario)} "
        "caracteres."
    )


def consultar_ia(
    instruccion_sistema, texto_usuario, max_caracteres=4000
):
    recortado = texto_usuario[:max_caracteres]
    clave = os.getenv("GEMINI_API_KEY", "").strip()

    if not clave:
        print(
            "[MODO PRUEBA] Falta GEMINI_API_KEY. "
            "Usando respuesta simulada."
        )
        return respuesta_modo_prueba(recortado), True

    cabeceras = {
        "Authorization": f"Bearer {clave}",
        "Content-Type": "application/json",
    }
    carga = {
        "model": MODELO,
        "messages": [
            {
                "role": "system",
                "content": instruccion_sistema,
            },
            {"role": "user", "content": recortado},
        ],
        "temperature": 0.2,
    }

    try:
        resp = requests.post(
            URL_API,
            headers=cabeceras,
            json=carga,
            timeout=TIMEOUT_SEG,
        )
        resp.raise_for_status()
        datos = resp.json()
        contenido = (
            datos["choices"][0]["message"]["content"]
        )
        return contenido.strip(), False
    except (
        requests.RequestException,
        KeyError,
        IndexError,
    ) as err:
        print(f"[AVISO API] Fallo en llamada IA: {err}")
        return respuesta_modo_prueba(recortado), True


def main():
    instruccion = (
        "Eres un asistente seco y directo. Resume el "
        "texto del usuario en 3 viñetas cortas en español "
        "indicando las tareas concretas y sus fechas."
    )
    nota_reunion = (
        "Acta rápida del lunes 16 de marzo.\n"
        "1. Hay que renovar el dominio de la web antes del "
        "viernes 20 para que no caduque.\n"
        "2. Lucía revisará las facturas del trimestre el "
        "miércoles por la mañana.\n"
        "3. Queda pendiente comprar dos cables HDMI nuevos "
        "para el monitor del taller."
    )

    print("=" * 54)
    print("CONSULTANDO AL MOTOR DE IA")
    print("=" * 54)

    resultado, es_prueba = consultar_ia(
        instruccion, nota_reunion
    )
    origen = "MODO PRUEBA" if es_prueba else MODELO

    print(f"\nRespuesta recibida ({origen}):\n")
    print(resultado)
    print("\n" + "=" * 54)

    ruta_sal = Path.cwd() / "salida" / "respuesta_ia.md"
    ruta_sal.parent.mkdir(parents=True, exist_ok=True)
    ruta_sal.write_text(resultado + "\n", encoding="utf-8")
    print(f"Guardado en: salida/{ruta_sal.name}")


if __name__ == "__main__":
    main()
