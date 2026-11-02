# Archivo: cap12_crear_ejemplos.py

from pathlib import Path


def crear_html_ejemplo():
    carpeta = Path.cwd() / "entrada"
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "catalogo_retro.html"

    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Catálogo Retro</title>
</head>
<body>
  <h1>Ofertas de la semana</h1>
  <section class="catalogo">
    <article class="product_pod">
      <h3><a title="Joystick Arcade Microswitches">
        Joystick Arcade</a></h3>
      <p class="price_color">€34.90</p>
      <p class="instock availability">En stock</p>
    </article>
    <article class="product_pod">
      <h3><a title="Cable RGB Scart Blindado">
        Cable RGB Scart</a></h3>
      <p class="price_color">€18.50</p>
      <p class="instock availability">En stock</p>
    </article>
    <article class="product_pod">
      <h3><a title="Fuente Alimentación 9V Clásica">
        Fuente 9V</a></h3>
      <p class="price_color">€22.00</p>
      <p class="instock availability">Últimas unidades</p>
    </article>
    <article class="product_pod">
      <h3><a title="Adaptador Mandos USB">
        Adaptador USB</a></h3>
      <p class="price_color">€14.95</p>
      <p class="instock availability">En stock</p>
    </article>
  </section>
</body>
</html>
"""
    ruta.write_text(
        html, encoding="utf-8", newline="\n"
    )
    print(f"Página local creada en: entrada/{ruta.name}")


if __name__ == "__main__":
    crear_html_ejemplo()
