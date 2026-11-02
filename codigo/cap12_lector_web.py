# Archivo: cap12_lector_web.py

import csv
from pathlib import Path
import sys
import time
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import requests

URL_PRACTICA = "https://books.toscrape.com/"
AGENTE = "TallerPythonLibro2/1.0 (Educativo)"


def permiso_robots(url_base, agente):
    url_robots = url_base.rstrip("/") + "/robots.txt"
    try:
        resp = requests.get(
            url_robots,
            headers={"User-Agent": agente},
            timeout=5,
        )
        if resp.status_code == 404:
            return True
        resp.raise_for_status()
        rp = RobotFileParser()
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(agente, url_base)
    except requests.RequestException:
        return True


def obtener_html(usar_web, ruta_local):
    if usar_web:
        print(f"Comprobando normas en {URL_PRACTICA}...")
        if not permiso_robots(URL_PRACTICA, AGENTE):
            print(
                "[AVISO] robots.txt no autoriza el acceso."
            )
        else:
            try:
                time.sleep(1.5)
                resp = requests.get(
                    URL_PRACTICA,
                    headers={"User-Agent": AGENTE},
                    timeout=10,
                )
                resp.raise_for_status()
                resp.encoding = "utf-8"
                return resp.text, "WEB EN VIVO"
            except requests.RequestException as err:
                print(f"[AVISO RED] Fallo web: {err}")
                print(
                    "Usando catálogo local de respaldo.\n"
                )

    if not ruta_local.exists():
        return "", "SIN ARCHIVO"
    texto = ruta_local.read_text(encoding="utf-8")
    return texto, "ARCHIVO LOCAL"


def extraer_productos(html, limite=5):
    sopa = BeautifulSoup(html, "html.parser")
    tarjetas = sopa.select("article.product_pod")
    productos = []

    for item in tarjetas[:limite]:
        enlace = item.select_one("h3 a")
        nodo_precio = item.select_one("p.price_color")
        nodo_stock = item.select_one("p.availability")

        if enlace and enlace.has_attr("title"):
            titulo = enlace["title"].strip()
        elif enlace:
            titulo = enlace.get_text(strip=True)
        else:
            titulo = "Sin título"

        precio_txt = (
            nodo_precio.get_text(strip=True)
            if nodo_precio
            else "0"
        )
        limpio = (
            precio_txt.replace("€", "")
            .replace("£", "")
            .strip()
        )
        try:
            precio = float(limpio)
        except ValueError:
            precio = 0.0

        stock = (
            nodo_stock.get_text(strip=True)
            if nodo_stock
            else "Desconocido"
        )

        productos.append(
            {
                "titulo": titulo,
                "precio": precio,
                "stock": stock,
            }
        )
    return productos


def guardar_y_mostrar(productos, origen, ruta_csv):
    print("=" * 56)
    print(f"PRODUCTOS EXTRAÍDOS ({origen})")
    print("=" * 56)
    for p in productos:
        print(
            f"  - {p['titulo'][:30]:<30} | "
            f"{p['precio']:>6.2f} | {p['stock']}"
        )
    print("=" * 56)

    ruta_csv.parent.mkdir(parents=True, exist_ok=True)
    cols = ["titulo", "precio", "stock"]
    with open(
        ruta_csv, "w", encoding="utf-8", newline=""
    ) as f:
        esc = csv.DictWriter(f, fieldnames=cols)
        esc.writeheader()
        esc.writerows(productos)


def main():
    usar_web = "--web" in sys.argv[1:]
    raiz = Path.cwd()
    local = raiz / "entrada" / "catalogo_retro.html"
    salida = raiz / "salida" / "productos_extraidos.csv"

    html, origen = obtener_html(usar_web, local)
    if not html:
        print(
            "No existe entrada/catalogo_retro.html. "
            "Ejecuta antes cap12_crear_ejemplos.py"
        )
        return

    productos = extraer_productos(html)
    guardar_y_mostrar(productos, origen, salida)
    print(f"Datos guardados en: salida/{salida.name}")


if __name__ == "__main__":
    main()
