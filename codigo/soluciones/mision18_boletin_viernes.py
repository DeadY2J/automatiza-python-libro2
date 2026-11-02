# Archivo: mision18_boletin_viernes.py

import argparse
from datetime import datetime
import json
from cap18_el_mayordomo import (
    BASE,
    consultar_tiempo_hoy,
    hacer_copia_trabajo,
    iniciar_logging,
    notificar_parte,
    ordenar_descargas,
)

VIERNES = 4


def es_viernes(fecha, forzar=False):
    return forzar or fecha.weekday() == VIERNES


def cierre_semanal(backups):
    zips = []
    if backups.exists():
        zips = sorted(backups.glob("*.zip"))
    total = sum(p.stat().st_size for p in zips)
    return (
        "=== CIERRE SEMANAL ===\n"
        f"Copias .zip guardadas: {len(zips)}\n"
        f"Espacio que ocupan: {total} bytes "
        f"({total / 1024:.1f} KB)"
    )


def leer_argumentos():
    parser = argparse.ArgumentParser(
        description="El Mayordomo con cierre de viernes."
    )
    parser.add_argument(
        "--hacer",
        action="store_true",
        help="Ejecuta cambios reales en disco.",
    )
    parser.add_argument(
        "--viernes",
        action="store_true",
        help="Fuerza el cierre semanal hoy.",
    )
    return parser.parse_args()


def main():
    args = leer_argumentos()
    simulacion = not args.hacer
    iniciar_logging(BASE / "salida" / "mayordomo.log")
    ruta_cfg = BASE / "entrada" / "mayordomo_config.json"
    if not ruta_cfg.exists():
        print("Ejecuta antes cap18_crear_ejemplos.py")
        return

    cfg = json.loads(ruta_cfg.read_text(encoding="utf-8"))
    descargas = BASE / "entrada" / "descargas_mayordomo"
    trabajo = BASE / "entrada" / "trabajo_mayordomo"
    backups = BASE / "copias" / "mayordomo_backups"
    modo_txt = "SIMULACIÓN" if simulacion else "REAL"

    res_desc = ordenar_descargas(
        descargas, cfg["categorias"], simulacion
    )
    res_copia = hacer_copia_trabajo(
        trabajo, backups, cfg["max_copias"], simulacion
    )
    res_clima = consultar_tiempo_hoy(
        cfg["latitud"], cfg["longitud"]
    )

    ahora = datetime.now()
    hoy = ahora.strftime("%Y-%m-%d %H:%M")
    parte = (
        f"**Parte matinal de El Mayordomo** "
        f"({hoy} - {modo_txt})\n"
        f"- **Descargas:** {res_desc}\n"
        f"- **Copia ZIP:** {res_copia}\n"
        f"- **Tiempo hoy:** {res_clima}"
    )
    if es_viernes(ahora, args.viernes):
        parte += "\n\n" + cierre_semanal(backups)
        ruta_bol = BASE / "salida" / "boletin_semanal.txt"
        ruta_bol.write_text(
            parte + "\n", encoding="utf-8", newline="\n"
        )
    notificar_parte(parte)


if __name__ == "__main__":
    main()
