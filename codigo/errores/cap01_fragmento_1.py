min_por_semana = (
    tarea["veces_semana"] * tarea["minutos_manual"]
)
if min_por_semana > 0:
    semanas_retorno = (
        tarea["minutos_crear"] / min_por_semana
    )
else:
    semanas_retorno = 999.0
