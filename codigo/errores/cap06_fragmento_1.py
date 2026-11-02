# Fragmento ilustrativo (el programa completo va más abajo)
from pathlib import Path
import zipfile

origen = Path("entrada/proyecto_activo")
destino_zip = Path("copias/backup_20260315.zip")

with zipfile.ZipFile(
    destino_zip, "w", zipfile.ZIP_DEFLATED
) as archivo_zip:
    for ruta in origen.rglob("*"):
        if ruta.is_file():
            ruta_interna = ruta.relative_to(origen)
            archivo_zip.write(ruta, arcname=ruta_interna)
