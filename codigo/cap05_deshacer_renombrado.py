# Archivo: cap05_deshacer_renombrado.py

import json
from pathlib import Path
import shutil
import sys


def deshacer_lote(ruta_json, simulacion):
    if not ruta_json.exists():
        print("No existe registro de lote para deshacer.")
        return

    datos = json.loads(
        ruta_json.read_text(encoding="utf-8")
    )
    raiz = Path.cwd()
    modo = "SIMULACIÓN" if simulacion else "REAL"
    print(f"=== Deshaciendo lote en modo {modo} ===")

    for item in reversed(datos):
        orig = raiz / item["origen"]
        dest = raiz / item["destino"]
        if not dest.exists():
            print(
                f"[AVISO] No se encuentra {item['destino']}"
            )
            continue
        if orig.exists():
            print(
                f"[AVISO] Ya existe {item['origen']}, "
                "se omite"
            )
            continue

        if simulacion:
            print(
                f"[SIMULACIÓN] Restauraría {dest.name} "
                f"-> {orig.name}"
            )
        else:
            orig.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(orig))
            print(
                f"[RESTAURADO] {dest.name} -> {orig.name}"
            )

    if not simulacion:
        ruta_json.unlink()
        print("\nLote restaurado y registro JSON limpiado.")


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    ruta_json = (
        Path.cwd() / "salida" / "ultimo_lote_fotos.json"
    )
    deshacer_lote(ruta_json, simulacion)
    if simulacion and ruta_json.exists():
        print(
            "\nAñade --hacer para restaurar los archivos."
        )


if __name__ == "__main__":
    main()
