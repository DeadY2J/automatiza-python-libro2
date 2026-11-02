# Archivo: cap02_comprobar_entorno.py

from pathlib import Path
import sys

CARPETAS_TALLER = ["entrada", "salida", "copias"]


def verificar_version():
    mayor = sys.version_info.major
    menor = sys.version_info.minor
    micro = sys.version_info.micro
    version_txt = f"{mayor}.{menor}.{micro}"
    cumple = (mayor, menor) >= (3, 12)
    return version_txt, cumple


def en_entorno_virtual():
    return sys.prefix != sys.base_prefix


def preparar_carpetas(base):
    estado_carpetas = []
    for nombre in CARPETAS_TALLER:
        ruta = base / nombre
        existia = ruta.exists()
        if not existia:
            ruta.mkdir(parents=True, exist_ok=True)
        estado_carpetas.append((nombre, existia))
    return estado_carpetas


def main():
    print("=" * 52)
    print("DIAGNÓSTICO DEL TALLER DE AUTOMATIZACIÓN")
    print("=" * 52)

    ver_txt, ver_ok = verificar_version()
    estado_ver = "OK" if ver_ok else "ACTUALIZAR (<3.12)"
    print(f"Versión de Python: {ver_txt} [{estado_ver}]")

    venv_ok = en_entorno_virtual()
    if venv_ok:
        txt_venv = "ACTIVO (.venv detectado)"
    else:
        txt_venv = "INACTIVO (activa .venv antes de seguir)"
    print(f"Entorno virtual:   {txt_venv}")

    carpeta_actual = Path.cwd()
    print(f"Carpeta activa:    ./{carpeta_actual.name}/")

    print("\nSubcarpetas de trabajo:")
    resultados = preparar_carpetas(carpeta_actual)
    for nombre, existia in resultados:
        accion = "ya existía" if existia else "CREADA AHORA"
        print(f"  - {nombre}/ -> {accion}")

    print("=" * 52)
    if ver_ok and venv_ok:
        print("Estado final: Taller listo para trabajar.")
    else:
        print("Estado final: Revisa los avisos anteriores.")


if __name__ == "__main__":
    main()
