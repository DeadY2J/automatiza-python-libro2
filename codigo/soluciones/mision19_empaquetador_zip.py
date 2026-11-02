# Archivo: mision19_empaquetador_zip.py

from pathlib import Path
import zipfile
from cap19_preparar_entrega import (
    BASE,
    auditar_codigo,
    listar_scripts_py,
)

EXTRAS = [
    "cap19_preparar_entrega.py",
    "requirements.txt",
    "README.md",
]


def ruta_libre(ruta):
    cand = ruta
    cont = 1
    while cand.exists():
        cand = ruta.with_name(
            f"{ruta.stem}_{cont}{ruta.suffix}"
        )
        cont += 1
    return cand


def elegir_archivos(base):
    elegidos = list(listar_scripts_py(base))
    for nombre in EXTRAS:
        ruta = base / nombre
        if ruta.is_file() and ruta not in elegidos:
            elegidos.append(ruta)
    return elegidos


def crear_kit(base, archivos, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destino, "w", zipfile.ZIP_DEFLATED
    ) as zf:
        for ruta in archivos:
            zf.write(ruta, arcname=ruta.relative_to(base))
    return destino


def main():
    total, alertas = auditar_codigo(BASE)
    print(f"Scripts auditados: {total}")
    if alertas:
        print(f"{len(alertas)} alerta(s). No creo el .zip:")
        for arch, fila, mot in alertas:
            print(f"  [!] {arch} (línea {fila}): {mot}")
        return

    archivos = elegir_archivos(BASE)
    salida = BASE / "salida" / "kit_compartir_taller.zip"
    destino = crear_kit(BASE, archivos, ruta_libre(salida))
    print("Auditoría limpia (0 alertas).")
    print(
        f"Empaquetados {len(archivos)} archivos en "
        f"salida/{destino.name}"
    )


if __name__ == "__main__":
    main()
