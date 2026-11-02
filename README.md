# Automatiza tu vida con Python y IA: código del libro

Código descargable del libro **«Automatiza tu vida con Python y IA»** (serie *Programar con IA*, nº 2), de Jorge Lamelas.

- `codigo/`: los 53 scripts del libro, un archivo por programa, con el mismo nombre que en cada capítulo. Incluye `errores/` (los fallos que se analizan en el texto) y `soluciones/` (las soluciones de las misiones).
- `tests/`: pruebas con `pytest` de todos los scripts y de las soluciones.

Los scripts funcionan primero en **modo simulación** y solo actúan de verdad si añades `--hacer`. Se prueban de forma automática en Windows, Linux y macOS con Python 3.12.

## Cómo empezar

```bash
python -m venv .venv
python -m pip install openpyxl pypdf Pillow requests beautifulsoup4 pytest
python -m pytest -q tests
```

En `codigo/README.md` tienes los pasos detallados para preparar el taller. Los capítulos explican cada script y cómo adaptarlo.

## Qué no incluye

Este repositorio contiene solo el código. El texto del libro está en Amazon.

## Licencia

Código bajo licencia MIT (ver `LICENSE`). Úsalo, cámbialo y compártelo.
