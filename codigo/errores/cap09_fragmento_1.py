# Fragmento ilustrativo (el programa completo va más abajo)
from pypdf import PdfReader, PdfWriter

lector = PdfReader("entrada/pdfs_prueba/doc1.pdf")
primera_pagina = lector.pages[0]
print(primera_pagina.extract_text())

escritor = PdfWriter()
escritor.add_page(primera_pagina)
with open("salida/recorte.pdf", "wb") as f:
    escritor.write(f)
