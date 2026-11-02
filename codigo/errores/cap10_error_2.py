# ERROR A PROPÓSITO
from PIL import Image, ImageDraw

img = Image.new("RGB", (200, 200))
dibujo = ImageDraw.Draw(img)
ancho, alto = dibujo.textsize("Hola")
