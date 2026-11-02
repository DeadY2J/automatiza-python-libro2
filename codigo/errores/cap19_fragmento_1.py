import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    CARPETA_BASE = Path(sys.executable).resolve().parent
else:
    CARPETA_BASE = Path(__file__).resolve().parent
