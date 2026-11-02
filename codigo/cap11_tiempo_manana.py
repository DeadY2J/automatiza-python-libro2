# Archivo: cap11_tiempo_manana.py

import json
from pathlib import Path
import requests

URL_METEO = "https://api.open-meteo.com/v1/forecast"
LATITUD = 42.603
LONGITUD = -8.644


def datos_respaldo():
    return {
        "daily": {
            "time": ["2026-03-15", "2026-03-16"],
            "temperature_2m_max": [18.4, 16.2],
            "temperature_2m_min": [8.1, 9.5],
            "precipitation_probability_max": [15, 75],
        }
    }


def obtener_prevision(lat, lon):
    parametros = {
        "latitude": lat,
        "longitude": lon,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "timezone": "Europe/Madrid",
        "forecast_days": 2,
    }
    try:
        resp = requests.get(
            URL_METEO, params=parametros, timeout=10
        )
        resp.raise_for_status()
        return resp.json(), False
    except requests.RequestException as err:
        print(f"[AVISO RED] No se pudo conectar: {err}")
        print("[MODO PRUEBA] Usando datos simulados.\n")
        return datos_respaldo(), True


def mostrar_y_guardar(datos, simulado):
    diario = datos["daily"]
    fechas = diario["time"]
    maximas = diario["temperature_2m_max"]
    minimas = diario["temperature_2m_min"]
    lluvias = diario["precipitation_probability_max"]

    origen = "SIMULADO" if simulado else "OPEN-METEO"
    print("=" * 52)
    print(f"PREVISIÓN METEOROLÓGICA ({origen})")
    print("=" * 52)

    etiquetas = ["HOY", "MAÑANA"]
    for i, etiq in enumerate(etiquetas):
        fecha = fechas[i]
        t_min = minimas[i]
        t_max = maximas[i]
        prob = lluvias[i]
        aviso = (
            "-> ¡Coge paraguas!"
            if prob >= 50
            else "-> Sin lluvia a la vista"
        )
        print(f"\n[{etiq} - {fecha}]")
        print(f"  Temperatura: {t_min} °C a {t_max} °C")
        print(f"  Lluvia:      {prob} % {aviso}")

    print("\n" + "=" * 52)
    ruta_sal = (
        Path.cwd() / "salida" / "prevision_tiempo.json"
    )
    ruta_sal.parent.mkdir(parents=True, exist_ok=True)
    texto_json = json.dumps(datos, indent=2)
    ruta_sal.write_text(texto_json + "\n", encoding="utf-8")


def main():
    datos, es_simulado = obtener_prevision(
        LATITUD, LONGITUD
    )
    mostrar_y_guardar(datos, es_simulado)


if __name__ == "__main__":
    main()
