# Archivo: cap10_crear_ejemplos.py

from pathlib import Path
from PIL import Image, ImageDraw


def crear_imagenes_prueba():
    carpeta = Path.cwd() / "entrada" / "imagenes_bruto"
    carpeta.mkdir(parents=True, exist_ok=True)

    muestras = [
        ("01_arcade_horizontal.png", (1600, 900),
         (35, 65, 110, 255)),
        ("02_cartucho_vertical.png", (900, 1200),
         (110, 45, 55, 255)),
        ("03_ficha_cuadrada.png", (1000, 1000),
         (40, 100, 70, 255)),
        ("04_icono_pequeno.png", (400, 300),
         (95, 75, 35, 255)),
    ]

    for nombre, dims, color in muestras:
        img = Image.new("RGBA", dims, color)
        dibujo = ImageDraw.Draw(img)
        ancho, alto = dims
        margen = 40
        dibujo.rectangle(
            [margen, margen, ancho - margen, alto - margen],
            outline=(240, 220, 120, 255),
            width=6,
        )
        ruta = carpeta / nombre
        img.save(ruta, "PNG")

    print(
        "Creadas 4 imágenes PNG de prueba en "
        "entrada/imagenes_bruto/"
    )


if __name__ == "__main__":
    crear_imagenes_prueba()
