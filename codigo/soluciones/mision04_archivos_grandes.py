# Archivo: mision04_archivos_grandes.py

from pathlib import Path

UMBRAL_BYTES = 2000
PUESTOS = 3


def buscar_grandes(base, umbral):
    grandes = []
    for ruta in base.rglob("*"):
        if not ruta.is_file():
            continue
        tamano = ruta.stat().st_size
        if tamano > umbral:
            rel = ruta.relative_to(base).as_posix()
            grandes.append((tamano, rel))
    return sorted(grandes, reverse=True)


def main():
    base = Path.cwd() / "entrada" / "almacen_prueba"
    if not base.exists():
        print(
            "No existe entrada/almacen_prueba. "
            "Ejecuta antes cap04_crear_ejemplos.py"
        )
        return

    grandes = buscar_grandes(base, UMBRAL_BYTES)
    print(f"Archivos de más de {UMBRAL_BYTES} bytes: "
          f"{len(grandes)}")
    print(f"Top {PUESTOS} de los más pesados:")
    for puesto, (tamano, rel) in enumerate(
        grandes[:PUESTOS], start=1
    ):
        print(f"  {puesto}. {tamano:>6} bytes  {rel}")


if __name__ == "__main__":
    main()
