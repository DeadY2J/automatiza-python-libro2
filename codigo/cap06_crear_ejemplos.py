# Archivo: cap06_crear_ejemplos.py

from pathlib import Path
import zipfile


def preparar_escenario_backup():
    raiz = Path.cwd()
    origen = raiz / "entrada" / "proyecto_activo"
    sub = origen / "capitulos"
    destino = raiz / "copias" / "backups_proyecto"

    sub.mkdir(parents=True, exist_ok=True)
    destino.mkdir(parents=True, exist_ok=True)

    (origen / "notas.txt").write_text(
        "Ideas principales del guion.\n" * 20,
        encoding="utf-8",
        newline="\n",
    )
    (sub / "borrador_01.md").write_text(
        "# Capítulo 1\nTexto de prueba.\n" * 30,
        encoding="utf-8",
        newline="\n",
    )
    (sub / "presupuesto.csv").write_text(
        "concepto,importe\nServidor,45\nDominio,12\n",
        encoding="utf-8",
        newline="\n",
    )

    fechas_viejas = [
        "2026-01-10_090000",
        "2026-01-15_090000",
        "2026-01-20_090000",
        "2026-01-25_090000",
    ]
    for marca in fechas_viejas:
        ruta_zip = destino / f"backup_{marca}.zip"
        with zipfile.ZipFile(
            ruta_zip, "w", zipfile.ZIP_DEFLATED
        ) as zf:
            zf.writestr("info.txt", f"Copia de {marca}\n")

    print(
        "Escenario listo: 3 archivos en proyecto_activo y "
        "4 backups antiguos."
    )


if __name__ == "__main__":
    preparar_escenario_backup()
