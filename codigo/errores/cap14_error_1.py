# ERROR A PROPÓSITO (en un bucle sin pausa con clave real)
for i in range(10):
    resp = requests.post(
        URL_API, headers=cabeceras, json=carga
    )
    resp.raise_for_status()
