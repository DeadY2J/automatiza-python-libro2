"""Pruebas de los capítulos 07 a 10 (datos)."""

from openpyxl import load_workbook
from PIL import Image

import cap07_crear_ejemplos as cap07e
import cap07_resumen_gastos_csv as cap07
import cap08_crear_ejemplos as cap08e
import cap08_informe_excel as cap08
import cap09_crear_ejemplos as cap09e
import cap09_herramientas_pdf as cap09
import cap10_crear_ejemplos as cap10e
import cap10_procesar_imagenes as cap10


def test_limpiar_importe():
    assert cap07.limpiar_importe("42,90 €") == 42.9
    assert cap07.limpiar_importe(" 18.30 ") == 18.3
    assert cap07.limpiar_importe("pendiente") == 0.0
    assert cap07.limpiar_importe("") == 0.0
    assert cap07.limpiar_importe(None) == 0.0


def test_limpiar_categoria():
    assert cap07.limpiar_categoria(" suministros ") == (
        "Suministros"
    )
    assert cap07.limpiar_categoria("OCIO") == "Ocio"
    assert cap07.limpiar_categoria("  ") == "Sin categoría"


def test_resumen_gastos_del_libro(taller):
    cap07e.crear_csv_ejemplos()
    entrada = taller / "entrada" / "gastos_mes_sucios.csv"
    resumen, omitidas = cap07.procesar_gastos(entrada)
    assert omitidas == 1
    assert [
        (f["categoria"], f["total_euros"]) for f in resumen
    ] == [
        ("Suministros", 98.0),
        ("Supermercado", 82.5),
        ("Ocio", 27.49),
        ("Sin categoría", 8.0),
    ]
    salida = taller / "salida" / "resumen.csv"
    cap07.guardar_resumen_csv(salida, resumen)
    lineas = salida.read_text(encoding="utf-8").splitlines()
    assert lineas[0] == "categoria,apuntes,total_euros"
    assert lineas[1] == "Suministros,2,98.0"


def test_informe_excel(taller):
    cap08e.crear_csv_base()
    cap08.main()
    ruta = taller / "salida" / "informe_mensual.xlsx"
    wb = load_workbook(ruta)
    assert wb.sheetnames == ["Detalle", "Resumen"]
    det = wb["Detalle"]
    assert det["A6"].value == "TOTAL"
    assert det["B6"].value == "=SUM(B2:B5)"
    assert det["C6"].value == "=SUM(C2:C5)"
    assert det["C2"].value == 98.0
    assert det["A1"].fill.start_color.rgb.endswith("1F4E78")
    assert len(det._charts) == 1
    res = wb["Resumen"]
    assert res["B3"].value == "=Detalle!C6"
    assert res["B4"].value == "=AVERAGE(Detalle!C2:C5)"


def test_pdf_minimo_y_herramientas(taller):
    cap09e.main()
    entrada = taller / "entrada" / "pdfs_prueba"
    pdfs = cap09.obtener_pdfs(entrada)
    assert [p.name for p in pdfs] == [
        "01_factura_enero.pdf",
        "02_factura_febrero.pdf",
        "03_albaran_entrega.pdf",
    ]
    unido = taller / "salida" / "unido.pdf"
    assert cap09.unir_todos_los_pdfs(pdfs, unido) == 4
    primera = taller / "salida" / "primera.pdf"
    assert cap09.separar_primera_pagina(pdfs[0], primera)
    txt = taller / "salida" / "texto.txt"
    texto = cap09.extraer_todo_el_texto(pdfs, txt)
    assert "Total: 95.50 EUR" in texto
    assert "Caja revisada sin daños." in texto


def test_imagenes_en_lote(taller):
    cap10e.crear_imagenes_prueba()
    origen = taller / "entrada" / "imagenes_bruto"
    destino = taller / "salida" / "imagenes_listas"
    destino.mkdir(parents=True)
    tamanos = {}
    for ruta in cap10.obtener_imagenes(origen):
        _, despues, nombre, peso = (
            cap10.procesar_una_imagen(ruta, destino)
        )
        tamanos[nombre] = despues
        assert peso > 0
    assert tamanos == {
        "01_arcade_horizontal.jpg": (800, 450),
        "02_cartucho_vertical.jpg": (600, 800),
        "03_ficha_cuadrada.jpg": (800, 800),
        "04_icono_pequeno.jpg": (400, 300),
    }
    with Image.open(destino / "04_icono_pequeno.jpg") as img:
        assert img.mode == "RGB"
        # La esquina inferior derecha lleva la caja oscura.
        assert max(img.getpixel((390, 290))) < 60
