# Archivo: mision07_tasador_juegos.py

import csv
from pathlib import Path


def leer_coleccion(ruta):
    with open(ruta, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def juegos_prestados(juegos):
    return [
        j for j in juegos
        if j["prestado_a"].strip() != "Nadie"
    ]


def valor_por_sistema(juegos):
    grupos = {}
    for juego in juegos:
        sistema = juego["sistema"].strip()
        valor = float(juego["valor_euros"].strip())
        datos = grupos.setdefault(
            sistema, {"cantidad": 0, "valor_total": 0.0}
        )
        datos["cantidad"] += 1
        datos["valor_total"] += valor
    filas = [
        {
            "sistema": s,
            "cantidad": d["cantidad"],
            "valor_total": round(d["valor_total"], 2),
        }
        for s, d in grupos.items()
    ]
    filas.sort(key=lambda f: f["valor_total"], reverse=True)
    return filas


def guardar_csv(ruta, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    columnas = ["sistema", "cantidad", "valor_total"]
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    raiz = Path.cwd()
    entrada = raiz / "entrada" / "coleccion_juegos.csv"
    salida = raiz / "salida" / "valor_por_sistema.csv"
    if not entrada.exists():
        print(
            "No existe entrada/coleccion_juegos.csv. "
            "Ejecuta antes cap07_crear_ejemplos.py"
        )
        return

    juegos = leer_coleccion(entrada)
    print("Juegos prestados:")
    for j in juegos_prestados(juegos):
        valor = float(j["valor_euros"])
        print(
            f"  - {j['titulo']} -> {j['prestado_a']} "
            f"({valor:.2f} EUR)"
        )

    filas = valor_por_sistema(juegos)
    print("\nValor de la colección por sistema:")
    for f in filas:
        print(
            f"  {f['sistema']:<12} "
            f"{f['cantidad']} juego(s) "
            f"{f['valor_total']:>7.2f} EUR"
        )
    guardar_csv(salida, filas)
    print(f"\nGuardado en: salida/{salida.name}")


if __name__ == "__main__":
    main()
