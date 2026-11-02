# Archivo: cap18_el_mayordomo.py

import argparse
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import shutil
import zipfile
import requests

BASE = Path(__file__).resolve().parent
URL_METEO = "https://api.open-meteo.com/v1/forecast"


def iniciar_logging(ruta_log):
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s [%(levelname)s] %(message)s"
    h_arch = logging.FileHandler(ruta_log, encoding="utf-8")
    h_cons = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[h_arch, h_cons],
    )


def ruta_libre(carpeta, nombre):
    cand = carpeta / nombre
    stem = Path(nombre).stem
    suf = Path(nombre).suffix
    cont = 1
    while cand.exists():
        cand = carpeta / f"{stem}_{cont}{suf}"
        cont += 1
    return cand


def ordenar_descargas(carpeta, mapa_cats, simulacion):
    if not carpeta.exists():
        return "Carpeta de descargas no encontrada."

    archivos = sorted(
        p for p in carpeta.iterdir() if p.is_file()
    )
    if not archivos:
        return "0 archivos pendientes en Descargas."

    cont = 0
    for arch in archivos:
        ext = arch.suffix.lower()
        sub = mapa_cats.get(ext, "Otros")
        dest_dir = carpeta / sub
        dest = ruta_libre(dest_dir, arch.name)

        if simulacion:
            logging.info(
                "[SIM] Movería %s -> %s/%s",
                arch.name,
                sub,
                dest.name,
            )
            cont += 1
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(arch), str(dest))
            logging.info(
                "[OK] Movido %s -> %s/%s",
                arch.name,
                sub,
                dest.name,
            )
            cont += 1

    pref = "Simulados" if simulacion else "Ordenados"
    return f"{pref} {cont} archivo(s) en Descargas."


def hacer_copia_trabajo(
    origen, backups, max_copias, simulacion
):
    archivos = sorted(
        p for p in origen.rglob("*") if p.is_file()
    )
    marca = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    nuevo_zip = backups / f"backup_{marca}.zip"

    if not simulacion:
        backups.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(
            nuevo_zip, "w", zipfile.ZIP_DEFLATED
        ) as zf:
            for a in archivos:
                zf.write(a, arcname=a.relative_to(origen))

    zips = (
        list(backups.glob("backup_*.zip"))
        if backups.exists()
        else []
    )
    if simulacion and nuevo_zip not in zips:
        zips.append(nuevo_zip)

    ordenados = sorted(zips, key=lambda p: p.name)
    sobrantes = (
        ordenados[:-max_copias]
        if len(ordenados) > max_copias
        else []
    )
    hist = backups / "historico_antiguo"

    for viejo in sobrantes:
        if not simulacion:
            hist.mkdir(parents=True, exist_ok=True)
            dest = ruta_libre(hist, viejo.name)
            shutil.move(str(viejo), str(dest))

    estado = "Simulado" if simulacion else "Creado"
    return (
        f"{estado} {nuevo_zip.name} "
        f"({len(archivos)} arch., "
        f"{len(sobrantes)} copia(s) rotada(s))."
    )


def consultar_tiempo_hoy(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max"
        ),
        "timezone": "Europe/Madrid",
        "forecast_days": 1,
    }
    try:
        r = requests.get(
            URL_METEO, params=params, timeout=10
        )
        r.raise_for_status()
        d = r.json()["daily"]
        t_min = d["temperature_2m_min"][0]
        t_max = d["temperature_2m_max"][0]
        lluvia = d["precipitation_probability_max"][0]
        orig = "Open-Meteo"
    except (requests.RequestException, KeyError) as err:
        logging.warning("Usando clima simulado: %s", err)
        t_min, t_max, lluvia = 9.0, 18.5, 20
        orig = "Simulado"

    aviso = (
        "Paraguas" if lluvia >= 50 else "Cielo tranquilo"
    )
    return (
        f"{t_min} °C a {t_max} °C | "
        f"Lluvia: {lluvia} % ({aviso}) [{orig}]."
    )


def notificar_parte(resumen_txt):
    url = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    carga = {
        "username": "El Mayordomo",
        "content": resumen_txt,
    }
    if not url:
        logging.info(
            "[MODO PRUEBA] Sin DISCORD_WEBHOOK_URL. "
            "Parte matinal generado:"
        )
        print("\n" + "=" * 54)
        print(resumen_txt)
        print("=" * 54)
        return

    try:
        r = requests.post(url, json=carga, timeout=10)
        r.raise_for_status()
        logging.info("Parte enviado a Discord con éxito.")
    except requests.RequestException as err:
        logging.error("Fallo al enviar a Discord: %s", err)


def main():
    parser = argparse.ArgumentParser(
        description="El Mayordomo: rutina matinal."
    )
    parser.add_argument(
        "--hacer",
        action="store_true",
        help="Ejecuta cambios reales en disco.",
    )
    args = parser.parse_args()
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
    logging.info(
        "=== Iniciando El Mayordomo (%s) ===", modo_txt
    )

    res_desc = ordenar_descargas(
        descargas, cfg["categorias"], simulacion
    )
    res_copia = hacer_copia_trabajo(
        trabajo, backups, cfg["max_copias"], simulacion
    )
    res_clima = consultar_tiempo_hoy(
        cfg["latitud"], cfg["longitud"]
    )

    hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
    parte = (
        f"**Parte matinal de El Mayordomo** "
        f"({hoy} - {modo_txt})\n"
        f"- **Descargas:** {res_desc}\n"
        f"- **Copia ZIP:** {res_copia}\n"
        f"- **Tiempo hoy:** {res_clima}"
    )
    notificar_parte(parte)


if __name__ == "__main__":
    main()
