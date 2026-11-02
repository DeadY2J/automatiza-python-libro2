# Archivo: mision15_detector_fechas_importes.py

from pathlib import Path
from cap15_el_escriba import EXTENSIONES, leer_documento

PALABRAS_CLAVE = [
    "eur",
    "plazo",
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
]


def lineas_clave(texto):
    encontradas = []
    for lin in texto.splitlines():
        minus = lin.lower()
        if any(p in minus for p in PALABRAS_CLAVE):
            encontradas.append(lin.strip())
    return encontradas


def construir_agenda(compromisos):
    lineas = [
        "# Agenda urgente",
        "",
        f"Compromisos detectados: {len(compromisos)}",
        "",
        "| Archivo | Línea detectada |",
        "|---|---|",
    ]
    for nombre, lin in compromisos:
        limpia = lin.replace("|", "/")
        lineas.append(f"| {nombre} | {limpia} |")
    return "\n".join(lineas) + "\n"


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "documentos_escriba"
    if not entrada.exists():
        print("Ejecuta antes cap15_crear_ejemplos.py")
        return

    compromisos = []
    for ruta in sorted(entrada.iterdir()):
        if ruta.suffix.lower() not in EXTENSIONES:
            continue
        lineas = lineas_clave(leer_documento(ruta))
        print(f"{ruta.name}: {len(lineas)} línea(s)")
        for lin in lineas:
            compromisos.append((ruta.name, lin))

    agenda = construir_agenda(compromisos)
    salida = raiz / "salida" / "agenda_urgente.md"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(
        agenda, encoding="utf-8", newline="\n"
    )
    print(f"\nAgenda guardada en: salida/{salida.name}\n")
    print(agenda, end="")


if __name__ == "__main__":
    main()
