# Fragmento ilustrativo (el programa completo va más abajo)
from pathlib import Path

carpeta = Path("entrada/almacen_prueba")
for elemento in carpeta.rglob("*"):
    if elemento.is_file():
        tamano = elemento.stat().st_size
        print(elemento.name, tamano)
