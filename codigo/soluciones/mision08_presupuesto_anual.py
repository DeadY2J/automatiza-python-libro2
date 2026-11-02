# Archivo: mision08_presupuesto_anual.py

from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font

FORMATO_EURO = '#,##0.00 "€"'
DATOS = [
    ("T1", 12500, 9800),
    ("T2", 13200, 10100),
    ("T3", 11800, 9900),
    ("T4", 15400, 11200),
]


def crear_presupuesto(datos):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trimestres"
    ws.append(
        ["Trimestre", "Ingresos", "Gastos", "Beneficio"]
    )
    for celda in ws[1]:
        celda.font = Font(bold=True)

    for idx, (trim, ingresos, gastos) in enumerate(
        datos, start=2
    ):
        beneficio = f"=B{idx}-C{idx}"
        ws.append([trim, ingresos, gastos, beneficio])

    ultima = len(datos) + 1
    fila_tot = ultima + 1
    ws.cell(row=fila_tot, column=1, value="TOTAL")
    for col in "BCD":
        formula = f"=SUM({col}2:{col}{ultima})"
        ws[f"{col}{fila_tot}"] = formula
    for celda in ws[fila_tot]:
        celda.font = Font(bold=True)

    for fila in ws.iter_rows(
        min_row=2, max_row=fila_tot, min_col=2, max_col=4
    ):
        for celda in fila:
            celda.number_format = FORMATO_EURO
    for col in "ABCD":
        ws.column_dimensions[col].width = 14
    return wb


def main():
    ruta = Path.cwd() / "salida" / "presupuesto_anual.xlsx"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    wb = crear_presupuesto(DATOS)
    wb.save(ruta)
    ws = wb["Trimestres"]
    print(f"Creado: salida/{ruta.name}")
    print("Fórmulas de la columna Beneficio:")
    for fila in ws.iter_rows(min_row=2, values_only=True):
        print(f"  {fila[0]:<6} {fila[3]}")


if __name__ == "__main__":
    main()
