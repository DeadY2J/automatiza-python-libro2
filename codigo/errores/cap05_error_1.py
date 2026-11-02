# ERROR A PROPÓSITO
from pathlib import Path

archivos = [Path("IMG_1.JPG"), Path("foto_2.jpg")]
for indice, archivo in enumerate(archivos, start=1):
    if archivo.suffix in [".jpg", ".png"]:
        nuevo = f"2025-08-14_{indice:03d}{archivo.suffix}"
        print(nuevo)
