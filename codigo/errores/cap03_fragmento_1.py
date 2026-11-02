# Fragmento ilustrativo (el programa completo va más abajo)
contador = 1
candidato = destino / archivo.name
while candidato.exists():
    nuevo_nombre = (
        f"{archivo.stem}_{contador}{archivo.suffix}"
    )
    candidato = destino / nuevo_nombre
    contador += 1
