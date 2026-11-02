# Archivo: mision11_radar_ciudades.py

from pathlib import Path
import time
import requests

URL_METEO = "https://api.open-meteo.com/v1/forecast"
CIUDADES = {
    "Santiago": (42.88, -8.54),
    "Madrid": (40.41, -3.70),
    "Sevilla": (37.38, -5.98),
}
RESPALDO = {"Santiago": 80, "Madrid": 20, "Sevilla": 5}


def datos_simulados(ciudad):
    return {
        "daily": {
            "time": ["2026-03-15", "2026-03-16"],
            "precipitation_probability_max": [
                10,
                RESPALDO[ciudad],
            ],
        }
    }


def consultar(ciudad, lat, lon):
    parametros = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_probability_max",
        "timezone": "Europe/Madrid",
        "forecast_days": 2,
    }
    try:
        resp = requests.get(
            URL_METEO, params=parametros, timeout=10
        )
        resp.raise_for_status()
        return resp.json(), False
    except requests.RequestException:
        print(f"[AVISO RED] {ciudad}: uso datos simulados.")
        return datos_simulados(ciudad), True


def lluvia_manana(datos):
    diario = datos["daily"]
    return diario["precipitation_probability_max"][1]


def main():
    ranking = []
    for num, (ciudad, (lat, lon)) in enumerate(
        CIUDADES.items()
    ):
        if num > 0:
            time.sleep(0.5)
        datos, _ = consultar(ciudad, lat, lon)
        ranking.append((lluvia_manana(datos), ciudad))

    ranking.sort(reverse=True)
    lineas = ["Probabilidad de lluvia para mañana:"]
    for puesto, (prob, ciudad) in enumerate(ranking, 1):
        lineas.append(
            f"  {puesto}. {ciudad:<10} {prob:>3} %"
        )
    lineas.append(
        f"Más papeletas para mojarse: {ranking[0][1]}"
    )
    texto = "\n".join(lineas)
    print("\n" + texto)

    ruta = Path.cwd() / "salida" / "ranking_lluvia.txt"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
