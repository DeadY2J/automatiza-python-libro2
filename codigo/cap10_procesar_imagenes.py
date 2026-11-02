# Archivo: cap10_procesar_imagenes.py

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

MAX_LADO = 800
CALIDAD_JPG = 85
TEXTO_MARCA = "Taller Python"
EXTENSIONES = {".png", ".jpg", ".jpeg"}


def estampar_marca_agua(img, texto):
    dibujo = ImageDraw.Draw(img)
    fuente = ImageFont.load_default(size=18)

    caja = dibujo.textbbox((0, 0), texto, font=fuente)
    ancho_txt = caja[2] - caja[0]
    alto_txt = caja[3] - caja[1]

    ancho_img, alto_img = img.size
    margen = 14
    pos_x = ancho_img - ancho_txt - margen
    pos_y = alto_img - alto_txt - margen

    relleno = 6
    rect = [
        pos_x - relleno,
        pos_y - relleno,
        pos_x + ancho_txt + relleno,
        pos_y + alto_txt + relleno,
    ]
    dibujo.rectangle(rect, fill=(20, 20, 20))
    dibujo.text(
        (pos_x, pos_y),
        texto,
        fill=(255, 255, 255),
        font=fuente,
    )


def procesar_una_imagen(ruta_orig, carpeta_dest):
    with Image.open(ruta_orig) as img:
        dims_antes = img.size
        copia = img.convert("RGB")

    copia.thumbnail((MAX_LADO, MAX_LADO))
    dims_despues = copia.size
    estampar_marca_agua(copia, TEXTO_MARCA)

    ruta_salida = carpeta_dest / f"{ruta_orig.stem}.jpg"
    copia.save(
        ruta_salida,
        "JPEG",
        quality=CALIDAD_JPG,
        optimize=True,
    )
    peso = ruta_salida.stat().st_size
    return dims_antes, dims_despues, ruta_salida.name, peso


def obtener_imagenes(carpeta):
    if not carpeta.exists():
        return []
    lista = []
    for p in sorted(carpeta.iterdir()):
        if p.is_file() and p.suffix.lower() in EXTENSIONES:
            lista.append(p)
    return lista


def main():
    raiz = Path.cwd()
    origen = raiz / "entrada" / "imagenes_bruto"
    destino = raiz / "salida" / "imagenes_listas"

    imagenes = obtener_imagenes(origen)
    if not imagenes:
        print(
            "No hay imágenes en entrada/imagenes_bruto. "
            "Ejecuta antes cap10_crear_ejemplos.py"
        )
        return

    destino.mkdir(parents=True, exist_ok=True)
    print("=" * 56)
    print("PROCESANDO LOTE DE IMÁGENES CON PILLOW")
    print("=" * 56)

    for ruta in imagenes:
        antes, despues, nom_sal, peso = (
            procesar_una_imagen(ruta, destino)
        )
        txt_antes = f"{antes[0]}x{antes[1]}"
        txt_desp = f"{despues[0]}x{despues[1]}"
        print(
            f"  {ruta.name}\n"
            f"    -> {nom_sal} ({txt_antes} a "
            f"{txt_desp} px, "
            f"{peso} bytes)"
        )

    print("=" * 56)
    print(
        f"Lote completado: {len(imagenes)} imágenes en "
        f"salida/imagenes_listas/"
    )


if __name__ == "__main__":
    main()
