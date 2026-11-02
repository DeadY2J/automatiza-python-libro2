# Archivo: mision05_separar_capturas.py

from datetime import datetime
from pathlib import Path
import shutil
import sys

EXTENSIONES = {".jpg", ".jpeg", ".png"}
PALABRAS_CAPTURA = ("screenshot", "captura")


def es_captura(archivo):
    nombre = archivo.stem.lower()
    return any(p in nombre for p in PALABRAS_CAPTURA)


def calcular_destino(archivo, base, reservados):
    fecha = datetime.fromtimestamp(archivo.stat().st_mtime)
    tipo = "Capturas" if es_captura(archivo) else "Fotos"
    carpeta = base / tipo / fecha.strftime("%Y-%m")
    dia = fecha.strftime("%Y-%m-%d")
    ext = archivo.suffix.lower()
    numero = 1
    while True:
        candidato = carpeta / f"{dia}_{numero:03d}{ext}"
        clave = candidato.as_posix()
        libre = not candidato.exists()
        if libre and clave not in reservados:
            reservados.add(clave)
            return candidato
        numero += 1


def obtener_imagenes(carpeta):
    if not carpeta.exists():
        return []
    return [
        p
        for p in sorted(carpeta.iterdir())
        if p.is_file() and p.suffix.lower() in EXTENSIONES
    ]


def separar(base, simulacion):
    reservados = set()
    etiqueta = "[SIMULACIÓN]" if simulacion else "[HECHO]"
    for foto in obtener_imagenes(base):
        destino = calcular_destino(foto, base, reservados)
        rel = destino.relative_to(base).as_posix()
        if not simulacion:
            destino.parent.mkdir(
                parents=True, exist_ok=True
            )
            shutil.move(str(foto), str(destino))
        print(f"{etiqueta} {foto.name} -> {rel}")


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    base = Path.cwd() / "entrada" / "fotos_desordenadas"
    if not obtener_imagenes(base):
        print(
            "No hay imágenes en "
            "entrada/fotos_desordenadas. "
            "Ejecuta antes cap05_crear_ejemplos.py"
        )
        return
    separar(base, simulacion)
    if simulacion:
        print("\nAñade --hacer para mover de verdad.")


if __name__ == "__main__":
    main()
