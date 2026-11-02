# Fragmento ilustrativo (el programa completo va más abajo)
from bs4 import BeautifulSoup

html = (
    '<article class="item"><h3>Joystick</h3>'
    '<span class="precio">24.90</span></article>'
)
sopa = BeautifulSoup(html, "html.parser")

for ficha in sopa.select("article.item"):
    titulo = ficha.select_one("h3").get_text(strip=True)
    nodo = ficha.select_one("span.precio")
    precio = nodo.get_text(strip=True)
    print(titulo, precio)
