# Archivo: cap11_ficha_pokemon.py

import sys
import requests

URL_POKE = "https://pokeapi.co/api/v2/pokemon/"


def respaldo_pikachu():
    return {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60,
        "types": [{"type": {"name": "electric"}}],
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp"}},
            {"base_stat": 55, "stat": {"name": "attack"}},
            {"base_stat": 40, "stat": {"name": "defense"}},
            {
                "base_stat": 50,
                "stat": {"name": "special-attack"},
            },
            {
                "base_stat": 50,
                "stat": {"name": "special-defense"},
            },
            {"base_stat": 90, "stat": {"name": "speed"}},
        ],
    }


def consultar_pokemon(nombre_o_id):
    limpio = str(nombre_o_id).strip().lower()
    url = f"{URL_POKE}{limpio}"
    cabeceras = {"User-Agent": "TallerPythonLibro2/1.0"}
    try:
        resp = requests.get(
            url, headers=cabeceras, timeout=10
        )
        resp.raise_for_status()
        return resp.json(), False
    except requests.RequestException as err:
        print(f"[AVISO RED] Fallo al consultar API: {err}")
        print(
            "[MODO PRUEBA] Mostrando ficha de respaldo.\n"
        )
        return respaldo_pikachu(), True


def mostrar_ficha(datos):
    num = datos["id"]
    nombre = datos["name"].capitalize()
    altura_m = datos["height"] / 10
    peso_kg = datos["weight"] / 10

    tipos = [
        t["type"]["name"] for t in datos.get("types", [])
    ]
    txt_tipos = ", ".join(tipos)

    print("=" * 46)
    print(f"FICHA #{num:03d}: {nombre.upper()}")
    print("=" * 46)
    print(f"  Tipos:   {txt_tipos}")
    print(f"  Altura:  {altura_m} m")
    print(f"  Peso:    {peso_kg} kg")
    print("  Estadísticas base:")
    for item in datos.get("stats", []):
        nom_stat = item["stat"]["name"]
        valor = item["base_stat"]
        print(f"    - {nom_stat:<16}: {valor}")
    print("=" * 46)


def main():
    objetivo = "pikachu"
    if len(sys.argv) > 1:
        objetivo = sys.argv[1]
    datos, _ = consultar_pokemon(objetivo)
    mostrar_ficha(datos)


if __name__ == "__main__":
    main()
