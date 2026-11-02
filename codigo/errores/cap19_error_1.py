# ERROR A PROPÓSITO (compilado con PyInstaller --onefile)
from pathlib import Path

base = Path(__file__).resolve().parent
cfg = (base / "config.json").read_text(encoding="utf-8")
