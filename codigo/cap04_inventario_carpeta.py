# Archivo: cap04_inventario_carpeta.py

import hashlib
from pathlib import Path

BLOQUE_LECTURA = 65536


def calcular_sha256(ruta_archivo):
    resumen = hashlib.sha256()
    with open(ruta_archivo, "rb") as f:
        while True:
            bloque = f.read(BLOQUE_LECTURA)
            if not bloque:
                break
            resumen.update(bloque)
    return resumen.hexdigest()


def escanear_carpeta(carpeta_base):
    por_extension = {}
    por_tamano = {}
    total_archivos = 0
    total_bytes = 0

    archivos = sorted(
        p for p in carpeta_base.rglob("*") if p.is_file()
    )

    for archivo in archivos:
        tam = archivo.stat().st_size
        ext = archivo.suffix.lower() or "[sin_ext]"

        total_archivos += 1
        total_bytes += tam

        if ext not in por_extension:
            por_extension[ext] = {"cantidad": 0, "bytes": 0}
        por_extension[ext]["cantidad"] += 1
        por_extension[ext]["bytes"] += tam

        if tam > 0:
            por_tamano.setdefault(tam, []).append(archivo)

    return (
        total_archivos,
        total_bytes,
        por_extension,
        por_tamano,
    )


def buscar_duplicados(por_tamano):
    duplicados = []
    for tam, lista_rutas in por_tamano.items():
        if len(lista_rutas) < 2:
            continue
        por_hash = {}
        for ruta in lista_rutas:
            codigo = calcular_sha256(ruta)
            por_hash.setdefault(codigo, []).append(ruta)

        for codigo, iguales in por_hash.items():
            if len(iguales) > 1:
                duplicados.append(
                    (tam, codigo[:12], iguales)
                )
    return duplicados


def generar_informe(
    base, total_arch, total_bytes, por_ext, duplicados
):
    lineas = [
        "=" * 54,
        f"INVENTARIO DE: ./{base.name}/",
        "=" * 54,
        f"Archivos analizados: {total_arch}",
        f"Tamaño total:        {total_bytes} bytes",
        "\nDesglose por extensión:",
    ]

    for ext, datos in sorted(por_ext.items()):
        cant = datos["cantidad"]
        tam = datos["bytes"]
        lineas.append(
            f"  {ext:<10} -> {cant} archivo(s) "
            f"({tam} bytes)"
        )

    lineas.append(
        "\nDuplicados exactos (por tamaño y SHA-256):"
    )
    if not duplicados:
        lineas.append("  Ningún archivo duplicado.")
    else:
        ahorro = 0
        for tam, hash_corto, rutas in duplicados:
            sobrantes = len(rutas) - 1
            ahorro += tam * sobrantes
            lineas.append(
                f"  * Grupo [{hash_corto}...] "
                f"({tam} bytes cada uno):"
            )
            for r in rutas:
                rel = r.relative_to(base)
                lineas.append(f"      - {rel.as_posix()}")
        lineas.append(
            f"\nEspacio recuperable: {ahorro} bytes"
        )

    lineas.append("=" * 54)
    return "\n".join(lineas)


def main():
    base = Path.cwd() / "entrada" / "almacen_prueba"
    if not base.exists():
        print(
            "No existe entrada/almacen_prueba. "
            "Ejecuta antes cap04_crear_ejemplos.py"
        )
        return

    tot_arch, tot_bytes, por_ext, por_tam = (
        escanear_carpeta(base)
    )
    duplicados = buscar_duplicados(por_tam)
    texto = generar_informe(
        base, tot_arch, tot_bytes, por_ext, duplicados
    )

    print(texto)
    salida = (
        Path.cwd() / "salida" / "inventario_resultado.txt"
    )
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
