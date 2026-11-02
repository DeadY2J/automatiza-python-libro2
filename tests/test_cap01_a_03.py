"""Pruebas de los capítulos 01 a 03 (el taller)."""

from pathlib import Path

import cap01_calculadora_ahorro as cap01
import cap02_comprobar_entorno as cap02
import cap03_plantilla_segura as cap03


def tarea(**cambios):
    base = {
        "nombre": "Prueba",
        "veces_semana": 1,
        "minutos_manual": 60,
        "minutos_crear": 60,
        "minutos_mantenimiento_anual": 0,
    }
    base.update(cambios)
    return base


def test_evaluar_tarea_cuentas_en_minutos():
    res = cap01.evaluar_tarea(tarea())
    assert res["horas_manual"] == 52.0
    assert res["horas_ahorro"] == 51.0
    assert res["semanas_retorno"] == 1.0
    assert res["veredicto"] == "AUTOMATIZAR YA"


def test_evaluar_tarea_sin_repeticiones_no_divide():
    res = cap01.evaluar_tarea(tarea(veces_semana=0))
    assert res["semanas_retorno"] == 999.0
    assert res["veredicto"] == "MEJOR A MANO"


def test_veredicto_compensa():
    res = cap01.evaluar_tarea(
        tarea(minutos_manual=3, minutos_crear=60)
    )
    assert res["horas_ahorro"] == 1.6
    assert res["veredicto"] == "COMPENSA"


def test_cap01_salida_del_libro(capsys):
    cap01.main()
    salida = capsys.readouterr().out
    assert "Ahorro neto año 1:   33.4 h" in salida
    assert "Amortizado en:       400.0 semanas" in salida


def test_cap02_version_y_carpetas(taller):
    texto, cumple = cap02.verificar_version()
    assert texto.count(".") == 2
    assert cumple is True
    primera = cap02.preparar_carpetas(taller)
    assert [e for _, e in primera] == [False] * 3
    segunda = cap02.preparar_carpetas(taller)
    assert [e for _, e in segunda] == [True] * 3


def test_buscar_ruta_libre_no_pisa(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "a_1.txt").write_text("x")
    libre = cap03.buscar_ruta_libre(tmp_path, "a.txt")
    assert libre.name == "a_2.txt"
    libre = cap03.buscar_ruta_libre(
        tmp_path, "informe.enero.pdf"
    )
    assert libre.name == "informe.enero.pdf"


def test_cap03_simulacion_no_toca_nada(taller):
    origen = taller / "entrada" / "descargas_prueba"
    cap03.preparar_ejemplos(origen)
    log = taller / "salida" / "registro.txt"
    cap03.procesar_archivos(
        origen, taller / "copias", log, True
    )
    nombres = sorted(p.name for p in origen.iterdir())
    assert nombres == ["datos.csv", "foto.jpg", "nota.txt"]
    assert not (taller / "copias").exists()
    assert "SIMULACIÓN" in log.read_text(encoding="utf-8")


def test_cap03_real_copia_y_mueve(taller):
    origen = taller / "entrada" / "descargas_prueba"
    cap03.preparar_ejemplos(origen)
    log = taller / "salida" / "registro.txt"
    copias = taller / "copias"
    cap03.procesar_archivos(origen, copias, log, False)
    assert (origen / "Documentos" / "nota.txt").exists()
    assert (origen / "Imagenes" / "foto.jpg").exists()
    assert (copias / "datos.csv").exists()
    tamano = Path(copias / "nota.txt").stat().st_size
    assert tamano == len("Contenido de prueba de nota.txt\n")
