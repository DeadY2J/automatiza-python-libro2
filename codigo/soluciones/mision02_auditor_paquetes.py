# Archivo: mision02_auditor_paquetes.py

import importlib.util

MODULOS = [
    "openpyxl", "pypdf", "PIL", "requests", "bs4", "pytest"
]
NOMBRE_PIP = {"PIL": "Pillow", "bs4": "beautifulsoup4"}


def revisar_modulos(modulos):
    pendientes = []
    for nombre in modulos:
        if importlib.util.find_spec(nombre) is None:
            print(f"  [PENDIENTE] {nombre}")
            pendientes.append(nombre)
        else:
            print(f"  [INSTALADO] {nombre}")
    return pendientes


def orden_instalacion(pendientes):
    paquetes = [NOMBRE_PIP.get(m, m) for m in pendientes]
    return "python -m pip install " + " ".join(paquetes)


def main():
    print("Librerías del libro en este entorno:")
    pendientes = revisar_modulos(MODULOS)
    if pendientes:
        print("\nPara instalar lo que falta:")
        print(orden_instalacion(pendientes))
    else:
        print("\nTodo instalado. Puedes seguir.")


if __name__ == "__main__":
    main()
