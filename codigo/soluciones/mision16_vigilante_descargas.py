# Archivo: mision16_vigilante_descargas.py

from datetime import datetime
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
CABECERA = "fecha_hora,archivos,total_bytes\n"


def medir_carpeta(carpeta):
    if not carpeta.exists():
        return 0, 0
    archivos = [
        p for p in carpeta.rglob("*") if p.is_file()
    ]
    total = sum(p.stat().st_size for p in archivos)
    return len(archivos), total


def anotar_historico(ruta_csv, archivos, total, ahora):
    ruta_csv.parent.mkdir(parents=True, exist_ok=True)
    existe = ruta_csv.exists()
    marca = ahora.strftime("%Y-%m-%d %H:%M:%S")
    with open(
        ruta_csv, "a", encoding="utf-8", newline="\n"
    ) as f:
        if not existe:
            f.write(CABECERA)
        f.write(f"{marca},{archivos},{total}\n")
    return not existe


def main():
    entrada = BASE / "entrada"
    ruta_csv = BASE / "salida" / "historico_tamano.csv"
    try:
        archivos, total = medir_carpeta(entrada)
        nuevo = anotar_historico(
            ruta_csv, archivos, total, datetime.now()
        )
    except OSError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        sys.exit(1)

    if nuevo:
        print("Creado salida/historico_tamano.csv")
    print(f"Archivos en entrada/: {archivos}")
    print(f"Total: {total} bytes")
    sys.exit(0)


if __name__ == "__main__":
    main()
