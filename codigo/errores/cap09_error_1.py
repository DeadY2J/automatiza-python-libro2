# ERROR A PROPÓSITO
from pypdf import PdfReader

ruta = "entrada/pdfs_prueba/01_factura_enero.pdf"
lector = PdfReader(ruta)
cantidad = lector.getNumPages()
