# ERROR A PROPÓSITO
import hashlib
from pathlib import Path

ruta = Path("entrada/almacen_prueba/leeme_urgente.md")
texto = ruta.read_text(encoding="utf-8")
codigo = hashlib.sha256(texto).hexdigest()
