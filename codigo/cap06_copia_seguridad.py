# Archivo: cap06_copia_seguridad.py

from datetime import datetime
from pathlib import Path
import shutil
import sys
import zipfile

MAX_COPIAS = 3


def listar_archivos_origen(carpeta_origen):
    if not carpeta_origen.exists():
        return []
    return sorted(
        p for p in carpeta_origen.rglob("*") if p.is_file()
    )


def crear_zip(origen, ruta_zip, archivos, simulacion):
    if simulacion:
        print(
            f"[SIMULACIÓN] Crearía {ruta_zip.name} con "
            f"{len(archivos)} archivo(s)."
        )
        return

    ruta_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        ruta_zip, "w", zipfile.ZIP_DEFLATED
    ) as zf:
        for archivo in archivos:
            rel = archivo.relative_to(origen)
            zf.write(archivo, arcname=rel)

    tam = ruta_zip.stat().st_size
    print(
        f"[HECHO] Creado {ruta_zip.name} "
        f"({len(archivos)} archivos, {tam} bytes)."
    )


def rotar_copias_antiguas(
    carpeta_backups, nuevo_zip, max_copias, simulacion
):
    existentes = []
    if carpeta_backups.exists():
        existentes = list(
            carpeta_backups.glob("backup_*.zip")
        )

    if simulacion and nuevo_zip not in existentes:
        existentes.append(nuevo_zip)

    ordenadas = sorted(existentes, key=lambda p: p.name)
    if len(ordenadas) <= max_copias:
        print(
            f"Rotación: {len(ordenadas)}/{max_copias} "
            f"copias. No sobra ninguna."
        )
        return

    sobrantes = ordenadas[:-max_copias]
    historico = carpeta_backups / "historico_antiguo"

    for viejo in sobrantes:
        if simulacion:
            print(
                f"[SIMULACIÓN] Rotaría copia antigua: "
                f"{viejo.name} -> historico_antiguo/"
            )
        else:
            historico.mkdir(parents=True, exist_ok=True)
            destino = historico / viejo.name
            contador = 1
            while destino.exists():
                nuevo_nom = (
                    f"{viejo.stem}_{contador}{viejo.suffix}"
                )
                destino = historico / nuevo_nom
                contador += 1
            shutil.move(str(viejo), str(destino))
            print(
                f"[ROTADO] {viejo.name} movido a "
                f"historico_antiguo/{destino.name}"
            )


def main():
    simulacion = "--hacer" not in sys.argv[1:]
    raiz = Path.cwd()
    origen = raiz / "entrada" / "proyecto_activo"
    backups = raiz / "copias" / "backups_proyecto"

    archivos = listar_archivos_origen(origen)
    if not archivos:
        print(
            "No hay archivos en entrada/proyecto_activo. "
            "Ejecuta antes cap06_crear_ejemplos.py"
        )
        return

    marca = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    nuevo_zip = backups / f"backup_{marca}.zip"

    modo = "SIMULACIÓN" if simulacion else "REAL"
    print(f"=== Copia de seguridad en modo {modo} ===")

    crear_zip(origen, nuevo_zip, archivos, simulacion)
    rotar_copias_antiguas(
        backups, nuevo_zip, MAX_COPIAS, simulacion
    )

    if simulacion:
        print(
            "\nAñade --hacer para crear el ZIP y rotar."
        )


if __name__ == "__main__":
    main()
