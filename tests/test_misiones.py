"""Pruebas de las soluciones de las Misiones (Extra 4)."""

import zipfile
from unittest import mock

from openpyxl import load_workbook
from PIL import Image
import requests

import cap04_crear_ejemplos as cap04e
import cap05_crear_ejemplos as cap05e
import cap06_crear_ejemplos as cap06e
import cap07_crear_ejemplos as cap07e
import cap09_crear_ejemplos as cap09e
import cap10_crear_ejemplos as cap10e
import cap12_crear_ejemplos as cap12e
import mision01_auditor as m01
import mision02_auditor_paquetes as m02
import mision03_limpiador_vacios as m03
import mision04_archivos_grandes as m04
import mision05_separar_capturas as m05
import mision06_extractor_seguro as m06
import mision07_tasador_juegos as m07
import mision08_presupuesto_anual as m08
import mision09_buscador_pdf as m09
import mision10_miniaturas_cuadradas as m10
import mision11_radar_ciudades as m11
import mision12_chollos_retro as m12
import mision13_alerta_espacio as m13


def test_m01_recargo_por_errores():
    tarea = {
        "nombre": "X",
        "veces_semana": 1,
        "minutos_manual": 60,
        "minutos_crear": 0,
        "minutos_mantenimiento_anual": 0,
    }
    normal = m01.evaluar_tarea(tarea)
    tarea["propensa_a_errores"] = True
    con_recargo = m01.evaluar_tarea(tarea)
    assert normal["horas_manual"] == 52.0
    assert con_recargo["horas_manual"] == 65.0


def test_m01_total_solo_rentables():
    res = [
        {"horas_ahorro": 19.2, "veredicto": "AUTOMATIZAR YA"},
        {"horas_ahorro": 1.5, "veredicto": "COMPENSA"},
        {"horas_ahorro": -1.6, "veredicto": "MEJOR A MANO"},
    ]
    assert m01.total_rentable(res) == 20.7


def test_m02_pendientes_y_orden(capsys):
    def falso(nombre):
        return None if nombre in ("PIL", "bs4") else object()

    with mock.patch("importlib.util.find_spec", falso):
        pendientes = m02.revisar_modulos(m02.MODULOS)
    assert pendientes == ["PIL", "bs4"]
    assert m02.orden_instalacion(pendientes) == (
        "python -m pip install Pillow beautifulsoup4"
    )
    assert "[PENDIENTE] bs4" in capsys.readouterr().out


def test_m03_simulacion_y_real(taller):
    carpeta = taller / "entrada" / "prueba_vacios"
    log = taller / "salida" / "registro_cuarentena.txt"
    m03.preparar_ejemplos(carpeta)
    assert m03.poner_en_cuarentena(carpeta, log, True) == 2
    assert not (carpeta / "Cuarentena").exists()
    (carpeta / "Cuarentena").mkdir()
    (carpeta / "Cuarentena" / "vacio1.txt").write_bytes(b"")
    m03.poner_en_cuarentena(carpeta, log, False)
    cuarentena = sorted(
        p.name for p in (carpeta / "Cuarentena").iterdir()
    )
    assert cuarentena == [
        "vacio1.txt", "vacio1_1.txt", "vacio2.log"
    ]
    assert (carpeta / "lleno1.txt").exists()
    assert "Modo REAL" in log.read_text(encoding="utf-8")


def test_m04_top3(taller):
    cap04e.crear_almacen_prueba()
    base = taller / "entrada" / "almacen_prueba"
    grandes = m04.buscar_grandes(base, 2000)
    assert [t for t, _ in grandes[:3]] == [3280, 2617, 2608]
    assert all(t > 2000 for t, _ in grandes)


def test_m05_capturas_y_fotos(taller):
    cap05e.crear_fotos_prueba()
    base = taller / "entrada" / "fotos_desordenadas"
    m05.separar(base, False)
    assert (
        base / "Capturas" / "2025-11" / "2025-11-03_001.png"
    ).exists()
    fotos = sorted((base / "Fotos" / "2025-08").iterdir())
    assert [p.name for p in fotos] == [
        "2025-08-14_001.jpg",
        "2025-08-14_002.jpg",
    ]
    assert (base / "nota_suelta.txt").exists()


def test_m06_restaura_la_mas_reciente(taller, monkeypatch):
    cap06e.preparar_escenario_backup()
    backups = taller / "copias" / "backups_proyecto"
    reciente = m06.copia_mas_reciente(backups)
    assert reciente.name == "backup_2026-01-25_090000.zip"
    monkeypatch.setattr("sys.argv", ["m06", "--hacer"])
    m06.main()
    m06.main()
    salida = taller / "salida"
    assert (salida / "restauracion_prueba" / "info.txt").exists()
    assert (salida / "restauracion_prueba_1").is_dir()


