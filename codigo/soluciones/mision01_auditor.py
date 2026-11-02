# Archivo: mision01_auditor.py

SEMANAS_ANIO = 52
RECARGO_ERRORES = 1.25


def evaluar_tarea(tarea):
    veces_anio = tarea["veces_semana"] * SEMANAS_ANIO
    min_anuales = veces_anio * tarea["minutos_manual"]
    if tarea.get("propensa_a_errores", False):
        min_anuales = min_anuales * RECARGO_ERRORES
    coste_min = (
        tarea["minutos_crear"]
        + tarea["minutos_mantenimiento_anual"]
    )
    horas_ahorro = (min_anuales - coste_min) / 60

    if horas_ahorro >= 5:
        veredicto = "AUTOMATIZAR YA"
    elif horas_ahorro >= 1:
        veredicto = "COMPENSA"
    else:
        veredicto = "MEJOR A MANO"

    return {
        "nombre": tarea["nombre"],
        "propensa": tarea.get("propensa_a_errores", False),
        "horas_manual": round(min_anuales / 60, 1),
        "horas_ahorro": round(horas_ahorro, 1),
        "veredicto": veredicto,
    }


def total_rentable(resultados):
    rentables = [
        r["horas_ahorro"]
        for r in resultados
        if r["veredicto"] in ("AUTOMATIZAR YA", "COMPENSA")
    ]
    return round(sum(rentables), 1)


def mostrar_informe(resultados):
    print("=" * 50)
    print("AUDITORÍA DE RUTINAS")
    print("=" * 50)
    for res in resultados:
        marca = ""
        if res["propensa"]:
            marca = " (+25 % por errores)"
        print(f"\n{res['nombre']}{marca}")
        print(f"  A mano al año:  {res['horas_manual']} h")
        print(f"  Ahorro neto:    {res['horas_ahorro']} h")
        print(f"  Veredicto:      {res['veredicto']}")
    print("\n" + "=" * 50)
    total = total_rentable(resultados)
    print(f"Horas recuperables (rentables): {total} h")


def main():
    tareas = [
        {
            "nombre": "Copiar importes del banco",
            "veces_semana": 1,
            "minutos_manual": 20,
            "minutos_crear": 120,
            "minutos_mantenimiento_anual": 30,
            "propensa_a_errores": True,
        },
        {
            "nombre": "Renombrar facturas del mes",
            "veces_semana": 0.25,
            "minutos_manual": 30,
            "minutos_crear": 60,
            "minutos_mantenimiento_anual": 15,
            "propensa_a_errores": True,
        },
        {
            "nombre": "Revisar espacio del disco",
            "veces_semana": 0.5,
            "minutos_manual": 4,
            "minutos_crear": 30,
            "minutos_mantenimiento_anual": 10,
            "propensa_a_errores": True,
        },
        {
            "nombre": "Felicitar cumpleaños del clan",
            "veces_semana": 0.1,
            "minutos_manual": 3,
            "minutos_crear": 90,
            "minutos_mantenimiento_anual": 20,
            "propensa_a_errores": False,
        },
    ]
    resultados = [evaluar_tarea(t) for t in tareas]
    resultados.sort(
        key=lambda r: r["horas_ahorro"], reverse=True
    )
    mostrar_informe(resultados)


if __name__ == "__main__":
    main()
