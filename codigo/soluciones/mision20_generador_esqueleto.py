# Archivo: mision20_generador_esqueleto.py

import argparse
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent

PLANTILLA = [
    "# Archivo: NOMBRE.py",
    "",
    "import argparse",
    "import logging",
    "from pathlib import Path",
    "",
    "BASE = Path(__file__).resolve().parent",
    "",
    "",
    "def leer_argumentos():",
    "    parser = argparse.ArgumentParser(",
    '        description="Script NOMBRE del taller."',
    "    )",
    "    parser.add_argument(",
    '        "--hacer",',
    '        action="store_true",',
    '        help="Aplica los cambios reales.",',
    "    )",
    "    return parser.parse_args()",
    "",
    "",
    "def main():",
    "    args = leer_argumentos()",
    "    simulacion = not args.hacer",
    "    logging.basicConfig(",
    "        level=logging.INFO,",
    "        format=(",
    '            "%(asctime)s [%(levelname)s] %(message)s"',
    "        ),",
    '        datefmt="%Y-%m-%d %H:%M:%S",',
    "    )",
    '    modo = "SIMULACIÓN" if simulacion else "REAL"',
    '    logging.info("Iniciando NOMBRE (%s)", modo)',
    '    entrada = BASE / "entrada"',
    '    logging.info("Entrada: %s", entrada.name)',
    "    # Tu código va aquí: si simulacion es True,",
    "    # solo informa de lo que harías.",
    "",
    "",
    'if __name__ == "__main__":',
    "    main()",
]


def limpiar_nombre(texto):
    nombre = texto.strip().lower().replace(" ", "_")
    nombre = nombre.removesuffix(".py")
    return re.sub(r"[^a-z0-9_]", "", nombre)


def crear_esqueleto(carpeta, nombre):
    ruta = carpeta / f"{nombre}.py"
    if ruta.exists():
        return ruta, False
    texto = "\n".join(PLANTILLA) + "\n"
    texto = texto.replace("NOMBRE", nombre)
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    return ruta, True


def main():
    parser = argparse.ArgumentParser(
        description="Crea el esqueleto de un script."
    )
    parser.add_argument(
        "nombre", help="Ejemplo: clasificar_recibos"
    )
    args = parser.parse_args()

    nombre = limpiar_nombre(args.nombre)
    if not nombre:
        print("El nombre no tiene letras ni números.")
        sys.exit(1)

    ruta, creado = crear_esqueleto(BASE, nombre)
    if not creado:
        print(f"Ya existe {ruta.name}: no lo sobrescribo.")
        sys.exit(1)
    print(f"Creado {ruta.name}. Pruébalo con:")
    print(f"  python {ruta.name} --help")


if __name__ == "__main__":
    main()
