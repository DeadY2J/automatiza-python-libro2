# Fragmento ilustrativo (el programa completo va más abajo)
import requests

url = "https://api.open-meteo.com/v1/forecast"
parametros = {
    "latitude": 42.60,
    "longitude": -8.64,
    "daily": (
        "temperature_2m_max,"
        "precipitation_probability_max"
    ),
    "timezone": "auto",
}

respuesta = requests.get(url, params=parametros, timeout=10)
respuesta.raise_for_status()
datos = respuesta.json()
