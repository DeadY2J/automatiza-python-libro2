# Archivo: mision14_clasificador_notas.py

from pathlib import Path
from cap14_cliente_ia import consultar_ia

NOTAS = [
    "La factura del alquiler del local vence mañana.",
    "Idea: leer en verano un libro sobre domótica.",
    "Aviso: se ha caído el servidor de la web.",
]
ETIQUETAS = ("URGENTE", "NORMAL", "IDEA")
INSTRUCCION = (
    "Clasifica el texto del usuario con una sola "
    "palabra: URGENTE, NORMAL o IDEA. Después escribe "
    "' - ' y un motivo de menos de diez palabras. "
    "Responde en una sola línea."
)


def clasificar_local(texto):
    minus = texto.lower()
    if "vence" in minus or "caído" in minus:
        return "URGENTE - Hay un plazo o una avería."
    if "idea" in minus:
        return "IDEA - El propio texto lo dice."
    return "NORMAL - Sin señales de urgencia."


def normalizar(respuesta):
    lineas = respuesta.strip().splitlines()
    linea = lineas[0].strip() if lineas else ""
    if linea.upper().startswith(ETIQUETAS):
        return linea
    return f"NORMAL - Respuesta no reconocida: {linea[:30]}"


def clasificar(texto):
    respuesta, es_prueba = consultar_ia(INSTRUCCION, texto)
    if es_prueba:
        return clasificar_local(texto), True
    return normalizar(respuesta), False


def main():
    filas = []
    alguna_prueba = False
    for num, nota in enumerate(NOTAS, start=1):
        resultado, es_prueba = clasificar(nota)
        alguna_prueba = alguna_prueba or es_prueba
        filas.append(f"{num} | {resultado} | {nota}")

    origen = "respaldo local" if alguna_prueba else "IA"
    tabla = [
        f"Notas clasificadas ({origen})",
        "N | Clasificación | Nota",
    ] + filas
    texto = "\n".join(tabla) + "\n"

    ruta = Path.cwd() / "salida" / "notas_clasificadas.txt"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    print()
    print(texto, end="")
    print(f"\nGuardado en: salida/{ruta.name}")


if __name__ == "__main__":
    main()
