# Fragmento ilustrativo (el programa completo va más abajo)
from PIL import Image

with Image.open("entrada/imagenes_bruto/foto.png") as img:
    img_rgb = img.convert("RGB")
    img_rgb.thumbnail((800, 800))
    img_rgb.save("salida/foto_web.jpg", "JPEG", quality=85)