def test_m06_simulacion_no_extrae(taller, monkeypatch):
    cap06e.preparar_escenario_backup()
    monkeypatch.setattr("sys.argv", ["m06"])
    m06.main()
    assert not (taller / "salida").exists()


def test_m07_prestados_y_valor(taller):
    cap07e.crear_csv_ejemplos()
    juegos = m07.leer_coleccion(
        taller / "entrada" / "coleccion_juegos.csv"
    )
    prestados = m07.juegos_prestados(juegos)
    assert len(prestados) == 3
    filas = m07.valor_por_sistema(juegos)
    assert filas[0] == {
        "sistema": "PlayStation",
        "cantidad": 1,
        "valor_total": 85.0,
    }
    assert filas[1]["valor_total"] == 63.5


def test_m08_formulas(taller):
    m08.main()
    wb = load_workbook(taller / "salida" / "presupuesto_anual.xlsx")
    ws = wb["Trimestres"]
    assert ws["D2"].value == "=B2-C2"
    assert ws["D5"].value == "=B5-C5"
    assert ws["A6"].value == "TOTAL"
    assert ws["B6"].value == "=SUM(B2:B5)"
    assert ws["D6"].value == "=SUM(D2:D5)"
    assert ws["A6"].font.bold
    assert ws["C3"].number_format == m08.FORMATO_EURO


def test_m09_facturas(taller):
    cap09e.main()
    carpeta = taller / "entrada" / "pdfs_prueba"
    texto = m09.texto_completo(carpeta / "01_factura_enero.pdf")
    assert m09.importe_total(texto) == 180.0
    assert m09.importe_total("sin total") == 0.0
    m09.main()
    from pypdf import PdfReader
    unido = PdfReader(taller / "salida" / "solo_facturas.pdf")
    assert len(unido.pages) == 3


def test_m10_miniaturas(taller):
    cap10e.crear_imagenes_prueba()
    m10.main()
    carpeta = taller / "salida" / "miniaturas"
    nombres = sorted(p.name for p in carpeta.iterdir())
    assert len(nombres) == 4
    assert nombres[0] == "thumb_01_arcade_horizontal.jpg"
    for nombre in nombres:
        with Image.open(carpeta / nombre) as img:
            assert img.size == (200, 200)


def test_m11_ranking_con_red_simulada(taller, capsys):
    valores = iter([30, 90, 60])

    def falsa_get(url, params=None, timeout=None):
        resp = requests.Response()
        resp.status_code = 200
        prob = next(valores)
        resp._content = (
            '{"daily": {"time": ["a", "b"], '
            '"precipitation_probability_max": [0, '
            + str(prob)
            + "]}}"
        ).encode()
        return resp

    with mock.patch("requests.get", falsa_get), \
            mock.patch("time.sleep") as pausa:
        m11.main()
    assert pausa.call_count == 2
    texto = (taller / "salida" / "ranking_lluvia.txt").read_text(
        encoding="utf-8"
    )
    assert "1. Madrid" in texto
    assert texto.strip().endswith("Madrid")


def test_m11_sin_red(taller):
    error = requests.ConnectionError("sin red")
    with mock.patch("requests.get", side_effect=error), \
            mock.patch("time.sleep"):
        m11.main()
    texto = (taller / "salida" / "ranking_lluvia.txt").read_text(
        encoding="utf-8"
    )
    assert "1. Santiago" in texto


def test_m12_chollos(taller):
    cap12e.crear_html_ejemplo()
    m12.main()
    texto = (taller / "salida" / "alertas_chollos.txt").read_text(
        encoding="utf-8"
    )
    assert texto.splitlines() == [
        "Cable RGB Scart Blindado: 18.50 EUR",
        "Adaptador Mandos USB: 14.95 EUR",
    ]


def test_m13_modo_prueba_y_envio(taller, monkeypatch, capsys):
    libre, porcentaje = m13.medir_disco(taller)
    assert libre >= 0 and 0 <= porcentaje <= 100
    with mock.patch("requests.post") as post:
        assert m13.enviar_aviso_discord("hola") is False
    post.assert_not_called()
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://x.invalid")
    ok = requests.Response()
    ok.status_code = 204
    with mock.patch("requests.post", return_value=ok) as post:
        assert m13.enviar_aviso_discord("hola") is True
    assert post.call_args.kwargs["json"]["content"] == "hola"
