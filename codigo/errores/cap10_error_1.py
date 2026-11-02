# ERROR A PROPÓSITO
from PIL import Image

img = Image.new("RGBA", (200, 200), (255, 0, 0, 128))
img.save("salida/fallo.jpg", "JPEG")
