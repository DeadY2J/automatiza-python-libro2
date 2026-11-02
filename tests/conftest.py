"""Configuración común de las pruebas del libro.

Los scripts viven en codigo/ y codigo/soluciones/; aquí los
hacemos importables y damos una carpeta de trabajo temporal,
porque todos usan Path.cwd() como raíz del taller.
"""

from pathlib import Path
import sys

import pytest

RAIZ = Path(__file__).resolve().parent.parent
for sub in ("codigo", "codigo/soluciones"):
    ruta = str(RAIZ / sub)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)


@pytest.fixture
def taller(tmp_path, monkeypatch):
    """Carpeta de trabajo vacía como directorio actual."""
    monkeypatch.chdir(tmp_path)
    for var in (
        "DISCORD_WEBHOOK_URL",
        "SMTP_SERVIDOR",
        "SMTP_PUERTO",
        "SMTP_USUARIO",
        "SMTP_CLAVE",
        "SMTP_DESTINO",
    ):
        monkeypatch.delenv(var, raising=False)
    return tmp_path
