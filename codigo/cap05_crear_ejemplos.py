# Archivo: cap05_crear_ejemplos.py

from datetime import datetime
import os
from pathlib import Path


def crear_fotos_prueba():
    carpeta = Path.cwd() / "entrada" / "fotos_desordenadas"
    carpeta.mkdir(parents=True, exist_ok=True)

    ejemplos = [
        ("IMG_4829.JPG", (2025, 8, 14, 10, 30)),
        ("DSC_0012.jpg", (2025, 8, 14, 18, 15)),
        ("Screenshot_01.png", (2025, 11, 3, 9, 5)),
        ("WhatsApp_Image.jpeg", (2026, 1, 20, 21, 0)),
        ("nota_suelta.txt", (2026, 1, 20, 21, 5)),
    ]

    for nombre, datos_fecha in ejemplos:
        ruta = carpeta / nombre
        contenido = b"DATOS_SIMULADOS_" + nombre.encode()
        ruta.write_bytes(contenido)
        instante = datetime(*datos_fecha).timestamp()
        os.utime(ruta, (instante, instante))

    print(
        "Creados 5 archivos con fecha fija en "
        "entrada/fotos_desordenadas/"
    )


if __name__ == "__main__":
    crear_fotos_prueba()
