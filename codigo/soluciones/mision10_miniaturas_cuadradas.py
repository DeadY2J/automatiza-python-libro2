# Archivo: mision10_miniaturas_cuadradas.py

from pathlib import Path
from PIL import Image, ImageOps

LADO = 200
EXTENSIONES = {".png", ".jpg", ".jpeg"}


def crear_miniatura(ruta, carpeta_dest):
    with Image.open(ruta) as img:
        copia = img.convert("RGB")
    cuadrada = ImageOps.fit(copia, (LADO, LADO))
    destino = carpeta_dest / f"thumb_{ruta.stem}.jpg"
    cuadrada.save(destino, "JPEG", quality=85)
    return destino, copia.size, cuadrada.size


def main():
    raiz = Path.cwd()
    origen = raiz / "entrada" / "imagenes_bruto"
    destino = raiz / "salida" / "miniaturas"
    imagenes = []
    if origen.exists():
        imagenes = [
            p
            for p in sorted(origen.iterdir())
            if p.suffix.lower() in EXTENSIONES
        ]
    if not imagenes:
        print(
            "No hay imágenes en entrada/imagenes_bruto. "
            "Ejecuta antes cap10_crear_ejemplos.py"
        )
        return

    destino.mkdir(parents=True, exist_ok=True)
    for ruta in imagenes:
        ruta_mini, antes, despues = crear_miniatura(
            ruta, destino
        )
        print(
            f"  {ruta_mini.name}: {antes[0]}x{antes[1]} "
            f"-> {despues[0]}x{despues[1]} px"
        )
    print(f"Miniaturas en salida/{destino.name}/")


if __name__ == "__main__":
    main()
