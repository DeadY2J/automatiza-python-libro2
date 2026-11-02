# Archivo: mision09_buscador_pdf.py

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def texto_completo(ruta):
    lector = PdfReader(ruta)
    return "\n".join(
        (p.extract_text() or "") for p in lector.pages
    )


def importe_total(texto):
    for linea in texto.splitlines():
        if linea.startswith("Total: "):
            limpio = (
                linea.replace("Total:", "")
                .replace("EUR", "")
                .strip()
            )
            try:
                return float(limpio)
            except ValueError:
                return 0.0
    return 0.0


def main():
    raiz = Path.cwd()
    carpeta = raiz / "entrada" / "pdfs_prueba"
    salida = raiz / "salida" / "solo_facturas.pdf"
    pdfs = sorted(carpeta.glob("*.pdf"))
    if not pdfs:
        print(
            "No hay PDFs en entrada/pdfs_prueba. "
            "Ejecuta antes cap09_crear_ejemplos.py"
        )
        return

    escritor = PdfWriter()
    suma = 0.0
    facturas = 0
    for ruta in pdfs:
        texto = texto_completo(ruta)
        if "FACTURA" not in texto:
            print(f"  Omitido:  {ruta.name}")
            continue
        importe = importe_total(texto)
        suma += importe
        facturas += 1
        escritor.append(ruta)
        print(
            f"  Factura:  {ruta.name} ({importe:.2f} EUR)"
        )

    if facturas:
        salida.parent.mkdir(parents=True, exist_ok=True)
        with open(salida, "wb") as f:
            escritor.write(f)
    print(f"\nFacturas encontradas: {facturas}")
    print(f"Importe total:        {suma:.2f} EUR")
    print(f"Unidas en:            salida/{salida.name}")


if __name__ == "__main__":
    main()
