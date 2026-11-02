# Código del libro «Automatiza tu vida con Python y IA»

Todos los scripts de los capítulos, probados con Python 3.12 o superior.
Cada archivo empieza con un comentario `# Archivo: nombre.py` que
indica el nombre con el que aparece en el libro.

## Preparar el taller

```bash
python -m venv .venv
```

Activa el entorno (`.venv\Scripts\Activate.ps1` en Windows,
`source .venv/bin/activate` en Mac y Linux) e instala las librerías:

```bash
python -m pip install openpyxl pypdf Pillow requests beautifulsoup4 pytest
```

Ejecuta los scripts desde la carpeta de trabajo (la que tendrá `entrada/`,
`salida/` y `copias/`). Hasta el capítulo 15 usan la carpeta actual como
raíz; del 16 en adelante calculan la suya con `Path(__file__)`, así que
`entrada/`, `salida/` y `copias/` quedan junto al script aunque lo lances
desde otra carpeta (o desde el Programador de tareas). Los que
mueven o renombran archivos arrancan en modo simulación y solo actúan con
`--hacer`. Los que usan secretos los leen de variables de entorno y, si
faltan, funcionan en modo prueba.

## Scripts por capítulo

| Cap. | Orden de ejecución | Qué hace |
|------|--------------------|----------|
| 01 | `python cap01_calculadora_ahorro.py` | Calcula si compensa automatizar cuatro tareas de ejemplo. |
| 02 | `python cap02_comprobar_entorno.py` | Comprueba la versión de Python, el entorno virtual y crea `entrada/`, `salida/` y `copias/`. |
| 03 | `python cap03_plantilla_segura.py` y luego `--hacer` | Plantilla segura: simulación, registro en `salida/registro_acciones.txt` y copia previa. |
| 04 | `cap04_crear_ejemplos.py`, `cap04_inventario_carpeta.py` | Inventario de `entrada/almacen_prueba` con duplicados por tamaño y SHA-256. |
| 05 | `cap05_crear_ejemplos.py`, `cap05_renombrar_fotos.py [--hacer]`, `cap05_deshacer_renombrado.py [--hacer]` | Renombra fotos por fecha y deshace el lote con el JSON. |
| 06 | `cap06_crear_ejemplos.py`, `cap06_copia_seguridad.py [--hacer]` | Copia `.zip` con fecha y rotación de las antiguas. |
| 07 | `cap07_crear_ejemplos.py`, `cap07_resumen_gastos_csv.py` | Limpia un CSV de gastos y guarda el resumen. |
| 08 | `cap08_crear_ejemplos.py`, `cap08_informe_excel.py` | Informe `.xlsx` con fórmulas, formato y gráfico. |
| 09 | `cap09_crear_ejemplos.py`, `cap09_herramientas_pdf.py` | Une PDF, separa una página y extrae el texto. |
| 10 | `cap10_crear_ejemplos.py`, `cap10_procesar_imagenes.py` | Redimensiona, pasa a JPEG y pone marca de agua. |
| 11 | `cap11_tiempo_manana.py`, `cap11_ficha_pokemon.py [nombre]` | Open-Meteo y PokéAPI, con datos de respaldo sin red. |
| 12 | `cap12_crear_ejemplos.py`, `cap12_lector_web.py [--web]` | Lee el catálogo local o books.toscrape.com respetando `robots.txt`. |
| 13 | `cap13_aviso_discord.py`, `cap13_aviso_correo.py` | Avisos por webhook de Discord y por correo (modo prueba sin variables). |
| 14 | `cap14_cliente_ia.py` | Llama a un modelo de IA con `requests` (formato `chat/completions`); sin `GEMINI_API_KEY`, modo prueba. |
| 15 | `cap15_crear_ejemplos.py`, `cap15_el_escriba.py` | El Escriba: resume `.txt`, `.md` y `.pdf` y escribe `salida/informe_escriba.md`. |
| 16 | `cap16_latido.py [--auto]` | Registra un latido en `salida/latidos_automaticos.log` y genera `cap16_lanzador.bat` para el Programador de tareas. |
| 17 | `cap17_limpiador_robusto.py [--hacer] [--min-bytes N]`, `python -m pytest test_cap17_limpiador.py -v` | Limpiador con `config.json`, `argparse`, `logging` y sus pruebas. |
| 18 | `cap18_crear_ejemplos.py`, `cap18_el_mayordomo.py [--hacer]` | El Mayordomo: ordena descargas, copia `.zip` con rotación, tiempo de hoy y parte a Discord. |
| 19 | `cap19_preparar_entrega.py` | Audita los `.py` en busca de rutas, correos y claves, y genera `.gitignore` y `README.md`. |

Variables de entorno: `DISCORD_WEBHOOK_URL` (capítulos 13 y 18),
`SMTP_SERVIDOR`, `SMTP_PUERTO`, `SMTP_USUARIO`, `SMTP_CLAVE` y
`SMTP_DESTINO` (capítulo 13) y `GEMINI_API_KEY` (capítulos 14 y 15).
Si falta alguna, el script correspondiente entra en modo prueba.

El capítulo 19 usa además PyInstaller (`python -m pip install
pyinstaller`) para crear ejecutables; no hace falta para el resto.

## Otras carpetas

- `errores/`: los fragmentos ilustrativos y los marcados con
  `# ERROR A PROPÓSITO`, tal como aparecen en el libro. No son programas
  completos; algunos fallan a propósito.
- `soluciones/`: las soluciones de las Misiones (Extra 4). Cada una se
  ejecuta como los scripts de su capítulo (`misionNN_*.py`); las que
  necesitan archivos de entrada usan los del `capNN_crear_ejemplos.py`
  correspondiente.

## Probarlo todo

```bash
python -m pytest -q tests
```

Las pruebas simulan las respuestas de red (Open-Meteo, PokéAPI, books.toscrape.com y el modelo de IA), así que no necesitan internet ni claves.
