# Archivo: cap15_el_escriba.py

from datetime import datetime
import os
from pathlib import Path
import time
from pypdf import PdfReader
import requests

URL_API = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/openai/chat/completions"
)
MODELO = "gemini-3.6-flash"
EXTENSIONES = {".txt", ".md", ".pdf"}
MAX_CARACTERES = 3500


def leer_documento(ruta):
    ext = ruta.suffix.lower()
    if ext in {".txt", ".md"}:
        return ruta.read_text(encoding="utf-8").strip()

    if ext == ".pdf":
        lector = PdfReader(ruta)
        trozos = []
        for pag in lector.pages:
            txt = pag.extract_text() or ""
            if txt.strip():
                trozos.append(txt.strip())
        return "\n".join(trozos).strip()

    return ""


def resumen_local_prueba(texto):
    lineas = [
        lin.lstrip("# ").strip()
        for lin in texto.splitlines()
        if lin.strip()
    ]
    seleccion = lineas[:3]
    vinetas = [f"- {lin}" for lin in seleccion]
    vinetas.append(
        f"- *(Resumen en modo prueba: "
        f"{len(texto)} caracteres leídos)*"
    )
    return "\n".join(vinetas)


def resumir_con_ia(nombre_archivo, texto):
    recortado = texto[:MAX_CARACTERES]
    clave = os.getenv("GEMINI_API_KEY", "").strip()
    if not clave:
        return resumen_local_prueba(recortado), True

    instruccion = (
        "Eres El Escriba, un asistente documental preciso. "
        "Resume el siguiente documento en 3 viñetas cortas "
        "en español destacando fechas, importes o tareas."
    )
    cabeceras = {
        "Authorization": f"Bearer {clave}",
        "Content-Type": "application/json",
    }
    carga = {
        "model": MODELO,
        "messages": [
            {"role": "system", "content": instruccion},
            {
                "role": "user",
                "content": (
                    f"Archivo: {nombre_archivo}\n\n"
                    f"{recortado}"
                ),
            },
        ],
        "temperature": 0.2,
    }
    try:
        resp = requests.post(
            URL_API,
            headers=cabeceras,
            json=carga,
            timeout=30,
        )
        resp.raise_for_status()
        datos = resp.json()
        resumen = (
            datos["choices"][0]["message"]["content"]
        )
        return resumen.strip(), False
    except (
        requests.RequestException,
        KeyError,
        IndexError,
    ) as err:
        print(f"  [AVISO API] {nombre_archivo}: {err}")
        return resumen_local_prueba(recortado), True


def procesar_carpeta(carpeta_entrada):
    archivos = sorted(
        p
        for p in carpeta_entrada.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONES
    )
    resultados = []

    for idx, ruta in enumerate(archivos):
        print(f"Leyendo: {ruta.name}...")
        texto = leer_documento(ruta)
        if not texto:
            resumen = "- *[Documento sin texto extraíble]*"
            modo_prueba = True
        else:
            resumen, modo_prueba = resumir_con_ia(
                ruta.name, texto
            )
            if not modo_prueba and idx < len(archivos) - 1:
                time.sleep(2)

        resultados.append(
            {
                "nombre": ruta.name,
                "caracteres": len(texto),
                "resumen": resumen,
                "prueba": modo_prueba,
            }
        )
    return resultados


def construir_markdown(resultados):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = [
        "# Informe de El Escriba",
        f"\n*Generado el: {fecha}*",
        f"*Documentos procesados: {len(resultados)}*\n",
        "## Índice de documentos",
    ]
    for item in resultados:
        lineas.append(
            f"- **{item['nombre']}** "
            f"({item['caracteres']} caracteres)"
        )

    lineas.append("\n---")
    for item in resultados:
        lineas.append(f"\n## {item['nombre']}\n")
        lineas.append(item["resumen"])

    return "\n".join(lineas) + "\n"


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "documentos_escriba"
    salida = raiz / "salida" / "informe_escriba.md"

    if not entrada.exists():
        print(
            "No existe entrada/documentos_escriba. "
            "Ejecuta antes cap15_crear_ejemplos.py"
        )
        return

    print("=" * 54)
    print("EL ESCRIBA: RESUMIDOR DOCUMENTAL EN MARCHA")
    print("=" * 54)

    resultados = procesar_carpeta(entrada)
    if not resultados:
        print("No se encontraron documentos compatibles.")
        return

    informe_md = construir_markdown(resultados)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(informe_md, encoding="utf-8")

    print("=" * 54)
    print(f"Informe creado en: salida/{salida.name}\n")
    print(informe_md)


if __name__ == "__main__":
    main()
