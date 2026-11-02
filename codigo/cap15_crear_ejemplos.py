# Archivo: cap15_crear_ejemplos.py

from pathlib import Path


def escribir_pdf_minimo(ruta, lineas):
    cmds = ["BT", "/F1 12 Tf", "50 750 Td", "18 TL"]
    for lin in lineas:
        limpio = (
            lin.replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
        )
        cmds.append(f"({limpio}) Tj T*")
    cmds.append("ET")
    flujo = "\n".join(cmds).encode("latin-1", "replace")

    cuerpos = {
        1: b"<< /Type /Catalog /Pages 2 0 R >>",
        2: b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        3: (
            b"<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 5 0 R >> >> "
            b"/Contents 4 0 R >>"
        ),
        4: (
            f"<< /Length {len(flujo)} >>\nstream\n".encode(
                "ascii"
            )
            + flujo
            + b"\nendstream"
        ),
        5: (
            b"<< /Type /Font /Subtype /Type1 "
            b"/BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>"
        ),
    }

    salida = bytearray(b"%PDF-1.4\n")
    pos = {}
    for idx in range(1, 6):
        pos[idx] = len(salida)
        cab = f"{idx} 0 obj\n".encode("ascii")
        salida.extend(cab + cuerpos[idx] + b"\nendobj\n")

    pos_xref = len(salida)
    salida.extend(b"xref\n0 6\n0000000000 65535 f \n")
    for idx in range(1, 6):
        linea = f"{pos[idx]:010d} 00000 n \n"
        salida.extend(linea.encode("ascii"))

    cola = (
        f"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        f"startxref\n{pos_xref}\n%%EOF\n"
    )
    salida.extend(cola.encode("ascii"))
    ruta.write_bytes(bytes(salida))


def main():
    carpeta = Path.cwd() / "entrada" / "documentos_escriba"
    carpeta.mkdir(parents=True, exist_ok=True)

    nota_txt = (
        "Reunión de logística del torneo retro.\n"
        "Fecha prevista: sábado 18 de abril en el "
        "pabellón.\n"
        "Se necesitan 12 regletas de enchufes y "
        "8 televisores.\n"
        "Adriana confirmará el seguro del local "
        "el jueves.\n"
    )
    (carpeta / "01_logistica_torneo.txt").write_text(
        nota_txt, encoding="utf-8", newline="\n"
    )

    ideas_md = (
        "# Propuesta de taller de Python\n\n"
        "Duración: 2 horas prácticas para principiantes.\n"
        "Temario: ordenar descargas y leer hojas "
        "de cálculo.\n"
        "Requisitos: traer portátil con Python "
        "3.12 instalado.\n"
    )
    (carpeta / "02_propuesta_taller.md").write_text(
        ideas_md, encoding="utf-8", newline="\n"
    )

    lineas_pdf = [
        "PRESUPUESTO IMPRENTA P-2026-44",
        "Tirada de 200 carteles A3 a todo color: "
        "85.00 EUR.",
        "Tirada de 500 acreditaciones "
        "plastificadas: 60.00 EUR.",
        "Plazo de entrega: 4 dias laborables "
        "tras confirmar.",
    ]
    escribir_pdf_minimo(
        carpeta / "03_presupuesto_imprenta.pdf", lineas_pdf
    )

    print(
        "Creados 3 documentos (.txt, .md, .pdf) en "
        "entrada/documentos_escriba/"
    )


if __name__ == "__main__":
    main()
