# ERROR A PROPÓSITO
try:
    for archivo in carpeta.iterdir():
        shutil.move(str(archivo), str(destino))
except:
    pass
