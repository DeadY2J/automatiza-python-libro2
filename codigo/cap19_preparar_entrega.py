# Archivo: cap19_preparar_entrega.py

from pathlib import Path

BASE = Path(__file__).resolve().parent
CARPETAS_EXCLUIDAS = {
    ".venv",
    "build",
    "dist",
    "__pycache__",
}

PATRONES_RIESGO = [
    "c:\\users\\",
    "/home/",
    "/users/",
    "aiza",
    "sk-",
    "discord.com/api/webhooks/",
]


def listar_scripts_py(base):
    propio = Path(__file__).name
    scripts = []
    for p in sorted(base.rglob("*.py")):
        if any(
            part in CARPETAS_EXCLUIDAS for part in p.parts
        ):
            continue
        if p.name == propio:
            continue
        scripts.append(p)
    return scripts


def revisar_linea(texto_linea):
    # "C:\\Users" en el código fuente equivale a C:\Users
    minus = texto_linea.lower().replace("\\\\", "\\")
    for patron in PATRONES_RIESGO:
        if patron in minus:
            return f"Patrón sensible '{patron}'"

    if "@" in minus:
        excepciones = [
            "@ejemplo.local",
            "@echo off",
            "[@",
        ]
        if not any(exc in minus for exc in excepciones):
            if "." in minus.split("@")[-1]:
                return "Posible correo electrónico real"
    return ""


def auditar_codigo(base):
    scripts = listar_scripts_py(base)
    hallazgos = []

    for ruta in scripts:
        lineas = ruta.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        for num, lin in enumerate(lineas, start=1):
            motivo = revisar_linea(lin)
            if motivo:
                hallazgos.append((ruta.name, num, motivo))

    return len(scripts), hallazgos


def escribir_gitignore(base):
    lineas = [
        "# Entorno virtual y cachés de Python",
        ".venv/",
        "__pycache__/",
        "*.pyc",
        "",
        "# Ejecutables de PyInstaller",
        "build/",
        "dist/",
        "*.spec",
        "",
        "# Datos locales y secretos",
        ".env",
        "entrada/",
        "salida/",
        "copias/",
        "*.log",
    ]
    ruta = base / ".gitignore"
    texto = "\n".join(lineas) + "\n"
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    return ruta


def escribir_readme(base, total_scripts):
    lineas = [
        "# Caja de Herramientas de Automatización "
        "en Python",
        "",
        f"Colección de {total_scripts} scripts "
        "prácticos para "
        "automatizar archivos, datos, avisos e IA.",
        "",
        "## Requisitos",
        "- Python 3.12 o superior",
        "",
        "## Instalación rápida (Windows)",
        "```powershell",
        "python -m venv .venv",
        ".venv\\Scripts\\Activate.ps1",
        "python -m pip install -r requirements.txt",
        "```",
        "",
        "## Regla de seguridad (Modo simulación)",
        "Todos los scripts que mueven o modifican archivos "
        "arrancan en **modo simulación** por defecto.",
        "Para aplicar los cambios reales, añade `--hacer`:",
        "```powershell",
        "python cap18_el_mayordomo.py --hacer",
        "```",
    ]
    ruta = base / "README.md"
    texto = "\n".join(lineas) + "\n"
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    return ruta


def main():
    print("=" * 54)
    print("AUDITORÍA PREVIA Y PREPARACIÓN DE ENTREGA")
    print("=" * 54)

    total, alertas = auditar_codigo(BASE)
    print(f"Scripts .py analizados: {total}")

    if not alertas:
        print("Estado de privacidad:   LIMPIO (0 alertas)")
    else:
        print(
            "Estado de privacidad:   "
            f"{len(alertas)} ALERTA(S)"
        )
        for arch, fila, mot in alertas:
            print(f"  [!] {arch} (línea {fila}): {mot}")

    r_git = escribir_gitignore(BASE)
    r_doc = escribir_readme(BASE, total)
    print("\nArchivos de repositorio generados:")
    print(f"  - {r_git.name}")
    print(f"  - {r_doc.name}")
    print("=" * 54)


if __name__ == "__main__":
    main()
