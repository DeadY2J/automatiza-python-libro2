# ERROR A PROPÓSITO
from bs4 import BeautifulSoup

html = "<article><h3>Mando</h3></article>"
sopa = BeautifulSoup(html, "html.parser")
texto = sopa.select_one("p.precio_oferta").get_text()
