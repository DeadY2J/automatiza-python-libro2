# Fragmento ilustrativo (el programa completo va más abajo)
from datetime import datetime
from pathlib import Path

ruta = Path("entrada/fotos_desordenadas/IMG_4829.jpg")
segundos = ruta.stat().st_mtime
fecha = datetime.fromtimestamp(segundos)

carpeta_mes = fecha.strftime("%Y/%Y-%m")
prefijo_dia = fecha.strftime("%Y-%m-%d")
print(carpeta_mes, prefijo_dia)
