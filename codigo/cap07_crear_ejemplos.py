# Archivo: cap07_crear_ejemplos.py

from pathlib import Path


def crear_csv_ejemplos():
    carpeta = Path.cwd() / "entrada"
    carpeta.mkdir(parents=True, exist_ok=True)

    juegos_txt = (
        "titulo,sistema,anio,prestado_a,valor_euros\n"
        "The Secret of Monkey Island,PC,1990,Nadie,45.00\n"
        "Streets of Rage 2,Mega Drive,1992,Carlos,38.50\n"
        "Super Mario World,SNES,1990,Nadie,50.00\n"
        "Castlevania Symphony,PlayStation,1997,"
        "Lucía,85.00\n"
        "Sonic the Hedgehog,Mega Drive,1991,Carlos,25.00\n"
    )
    (carpeta / "coleccion_juegos.csv").write_text(
        juegos_txt, encoding="utf-8", newline="\n"
    )

    gastos_sucios = (
        "fecha,concepto,categoria,importe\n"
        "2026-03-01,Compra semanal,Supermercado,64.20\n"
        '2026-03-03,Fibra y móvil, suministros ,"42,90 €"\n'
        "2026-03-05,Verduras y fruta,supermercado, 18.30 \n"
        "2026-03-08,Suscripción música,OCIO,10.99\n"
        "2026-03-10,Factura luz,Suministros,55.10\n"
        "2026-03-12,Anulación cargo,Ocio,pendiente\n"
        '2026-03-14,Cine viernes,ocio,"16,50"\n'
        "2026-03-15,Pilas mando,,8.00\n"
    )
    (carpeta / "gastos_mes_sucios.csv").write_text(
        gastos_sucios, encoding="utf-8", newline="\n"
    )

    print(
        "Archivos creados en entrada/: "
        "coleccion_juegos.csv y gastos_mes_sucios.csv"
    )


if __name__ == "__main__":
    crear_csv_ejemplos()
