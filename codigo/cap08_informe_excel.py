# Archivo: cap08_informe_excel.py

import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill

FORMATO_EURO = '#,##0.00 "€"'


def leer_datos_csv(ruta_csv):
    filas = []
    with open(
        ruta_csv, "r", encoding="utf-8", newline=""
    ) as f:
        lector = csv.DictReader(f)
        for fila in lector:
            filas.append(
                {
                    "categoria": fila["categoria"],
                    "apuntes": int(fila["apuntes"]),
                    "total_euros": float(
                        fila["total_euros"]
                    ),
                }
            )
    return filas


def crear_hoja_detalle(wb, datos):
    ws = wb.active
    ws.title = "Detalle"
    ws.append(["Categoría", "Apuntes", "Total Euros"])

    fuente_cab = Font(
        name="Calibri", size=11, bold=True, color="FFFFFF"
    )
    fondo_cab = PatternFill(
        start_color="1F4E78",
        end_color="1F4E78",
        fill_type="solid",
    )
    centrado = Alignment(
        horizontal="center", vertical="center"
    )

    for col_idx in range(1, 4):
        celda = ws.cell(row=1, column=col_idx)
        celda.font = fuente_cab
        celda.fill = fondo_cab
        if col_idx > 1:
            celda.alignment = centrado

    for idx, item in enumerate(datos, start=2):
        ws.append(
            [
                item["categoria"],
                item["apuntes"],
                item["total_euros"],
            ]
        )
        ws.cell(row=idx, column=2).alignment = centrado
        c_euro = ws.cell(row=idx, column=3)
        c_euro.number_format = FORMATO_EURO

    ult_dato = len(datos) + 1
    fila_tot = ult_dato + 1
    ws.cell(row=fila_tot, column=1, value="TOTAL")
    ws.cell(
        row=fila_tot,
        column=2,
        value=f"=SUM(B2:B{ult_dato})",
    )
    ws.cell(
        row=fila_tot,
        column=3,
        value=f"=SUM(C2:C{ult_dato})",
    )

    negrita = Font(name="Calibri", size=11, bold=True)
    for col_idx in range(1, 4):
        c_tot = ws.cell(row=fila_tot, column=col_idx)
        c_tot.font = negrita
    ws.cell(row=fila_tot, column=2).alignment = centrado
    ws.cell(row=fila_tot, column=3).number_format = (
        FORMATO_EURO
    )

    for col in ws.columns:
        largo = max(
            len(str(c.value or "")) for c in col
        )
        letra = col[0].column_letter
        ws.column_dimensions[letra].width = max(
            largo + 4, 15
        )

    return ult_dato


def agregar_grafico(ws, ult_dato):
    grafico = BarChart()
    grafico.type = "col"
    grafico.style = 10
    grafico.title = "Gasto por Categoría"
    grafico.y_axis.title = "Euros"
    grafico.x_axis.title = "Categoría"

    ref_datos = Reference(
        ws, min_col=3, min_row=1, max_row=ult_dato
    )
    ref_cats = Reference(
        ws, min_col=1, min_row=2, max_row=ult_dato
    )
    grafico.add_data(ref_datos, titles_from_data=True)
    grafico.set_categories(ref_cats)
    grafico.legend = None
    ws.add_chart(grafico, "E2")


def crear_hoja_resumen(wb, ult_dato):
    ws = wb.create_sheet(title="Resumen")
    ws["A1"] = "RESUMEN EJECUTIVO DEL MES"
    ws["A1"].font = Font(
        name="Calibri", size=13, bold=True, color="1F4E78"
    )

    fila_tot = ult_dato + 1
    ws["A3"] = "Gasto total mensual:"
    ws["B3"] = f"=Detalle!C{fila_tot}"
    ws["B3"].font = Font(bold=True)
    ws["B3"].number_format = FORMATO_EURO

    ws["A4"] = "Media por categoría:"
    ws["B4"] = f"=AVERAGE(Detalle!C2:C{ult_dato})"
    ws["B4"].number_format = FORMATO_EURO

    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 16


def main():
    raiz = Path.cwd()
    ruta_csv = raiz / "salida" / "resumen_gastos.csv"
    ruta_xlsx = raiz / "salida" / "informe_mensual.xlsx"

    if not ruta_csv.exists():
        print(
            "No existe salida/resumen_gastos.csv. "
            "Ejecuta antes cap08_crear_ejemplos.py"
        )
        return

    datos = leer_datos_csv(ruta_csv)
    wb = Workbook()
    ult_dato = crear_hoja_detalle(wb, datos)
    agregar_grafico(wb["Detalle"], ult_dato)
    crear_hoja_resumen(wb, ult_dato)

    ruta_xlsx.parent.mkdir(parents=True, exist_ok=True)
    wb.save(ruta_xlsx)
    print(f"Libro Excel creado: salida/{ruta_xlsx.name}")
    print(
        f"Pestañas: {', '.join(wb.sheetnames)} "
        f"({len(datos)} categorías procesadas)."
    )


if __name__ == "__main__":
    main()
