# Archivo: mision06_extractor_seguro.py

from pathlib import Path
import sys
import zipfile


def copia_mas_reciente(carpeta):
    if not carpeta.exists():
        return None
    ordenadas = sorted(
        carpeta.glob("backup_*.zip"), key=lambda p: p.name
    )
    if not ordenadas:
        return None
    return ordenadas[-1]


def carpeta_libre(base):
    candidata = base
    contador = 1
    while candidata.exists():
        nombre = f"{base.name}_{contador}"
        candidata = base.with_name(nombre)
        contador += 1
    return candidata


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    raiz = Path.cwd()
    backups = raiz / "copias" / "backups_proyecto"
    ruta_zip = copia_mas_reciente(backups)
    if ruta_zip is None:
        print("No hay copias backup_*.zip que restaurar.")
        return

    print(f"Copia más reciente: {ruta_zip.name}")
    with zipfile.ZipFile(ruta_zip, "r") as zf:
        for info in zf.infolist():
            print(
                f"  - {info.filename} "
                f"({info.file_size} bytes)"
            )

        destino = carpeta_libre(
            raiz / "salida" / "restauracion_prueba"
        )
        rel = destino.relative_to(raiz).as_posix()
        if simulacion:
            print(f"\n[SIMULACIÓN] Extraería en {rel}/")
            print("Añade --hacer para extraer de verdad.")
        else:
            zf.extractall(destino)
            print(f"\n[HECHO] Extraída en {rel}/")


if __name__ == "__main__":
    main()
