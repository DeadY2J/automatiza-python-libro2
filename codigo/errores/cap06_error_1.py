# ERROR A PROPÓSITO
from pathlib import Path
import zipfile

origen = Path("entrada/proyecto_activo")
ruta_zip = origen / "mi_copia.zip"

with zipfile.ZipFile(ruta_zip, "w") as zf:
    for p in origen.rglob("*"):
        if p.is_file():
            zf.write(p, arcname=p.relative_to(origen))
