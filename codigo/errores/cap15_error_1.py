# ERROR A PROPÓSITO
from pathlib import Path

ruta = Path("entrada/nota_antigua.txt")
ruta.write_bytes("Reunión en Málaga".encode("latin-1"))
texto = ruta.read_text(encoding="utf-8")
