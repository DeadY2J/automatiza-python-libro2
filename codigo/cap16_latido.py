# Archivo: cap16_latido.py

from datetime import datetime
from pathlib import Path
import sys


def obtener_carpeta_base():
    return Path(__file__).resolve().parent


def registrar_latido(base, modo_auto):
    ruta_log = base / "salida" / "latidos_automaticos.log"
    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    origen = "TAREA_AUTO" if modo_auto else "MANUAL"
    ejecutable = Path(sys.executable).name
    ver = (
        f"{sys.version_info.major}."
        f"{sys.version_info.minor}"
    )

    linea = (
        f"[{ahora}] [{origen}] OK | "
        f"Python {ver} ({ejecutable})\n"
    )
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(linea)

    print(f"Latido registrado: {linea.strip()}")
    return ruta_log


def generar_lanzador_bat(base):
    ruta_bat = base / "cap16_lanzador.bat"
    lineas_bat = [
        "@echo off",
        'cd /d "%~dp0"',
        "if not exist salida mkdir salida",
        "if exist .venv\\Scripts\\python.exe (",
        "  .venv\\Scripts\\python.exe cap16_latido.py "
        "--auto >> salida\\consola_tarea.log 2>&1",
        ") else (",
        "  python cap16_latido.py --auto "
        ">> salida\\consola_tarea.log 2>&1",
        ")",
    ]
    contenido = "\n".join(lineas_bat) + "\n"
    ruta_bat.write_text(
        contenido, encoding="utf-8", newline="\r\n"
    )
    return ruta_bat


def main():
    modo_auto = "--auto" in sys.argv[1:]
    base = obtener_carpeta_base()

    try:
        ruta_log = registrar_latido(base, modo_auto)
        if not modo_auto:
            ruta_bat = generar_lanzador_bat(base)
            print(
                f"Historial en: "
                f"salida/{ruta_log.name}"
            )
            print(
                f"Lanzador creado: "
                f"{ruta_bat.name}"
            )
        sys.exit(0)
    except Exception as err:
        print(f"[ERROR CRÍTICO] {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
