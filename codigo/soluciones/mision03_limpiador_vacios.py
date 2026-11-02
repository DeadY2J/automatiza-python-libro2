# Archivo: mision03_limpiador_vacios.py

from datetime import datetime
from pathlib import Path
import shutil
import sys


def escribir_registro(ruta_log, mensaje):
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(f"[{ahora}] {mensaje}\n")
    print(mensaje)


def buscar_ruta_libre(carpeta, nombre):
    candidato = carpeta / nombre
    base = Path(nombre).stem
    ext = Path(nombre).suffix
    contador = 1
    while candidato.exists():
        candidato = carpeta / f"{base}_{contador}{ext}"
        contador += 1
    return candidato


def preparar_ejemplos(carpeta):
    if carpeta.exists():
        return
    carpeta.mkdir(parents=True)
    (carpeta / "vacio1.txt").write_bytes(b"")
    (carpeta / "vacio2.log").write_bytes(b"")
    for nombre in ["lleno1.txt", "lleno2.txt"]:
        (carpeta / nombre).write_text(
            "Este archivo tiene texto.\n",
            encoding="utf-8",
            newline="\n",
        )


def buscar_vacios(carpeta):
    return [
        p
        for p in sorted(carpeta.iterdir())
        if p.is_file() and p.stat().st_size == 0
    ]


def poner_en_cuarentena(carpeta, ruta_log, simulacion):
    cuarentena = carpeta / "Cuarentena"
    modo = "SIMULACIÓN" if simulacion else "REAL"
    escribir_registro(ruta_log, f"--- Modo {modo} ---")
    vacios = buscar_vacios(carpeta)
    if not vacios:
        escribir_registro(
            ruta_log, "No hay archivos vacíos."
        )
        return 0

    for archivo in vacios:
        destino = buscar_ruta_libre(
            cuarentena, archivo.name
        )
        rel = f"Cuarentena/{destino.name}"
        if simulacion:
            msg = (
                f"[SIMULACIÓN] Movería {archivo.name} "
                f"-> {rel}"
            )
        else:
            cuarentena.mkdir(exist_ok=True)
            shutil.move(str(archivo), str(destino))
            msg = f"[HECHO] {archivo.name} -> {rel}"
        escribir_registro(ruta_log, msg)
    return len(vacios)


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    raiz = Path.cwd()
    carpeta = raiz / "entrada" / "prueba_vacios"
    ruta_log = raiz / "salida" / "registro_cuarentena.txt"

    preparar_ejemplos(carpeta)
    poner_en_cuarentena(carpeta, ruta_log, simulacion)
    if simulacion:
        print("\nAñade --hacer para mover a Cuarentena.")


if __name__ == "__main__":
    main()
