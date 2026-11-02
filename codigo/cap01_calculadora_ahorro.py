# Archivo: cap01_calculadora_ahorro.py

SEMANAS_ANIO = 52


def evaluar_tarea(tarea):
    veces_anio = tarea["veces_semana"] * SEMANAS_ANIO
    min_anuales = veces_anio * tarea["minutos_manual"]
    coste_min = (
        tarea["minutos_crear"]
        + tarea["minutos_mantenimiento_anual"]
    )
    ahorro_min = min_anuales - coste_min

    horas_manual = min_anuales / 60
    horas_ahorro = ahorro_min / 60

    min_por_semana = (
        tarea["veces_semana"] * tarea["minutos_manual"]
    )
    if min_por_semana > 0:
        semanas_retorno = (
            tarea["minutos_crear"] / min_por_semana
        )
    else:
        semanas_retorno = 999.0

    if horas_ahorro >= 5:
        veredicto = "AUTOMATIZAR YA"
    elif horas_ahorro >= 1:
        veredicto = "COMPENSA"
    else:
        veredicto = "MEJOR A MANO"

    return {
        "nombre": tarea["nombre"],
        "horas_manual": round(horas_manual, 1),
        "horas_ahorro": round(horas_ahorro, 1),
        "semanas_retorno": round(semanas_retorno, 1),
        "veredicto": veredicto,
    }


def mostrar_informe(resultados):
    print("=" * 56)
    print("INFORME DE RENTABILIDAD DE AUTOMATIZACIÓN")
    print("=" * 56)

    for res in resultados:
        print(f"\nTarea: {res['nombre']}")
        print(
            f"  Tiempo anual a mano: "
            f"{res['horas_manual']} h"
        )
        print(
            f"  Ahorro neto año 1:   "
            f"{res['horas_ahorro']} h"
        )
        print(
            f"  Amortizado en:       "
            f"{res['semanas_retorno']} semanas"
        )
        print(f"  Veredicto:           {res['veredicto']}")

    print("\n" + "=" * 56)


def main():
    tareas_candidatas = [
        {
            "nombre": "Ordenar Descargas y facturas",
            "veces_semana": 5,
            "minutos_manual": 8,
            "minutos_crear": 60,
            "minutos_mantenimiento_anual": 15,
        },
        {
            "nombre": "Informe Excel de gastos",
            "veces_semana": 1,
            "minutos_manual": 25,
            "minutos_crear": 90,
            "minutos_mantenimiento_anual": 30,
        },
        {
            "nombre": "Copia zip de proyectos",
            "veces_semana": 2,
            "minutos_manual": 5,
            "minutos_crear": 45,
            "minutos_mantenimiento_anual": 10,
        },
        {
            "nombre": "Convertir logo anual en web",
            "veces_semana": 0.02,
            "minutos_manual": 15,
            "minutos_crear": 120,
            "minutos_mantenimiento_anual": 60,
        },
    ]

    evaluadas = [
        evaluar_tarea(t) for t in tareas_candidatas
    ]
    ordenadas = sorted(
        evaluadas,
        key=lambda x: x["horas_ahorro"],
        reverse=True,
    )
    mostrar_informe(ordenadas)


if __name__ == "__main__":
    main()
