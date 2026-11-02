# Archivo: cap08_crear_ejemplos.py

from pathlib import Path


def crear_csv_base():
    ruta = Path.cwd() / "salida" / "resumen_gastos.csv"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    contenido = (
        "categoria,apuntes,total_euros\n"
        "Suministros,2,98.0\n"
        "Supermercado,2,82.5\n"
        "Ocio,2,27.49\n"
        "Sin categoría,1,8.0\n"
    )
    ruta.write_text(
        contenido, encoding="utf-8", newline="\n"
    )
    print(f"CSV base listo en: salida/{ruta.name}")


if __name__ == "__main__":
    crear_csv_base()
