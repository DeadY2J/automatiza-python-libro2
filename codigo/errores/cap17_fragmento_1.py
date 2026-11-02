# Fragmento ilustrativo (el programa completo va más abajo)
import argparse

parser = argparse.ArgumentParser(
    description="Limpiador seguro"
)
parser.add_argument("--hacer", action="store_true")
parser.add_argument("--min-bytes", type=int, default=500)
args = parser.parse_args()
