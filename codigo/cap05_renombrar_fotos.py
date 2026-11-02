# Archivo: cap05_renombrar_fotos.py

from datetime import datetime
import json
from pathlib import Path
import shutil
import sys

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png"}


def calcular_destino(archivo, base, reservados):
    marca = archivo.stat().st_mtime
    fecha = datetime.fromtimestamp(marca)
    anio = fecha.strftime("%Y")
    anio_mes = fecha.strftime("%Y-%m")
    dia_txt = fecha.strftime("%Y-%m-%d")
    ext = archivo.suffix.lower()

    carpeta_dest = base / anio / anio_mes
    numero = 1
    while True:
        nombre = f"{dia_txt}_{numero:03d}{ext}"
        candidato = carpeta_dest / nombre
        clave = candidato.as_posix()
        libre = not candidato.exists()
        if libre and clave not in reservados:
            reservados.add(clave)
            return candidato
        numero += 1


def obtener_fotos(carpeta):
    if not carpeta.exists():
        return []
    fotos = []
    for p in sorted(carpeta.iterdir()):
        ext = p.suffix.lower()
        if p.is_file() and ext in EXTENSIONES_VALIDAS:
            fotos.append(p)
    return fotos


def procesar_lote(base, ruta_json, simulacion):
    fotos = obtener_fotos(base)
    if not fotos:
        print("No hay imágenes para ordenar en la carpeta.")
        return

    modo = "SIMULACIÓN" if simulacion else "REAL"
    print(f"=== Ordenando fotos en modo {modo} ===")

    reservados = set()
    movimientos = []
    raiz = Path.cwd()

    for foto in fotos:
        destino = calcular_destino(foto, base, reservados)
        rel_dest = destino.relative_to(base).as_posix()

        if simulacion:
            print(
                f"[SIMULACIÓN] {foto.name} -> {rel_dest}"
            )
        else:
            destino.parent.mkdir(
                parents=True, exist_ok=True
            )
            shutil.move(str(foto), str(destino))
            print(f"[HECHO] {foto.name} -> {rel_dest}")
            movimientos.append(
                {
                    "origen": (
                        foto.relative_to(raiz).as_posix()
                    ),
                    "destino": (
                        destino.relative_to(raiz).as_posix()
                    ),
                }
            )

    if not simulacion and movimientos:
        ruta_json.parent.mkdir(parents=True, exist_ok=True)
        texto = json.dumps(movimientos, indent=2)
        ruta_json.write_text(texto + "\n", encoding="utf-8")
        print(
            f"\nMapa para deshacer guardado en: "
            f"{ruta_json.relative_to(raiz).as_posix()}"
        )


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    raiz = Path.cwd()
    base = raiz / "entrada" / "fotos_desordenadas"
    ruta_json = raiz / "salida" / "ultimo_lote_fotos.json"

    procesar_lote(base, ruta_json, simulacion)
    if simulacion:
        print(
            "\nAñade --hacer para renombrar y mover "
            "de verdad."
        )


if __name__ == "__main__":
    main()
