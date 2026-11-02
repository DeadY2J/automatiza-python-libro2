# Archivo: mision17_lector_json_robusto.py

import json
import logging
from pathlib import Path

BASE = Path(__file__).resolve().parent
CLAVES = ["latitud", "longitud", "max_copias"]


def cargar_json_seguro(ruta_json, claves_obligatorias):
    try:
        texto = ruta_json.read_text(encoding="utf-8")
        datos = json.loads(texto)
    except json.JSONDecodeError as err:
        logging.error(
            "%s: JSON roto (%s)", ruta_json.name, err
        )
        return None
    except OSError as err:
        logging.error(
            "%s: no se pudo leer (%s)",
            ruta_json.name,
            err.strerror,
        )
        return None

    if not isinstance(datos, dict):
        logging.error(
            "%s: no es un diccionario", ruta_json.name
        )
        return None
    faltan = [
        k for k in claves_obligatorias if k not in datos
    ]
    if faltan:
        logging.error(
            "%s: faltan claves %s",
            ruta_json.name,
            ", ".join(faltan),
        )
        return None
    logging.info("%s: correcto", ruta_json.name)
    return datos


def crear_pruebas(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    muestras = {
        "valido.json": '{"latitud": 42.6, "longitud": '
        '-8.6, "max_copias": 3}\n',
        "roto.json": '{"latitud": 42.6, "longitud": -8.6\n',
        "incompleto.json": '{"latitud": 42.6}\n',
    }
    for nombre, texto in muestras.items():
        (carpeta / nombre).write_text(
            texto, encoding="utf-8", newline="\n"
        )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    carpeta = BASE / "entrada" / "jsons_prueba"
    crear_pruebas(carpeta)
    nombres = [
        "valido.json",
        "roto.json",
        "incompleto.json",
        "no_existe.json",
    ]
    validos = 0
    for nombre in nombres:
        datos = cargar_json_seguro(carpeta / nombre, CLAVES)
        if datos is not None:
            validos += 1
    print(f"Válidos: {validos} de {len(nombres)}")


def test_cargar_json_seguro(tmp_path):
    crear_pruebas(tmp_path)
    ok = cargar_json_seguro(
        tmp_path / "valido.json", CLAVES
    )
    assert ok["max_copias"] == 3
    malos = ["roto.json", "incompleto.json", "x.json"]
    for nombre in malos:
        ruta = tmp_path / nombre
        assert cargar_json_seguro(ruta, CLAVES) is None


if __name__ == "__main__":
    main()
