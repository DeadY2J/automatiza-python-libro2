# Archivo: cap03_plantilla_segura.py

from datetime import datetime
from pathlib import Path
import shutil
import sys

CATEGORIAS = {
    ".txt": "Documentos",
    ".csv": "Documentos",
    ".jpg": "Imagenes",
}


def escribir_registro(ruta_log, mensaje):
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ahora}] {mensaje}\n"
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(linea)
    print(mensaje)


def buscar_ruta_libre(carpeta_destino, nombre_archivo):
    candidato = carpeta_destino / nombre_archivo
    base = Path(nombre_archivo).stem
    ext = Path(nombre_archivo).suffix
    contador = 1
    while candidato.exists():
        nuevo = f"{base}_{contador}{ext}"
        candidato = carpeta_destino / nuevo
        contador += 1
    return candidato


def preparar_ejemplos(carpeta_origen):
    carpeta_origen.mkdir(parents=True, exist_ok=True)
    muestras = ["nota.txt", "foto.jpg", "datos.csv"]
    for nombre in muestras:
        ruta = carpeta_origen / nombre
        if not ruta.exists():
            ruta.write_text(
                f"Contenido de prueba de {nombre}\n",
                encoding="utf-8",
                newline="\n",
            )


def procesar_archivos(origen, copias, ruta_log, simulacion):
    modo = "SIMULACIÓN" if simulacion else "REAL"
    escribir_registro(
        ruta_log, f"--- Inicio en modo {modo} ---"
    )

    archivos = [
        p for p in origen.iterdir() if p.is_file()
    ]
    if not archivos:
        escribir_registro(
            ruta_log, "No hay archivos para procesar."
        )
        return

    for archivo in sorted(archivos):
        ext = archivo.suffix.lower()
        subcarpeta = CATEGORIAS.get(ext, "Otros")
        carpeta_dest = origen / subcarpeta
        destino_final = buscar_ruta_libre(
            carpeta_dest, archivo.name
        )
        rel_dest = (
            f"{subcarpeta}/{destino_final.name}"
        )

        if simulacion:
            msg = (
                f"[SIMULACIÓN] Movería {archivo.name} "
                f"-> {rel_dest}"
            )
            escribir_registro(ruta_log, msg)
        else:
            copias.mkdir(parents=True, exist_ok=True)
            carpeta_dest.mkdir(
                parents=True, exist_ok=True
            )
            ruta_copia = buscar_ruta_libre(
                copias, archivo.name
            )
            shutil.copy2(archivo, ruta_copia)
            shutil.move(str(archivo), str(destino_final))
            msg = (
                f"[HECHO] Copia en copias/"
                f"{ruta_copia.name} y movido a "
                f"{rel_dest}"
            )
            escribir_registro(ruta_log, msg)


def main():
    hacer_cambios = "--hacer" in sys.argv[1:]
    simulacion = not hacer_cambios

    base = Path.cwd()
    origen = base / "entrada" / "descargas_prueba"
    copias = base / "copias"
    ruta_log = base / "salida" / "registro_acciones.txt"

    preparar_ejemplos(origen)
    procesar_archivos(
        origen, copias, ruta_log, simulacion
    )

    if simulacion:
        print(
            "\nNota: No se ha movido ningún archivo. "
            "Añade --hacer para ejecutar de verdad."
        )


if __name__ == "__main__":
    main()
