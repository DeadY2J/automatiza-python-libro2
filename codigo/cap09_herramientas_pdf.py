# Archivo: cap09_herramientas_pdf.py

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def obtener_pdfs(carpeta):
    if not carpeta.exists():
        return []
    return sorted(carpeta.glob("*.pdf"))


def unir_todos_los_pdfs(lista_pdfs, ruta_salida):
    escritor = PdfWriter()
    total_paginas = 0

    for ruta in lista_pdfs:
        lector = PdfReader(ruta)
        num_pags = len(lector.pages)
        total_paginas += num_pags
        escritor.append(ruta)

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta_salida, "wb") as f:
        escritor.write(f)

    return total_paginas


def separar_primera_pagina(ruta_pdf, ruta_salida):
    lector = PdfReader(ruta_pdf)
    if len(lector.pages) == 0:
        return False

    escritor = PdfWriter()
    escritor.add_page(lector.pages[0])

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta_salida, "wb") as f:
        escritor.write(f)

    return True


def extraer_todo_el_texto(lista_pdfs, ruta_txt):
    bloques = []
    for ruta in lista_pdfs:
        lector = PdfReader(ruta)
        bloques.append("=" * 50)
        bloques.append(
            f"ARCHIVO: {ruta.name} "
            f"({len(lector.pages)} pág.)"
        )
        bloques.append("=" * 50)

        for idx, pagina in enumerate(
            lector.pages, start=1
        ):
            texto = pagina.extract_text() or ""
            texto_limpio = texto.strip()
            bloques.append(f"--- Página {idx} ---")
            if texto_limpio:
                bloques.append(texto_limpio)
            else:
                bloques.append("[Sin texto extraíble]")
        bloques.append("")

    contenido = "\n".join(bloques)
    ruta_txt.parent.mkdir(parents=True, exist_ok=True)
    ruta_txt.write_text(contenido, encoding="utf-8")
    return contenido


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "pdfs_prueba"
    salida = raiz / "salida"

    pdfs = obtener_pdfs(entrada)
    if not pdfs:
        print(
            "No hay PDFs en entrada/pdfs_prueba. "
            "Ejecuta antes cap09_crear_ejemplos.py"
        )
        return

    ruta_unido = salida / "documentos_unidos.pdf"
    tot_pags = unir_todos_los_pdfs(pdfs, ruta_unido)
    print(
        f"[1] Unidos {len(pdfs)} PDFs en "
        f"salida/{ruta_unido.name} ({tot_pags} páginas)."
    )

    ruta_primera = salida / "primera_pagina.pdf"
    separar_primera_pagina(pdfs[0], ruta_primera)
    print(
        f"[2] Extraída pág. 1 de {pdfs[0].name} en "
        f"salida/{ruta_primera.name}."
    )

    ruta_txt = salida / "texto_extraido.txt"
    texto = extraer_todo_el_texto(pdfs, ruta_txt)
    print(
        f"[3] Texto volcado en salida/{ruta_txt.name}:\n"
    )
    print(texto)


if __name__ == "__main__":
    main()
