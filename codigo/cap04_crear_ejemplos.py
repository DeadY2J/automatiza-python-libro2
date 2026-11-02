# Archivo: cap04_crear_ejemplos.py

from pathlib import Path


def crear_almacen_prueba():
    base = Path.cwd() / "entrada" / "almacen_prueba"
    docs = base / "documentos" / "2025"
    fotos = base / "multimedia" / "fotos"
    copias = base / "descargas_viejas"

    for carpeta in [docs, fotos, copias]:
        carpeta.mkdir(parents=True, exist_ok=True)

    texto_factura = (
        "Factura de suministro eléctrico #901\n" * 40
    )
    texto_manual = (
        "Manual de instrucciones del sintetizador\n" * 80
    )
    datos_imagen = (
        b"\x89PNG\r\n\x1a\n" + b"PIXEL_DATA_88" * 200
    )

    (docs / "factura_enero.txt").write_text(
        texto_factura,
        encoding="utf-8",
        newline="\n",
    )
    (docs / "manual_sinte.txt").write_text(
        texto_manual,
        encoding="utf-8",
        newline="\n",
    )
    (fotos / "retrato_01.png").write_bytes(datos_imagen)
    (fotos / "paisaje_02.png").write_bytes(
        datos_imagen + b"_DISTINTO"
    )

    # Duplicados con distinto nombre y en otras carpetas
    (copias / "recibo_copia.txt").write_text(
        texto_factura,
        encoding="utf-8",
        newline="\n",
    )
    (copias / "IMG_backup.png").write_bytes(datos_imagen)
    (base / "leeme_urgente.md").write_text(
        "Notas sueltas del proyecto.\n",
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Carpeta entrada/almacen_prueba creada "
        "con 7 archivos."
    )


if __name__ == "__main__":
    crear_almacen_prueba()
