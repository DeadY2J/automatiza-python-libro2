# Archivo: cap17_limpiador_robusto.py

import argparse
import json
import logging
from pathlib import Path
import shutil

CARPETA_BASE = Path(__file__).resolve().parent


def configurar_logging(ruta_log):
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    formato = "%(asctime)s [%(levelname)s] %(message)s"
    manejador_arch = logging.FileHandler(
        ruta_log, encoding="utf-8"
    )
    manejador_cons = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[manejador_arch, manejador_cons],
    )


def asegurar_escenario(ruta_cfg, carpeta_sucia):
    carpeta_sucia.mkdir(parents=True, exist_ok=True)
    if not ruta_cfg.exists():
        cfg_defecto = {
            "extensiones": [".tmp", ".bak", ".old"],
            "min_bytes": 100,
        }
        txt = json.dumps(cfg_defecto, indent=2)
        ruta_cfg.write_text(
            txt + "\n", encoding="utf-8", newline="\n"
        )

    muestras = [
        ("cache_01.tmp", "X" * 250),
        ("copia_vieja.bak", "Y" * 300),
        ("mini.tmp", "Z" * 10),
        ("documento_bueno.txt", "Conservar siempre" * 20),
    ]
    for nombre, contenido in muestras:
        p = carpeta_sucia / nombre
        if not p.exists():
            p.write_text(
                contenido, encoding="utf-8", newline="\n"
            )


def es_candidato(ruta, extensiones, min_bytes):
    if not ruta.is_file():
        return False
    ext = ruta.suffix.lower()
    exts_limpias = {e.lower() for e in extensiones}
    if ext not in exts_limpias:
        return False
    return ruta.stat().st_size >= min_bytes


def ruta_sin_colision(carpeta_dest, nombre):
    candidato = carpeta_dest / nombre
    stem = Path(nombre).stem
    suf = Path(nombre).suffix
    cont = 1
    while candidato.exists():
        candidato = carpeta_dest / f"{stem}_{cont}{suf}"
        cont += 1
    return candidato


def mover_con_seguridad(archivo, carpeta_dest, simulacion):
    destino = ruta_sin_colision(carpeta_dest, archivo.name)
    if simulacion:
        logging.info(
            "[SIMULACIÓN] Movería %s -> %s",
            archivo.name,
            destino.name,
        )
        return True

    try:
        carpeta_dest.mkdir(parents=True, exist_ok=True)
        shutil.move(str(archivo), str(destino))
        logging.info(
            "[HECHO] Movido %s -> %s",
            archivo.name,
            destino.name,
        )
        return True
    except OSError as err:
        logging.error(
            "No se pudo mover %s: %s", archivo.name, err
        )
        return False


def leer_argumentos():
    parser = argparse.ArgumentParser(
        description="Limpiador robusto de temporales."
    )
    parser.add_argument(
        "--hacer",
        action="store_true",
        help="Ejecuta el movimiento real de archivos.",
    )
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=None,
        help="Tamaño mínimo en bytes para filtrar.",
    )
    return parser.parse_args()


def main():
    args = leer_argumentos()
    simulacion = not args.hacer

    ruta_log = (
        CARPETA_BASE / "salida" / "limpiador_robusto.log"
    )
    configurar_logging(ruta_log)

    ruta_cfg = (
        CARPETA_BASE / "entrada" / "config_limpiador.json"
    )
    sucia = CARPETA_BASE / "entrada" / "taller_sucio"
    cuarentena = (
        CARPETA_BASE / "salida" / "cuarentena_temp"
    )

    asegurar_escenario(ruta_cfg, sucia)
    cfg = json.loads(ruta_cfg.read_text(encoding="utf-8"))

    exts = cfg.get("extensiones", [".tmp"])
    min_b = (
        args.min_bytes
        if args.min_bytes is not None
        else cfg.get("min_bytes", 100)
    )

    modo = "SIMULACIÓN" if simulacion else "REAL"
    logging.info(
        "Iniciando limpieza (%s) | min_bytes=%d",
        modo,
        min_b,
    )

    movidos = 0
    for ruta in sorted(sucia.iterdir()):
        if es_candidato(ruta, exts, min_b):
            if mover_con_seguridad(
                ruta, cuarentena, simulacion
            ):
                movidos += 1

    logging.info(
        "Proceso terminado. Archivos afectados: %d", movidos
    )


if __name__ == "__main__":
    main()
