# Archivo: cap18_crear_ejemplos.py

import json
from pathlib import Path
import zipfile

BASE = Path(__file__).resolve().parent


def preparar_escenario_mayordomo():
    entrada = BASE / "entrada"
    descargas = entrada / "descargas_mayordomo"
    trabajo = entrada / "trabajo_mayordomo"
    backups = BASE / "copias" / "mayordomo_backups"

    for c in [descargas, trabajo, backups]:
        c.mkdir(parents=True, exist_ok=True)

    config = {
        "latitud": 42.603,
        "longitud": -8.644,
        "max_copias": 2,
        "categorias": {
            ".pdf": "Documentos",
            ".txt": "Documentos",
            ".jpg": "Imagenes",
            ".png": "Imagenes",
            ".csv": "Datos",
        },
    }
    ruta_cfg = entrada / "mayordomo_config.json"
    ruta_cfg.write_text(
        json.dumps(config, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    muestras_desc = [
        ("recibo_luz.pdf", "PDF simulado"),
        ("captura_pantalla.png", "PNG simulado"),
        ("gastos_abril.csv", "concepto,euros\ncafe,1.50"),
        ("instalador_viejo.zip", "ZIP suelto"),
    ]
    for nom, txt in muestras_desc:
        (descargas / nom).write_text(
            txt, encoding="utf-8", newline="\n"
        )

    (trabajo / "guion_libro.md").write_text(
        "# Borrador activo\n",
        encoding="utf-8",
        newline="\n",
    )
    (trabajo / "clientes.csv").write_text(
        "id,nombre\n1,Taller\n",
        encoding="utf-8",
        newline="\n",
    )

    for fecha in ["2026-02-01_080000", "2026-02-02_080000"]:
        zpath = backups / f"backup_{fecha}.zip"
        with zipfile.ZipFile(zpath, "w") as zf:
            zf.writestr("nota.txt", fecha)

    print("Escenario de El Mayordomo listo para probar.")


if __name__ == "__main__":
    preparar_escenario_mayordomo()
