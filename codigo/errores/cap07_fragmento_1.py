# Fragmento ilustrativo (el programa completo va más abajo)
import csv
from pathlib import Path

ruta = Path("entrada/coleccion_juegos.csv")
with open(ruta, "r", encoding="utf-8", newline="") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        print(fila["titulo"], fila["sistema"])
