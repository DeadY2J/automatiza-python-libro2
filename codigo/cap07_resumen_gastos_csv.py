# Archivo: cap07_resumen_gastos_csv.py

import csv
from pathlib import Path


def limpiar_importe(texto):
    if not texto:
        return 0.0
    limpio = (
        texto.replace("€", "")
        .replace(" ", "")
        .replace(",", ".")
    )
    try:
        return float(limpio)
    except ValueError:
        return 0.0


def limpiar_categoria(texto):
    if not texto or not texto.strip():
        return "Sin categoría"
    return texto.strip().capitalize()


def procesar_gastos(ruta_entrada):
    agrupado = {}
    filas_omitidas = 0

    with open(
        ruta_entrada, "r", encoding="utf-8", newline=""
    ) as f:
        lector = csv.DictReader(f)
        for fila in lector:
            importe = limpiar_importe(fila.get("importe"))
            if importe <= 0:
                filas_omitidas += 1
                continue

            cat = limpiar_categoria(fila.get("categoria"))
            if cat not in agrupado:
                agrupado[cat] = {"apuntes": 0, "total": 0.0}
            agrupado[cat]["apuntes"] += 1
            agrupado[cat]["total"] += importe

    resumen = []
    for cat, datos in agrupado.items():
        resumen.append(
            {
                "categoria": cat,
                "apuntes": datos["apuntes"],
                "total_euros": round(datos["total"], 2),
            }
        )

    resumen.sort(
        key=lambda x: x["total_euros"], reverse=True
    )
    return resumen, filas_omitidas


def guardar_resumen_csv(ruta_salida, resumen):
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    columnas = ["categoria", "apuntes", "total_euros"]
    with open(
        ruta_salida, "w", encoding="utf-8", newline=""
    ) as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resumen)


def mostrar_tabla(resumen, omitidas):
    print("=" * 50)
    print("RESUMEN MENSUAL DE GASTOS POR CATEGORÍA")
    print("=" * 50)
    total_mes = 0.0
    for fila in resumen:
        cat = fila["categoria"]
        ap = fila["apuntes"]
        imp = fila["total_euros"]
        total_mes += imp
        print(
            f"  {cat:<16} | {ap} apunte(s) | "
            f"{imp:>7.2f} EUR"
        )
    print("-" * 50)
    print(
        f"  TOTAL DEL MES:               "
        f"{total_mes:>7.2f} EUR"
    )
    print(f"  Filas sin importe omitidas:  {omitidas}")
    print("=" * 50)


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "gastos_mes_sucios.csv"
    salida = raiz / "salida" / "resumen_gastos.csv"

    if not entrada.exists():
        print(
            "No existe entrada/gastos_mes_sucios.csv. "
            "Ejecuta antes cap07_crear_ejemplos.py"
        )
        return

    resumen, omitidas = procesar_gastos(entrada)
    mostrar_tabla(resumen, omitidas)
    guardar_resumen_csv(salida, resumen)
    print(f"\nGuardado en: salida/{salida.name}")


if __name__ == "__main__":
    main()
