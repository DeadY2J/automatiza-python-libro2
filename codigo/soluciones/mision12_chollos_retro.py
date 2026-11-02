# Archivo: mision12_chollos_retro.py

from pathlib import Path
from bs4 import BeautifulSoup

PRECIO_TOPE = 25.0


def leer_productos(html):
    sopa = BeautifulSoup(html, "html.parser")
    productos = []
    for item in sopa.select("article.product_pod"):
        enlace = item.select_one("h3 a")
        nodo_precio = item.select_one("p.price_color")
        nodo_stock = item.select_one("p.availability")
        if enlace is None or nodo_precio is None:
            continue
        titulo = enlace.get("title") or enlace.get_text()
        precio_txt = nodo_precio.get_text(strip=True)
        try:
            precio = float(precio_txt.replace("€", ""))
        except ValueError:
            continue
        stock = ""
        if nodo_stock:
            stock = nodo_stock.get_text(strip=True)
        productos.append(
            {
                "titulo": titulo.strip(),
                "precio": precio,
                "stock": stock,
            }
        )
    return productos


def es_chollo(p):
    en_stock = "en stock" in p["stock"].lower()
    return p["precio"] < PRECIO_TOPE and en_stock


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "catalogo_retro.html"
    salida = raiz / "salida" / "alertas_chollos.txt"
    if not entrada.exists():
        print(
            "No existe entrada/catalogo_retro.html. "
            "Ejecuta antes cap12_crear_ejemplos.py"
        )
        return

    html = entrada.read_text(encoding="utf-8")
    productos = leer_productos(html)
    chollos = [p for p in productos if es_chollo(p)]
    lineas = [
        f"{p['titulo']}: {p['precio']:.2f} EUR"
        for p in chollos
    ]
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(
        "\n".join(lineas) + "\n", encoding="utf-8"
    )
    print(
        f"Chollos en stock por debajo de {PRECIO_TOPE} EUR:"
    )
    for linea in lineas:
        print(f"  - {linea}")
    print(f"Alertas guardadas en salida/{salida.name}")


if __name__ == "__main__":
    main()
