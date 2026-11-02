# Archivo: cap09_crear_ejemplos.py

from pathlib import Path


def escribir_pdf_minimo(ruta, paginas_lineas):
    n_pags = len(paginas_lineas)
    id_fuente = 3 + (2 * n_pags)
    cuerpos = {}
    ids_pags = []

    for i, lineas in enumerate(paginas_lineas):
        id_pag = 3 + (2 * i)
        id_cont = id_pag + 1
        ids_pags.append(f"{id_pag} 0 R")

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

        cuerpos[id_pag] = (
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 595 842] "
            f"/Resources << /Font << "
            f"/F1 {id_fuente} 0 R >> >> "
            f"/Contents {id_cont} 0 R >>"
        ).encode("ascii")

        cab = f"<< /Length {len(flujo)} >>\nstream\n"
        cuerpos[id_cont] = (
            cab.encode("ascii") + flujo + b"\nendstream"
        )

    cuerpos[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(ids_pags)
    cuerpos[2] = (
        f"<< /Type /Pages /Kids [{kids}] "
        f"/Count {n_pags} >>"
    ).encode("ascii")
    cuerpos[id_fuente] = (
        b"<< /Type /Font /Subtype /Type1 "
        b"/BaseFont /Helvetica "
        b"/Encoding /WinAnsiEncoding >>"
    )

    salida = bytearray(b"%PDF-1.4\n")
    posiciones = {}
    total_objs = id_fuente

    for idx in range(1, total_objs + 1):
        posiciones[idx] = len(salida)
        enc = f"{idx} 0 obj\n".encode("ascii")
        salida.extend(enc + cuerpos[idx] + b"\nendobj\n")

    pos_xref = len(salida)
    salida.extend(
        f"xref\n0 {total_objs + 1}\n".encode("ascii")
    )
    salida.extend(b"0000000000 65535 f \n")
    for idx in range(1, total_objs + 1):
        linea_x = f"{posiciones[idx]:010d} 00000 n \n"
        salida.extend(linea_x.encode("ascii"))

    cola = (
        f"trailer\n<< /Size {total_objs + 1} "
        f"/Root 1 0 R >>\n"
        f"startxref\n{pos_xref}\n%%EOF\n"
    )
    salida.extend(cola.encode("ascii"))
    ruta.write_bytes(bytes(salida))


def main():
    carpeta = Path.cwd() / "entrada" / "pdfs_prueba"
    carpeta.mkdir(parents=True, exist_ok=True)

    doc1 = [
        [
            "FACTURA F-2026-001",
            "Cliente: Recreaciones Norte SL",
            "Concepto: Mantenimiento de placas arcade",
            "Total: 180.00 EUR",
        ],
        [
            "FACTURA F-2026-001 - Anexo",
            "Detalle de horas: 6 horas de taller.",
        ],
    ]
    doc2 = [
        [
            "FACTURA F-2026-002",
            "Cliente: Club Bit Ochenta",
            "Concepto: Lote de cables RGB y mandos",
            "Total: 95.50 EUR",
        ]
    ]
    doc3 = [
        [
            "NOTA DE ENTREGA N-099",
            "Estado: Entregado en almacén central.",
            "Observaciones: Caja revisada sin daños.",
        ]
    ]

    escribir_pdf_minimo(
        carpeta / "01_factura_enero.pdf", doc1
    )
    escribir_pdf_minimo(
        carpeta / "02_factura_febrero.pdf", doc2
    )
    escribir_pdf_minimo(
        carpeta / "03_albaran_entrega.pdf", doc3
    )
    print("Creados 3 archivos PDF en entrada/pdfs_prueba/")


if __name__ == "__main__":
    main()
