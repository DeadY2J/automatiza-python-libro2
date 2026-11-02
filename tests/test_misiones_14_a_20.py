"""Pruebas de las soluciones de las Misiones 14 a 20."""

from datetime import datetime
import json
import logging
import os
import subprocess
import sys
from unittest import mock
import zipfile

import pytest
import requests

import cap15_crear_ejemplos as cap15e
import cap18_crear_ejemplos as cap18e
import cap18_el_mayordomo as cap18
import mision14_clasificador_notas as m14
import mision15_detector_fechas_importes as m15
import mision16_vigilante_descargas as m16
import mision17_lector_json_robusto as m17
import mision18_boletin_viernes as m18
import mision19_empaquetador_zip as m19
import mision20_generador_esqueleto as m20


def respuesta_chat(texto):
    resp = requests.Response()
    resp.status_code = 200
    resp._content = json.dumps(
        {"choices": [{"message": {"content": texto}}]}
    ).encode("utf-8")
    return resp


# ---------- Misión 14 ----------


def test_m14_respaldo_local():
    assert m14.clasificar_local(
        "El recibo vence hoy"
    ).startswith("URGENTE")
    assert m14.clasificar_local(
        "Se ha caído la red"
    ).startswith("URGENTE")
    assert m14.clasificar_local(
        "Idea para el verano"
    ).startswith("IDEA")
    assert m14.clasificar_local("Comprar pan").startswith(
        "NORMAL"
    )


def test_m14_normalizar_respuesta_de_la_ia():
    assert m14.normalizar("IDEA - Lectura.\nMás") == (
        "IDEA - Lectura."
    )
    assert m14.normalizar("Creo que es urgente").startswith(
        "NORMAL - Respuesta no reconocida"
    )
    assert m14.normalizar("").startswith("NORMAL")


def test_m14_main_sin_clave(taller, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with mock.patch("requests.post") as post:
        m14.main()
    post.assert_not_called()
    texto = (
        taller / "salida" / "notas_clasificadas.txt"
    ).read_text(encoding="utf-8")
    filas = texto.splitlines()[2:]
    assert [f.split(" | ")[1].split()[0] for f in filas] == [
        "URGENTE",
        "IDEA",
        "URGENTE",
    ]


def test_m14_con_clave_usa_la_ia(taller, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "clave-falsa")
    with mock.patch(
        "requests.post",
        return_value=respuesta_chat("NORMAL - Sin prisa."),
    ) as post:
        res, prueba = m14.clasificar("Comprar pan")
    assert (res, prueba) == ("NORMAL - Sin prisa.", False)
    carga = post.call_args.kwargs["json"]
    assert "URGENTE, NORMAL o IDEA" in (
        carga["messages"][0]["content"]
    )


# ---------- Misión 15 ----------


def test_m15_lineas_clave():
    texto = "Nada\nEl LUNES voy\nTotal: 5 EUR\nplazo: hoy\n"
    assert m15.lineas_clave(texto) == [
        "El LUNES voy",
        "Total: 5 EUR",
        "plazo: hoy",
    ]


def test_m15_agenda_de_los_documentos(taller):
    cap15e.main()
    m15.main()
    agenda = (taller / "salida" / "agenda_urgente.md").read_text(
        encoding="utf-8"
    )
    filas = [f for f in agenda.splitlines() if f.startswith("| 0")]
    assert len(filas) == 5
    assert "Compromisos detectados: 5" in agenda
    assert sum("03_presupuesto" in f for f in filas) == 3


def test_m15_tabla_escapa_barras():
    agenda = m15.construir_agenda([("a.txt", "x | y")])
    assert "| a.txt | x / y |" in agenda


# ---------- Misión 16 ----------


def test_m16_medir_y_anotar(tmp_path):
    entrada = tmp_path / "entrada" / "sub"
    entrada.mkdir(parents=True)
    (entrada / "a.bin").write_bytes(b"x" * 10)
    (tmp_path / "entrada" / "b.bin").write_bytes(b"x" * 5)
    assert m16.medir_carpeta(tmp_path / "entrada") == (2, 15)
    assert m16.medir_carpeta(tmp_path / "no") == (0, 0)

    csv = tmp_path / "salida" / "historico_tamano.csv"
    fecha = datetime(2026, 3, 15, 23, 0, 0)
    assert m16.anotar_historico(csv, 2, 15, fecha) is True
    assert m16.anotar_historico(csv, 3, 20, fecha) is False
    assert csv.read_bytes() == (
        b"fecha_hora,archivos,total_bytes\n"
        b"2026-03-15 23:00:00,2,15\n"
        b"2026-03-15 23:00:00,3,20\n"
    )


def test_m16_main_usa_su_carpeta(tmp_path, monkeypatch):
    monkeypatch.setattr(m16, "BASE", tmp_path)
    monkeypatch.chdir(tmp_path.parent)
    with pytest.raises(SystemExit) as fin:
        m16.main()
    assert fin.value.code == 0
    assert (tmp_path / "salida" / "historico_tamano.csv").exists()


# ---------- Misión 17 ----------


def test_m17_casos(tmp_path, caplog):
    m17.crear_pruebas(tmp_path)
    with caplog.at_level(logging.INFO):
        ok = m17.cargar_json_seguro(
            tmp_path / "valido.json", m17.CLAVES
        )
        roto = m17.cargar_json_seguro(
            tmp_path / "roto.json", m17.CLAVES
        )
        falta = m17.cargar_json_seguro(
            tmp_path / "incompleto.json", m17.CLAVES
        )
        nada = m17.cargar_json_seguro(
            tmp_path / "no.json", m17.CLAVES
        )
    assert ok == {"latitud": 42.6, "longitud": -8.6,
                  "max_copias": 3}
    assert roto is falta is nada is None
    assert "faltan claves longitud, max_copias" in caplog.text
    assert "JSON roto" in caplog.text
    lista = tmp_path / "lista.json"
    lista.write_text("[1, 2]", encoding="utf-8")
    assert m17.cargar_json_seguro(lista, ["a"]) is None


def test_m17_su_propia_prueba(tmp_path):
    m17.test_cargar_json_seguro(tmp_path)


# ---------- Misión 18 ----------


def test_m18_es_viernes():
    assert m18.es_viernes(datetime(2026, 3, 20))
    assert not m18.es_viernes(datetime(2026, 3, 19))
    assert m18.es_viernes(datetime(2026, 3, 19), forzar=True)


def test_m18_boletin_forzado(tmp_path, monkeypatch, capsys):
    for modulo in (cap18e, cap18, m18):
        monkeypatch.setattr(modulo, "BASE", tmp_path)
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    cap18e.preparar_escenario_mayordomo()
    monkeypatch.setattr(sys, "argv", ["x", "--viernes"])
    with mock.patch(
        "requests.get",
        side_effect=requests.ConnectionError("sin red"),
    ):
        m18.main()
    boletin = (
        tmp_path / "salida" / "boletin_semanal.txt"
    ).read_text(encoding="utf-8")
    assert "=== CIERRE SEMANAL ===" in boletin
    assert "Copias .zip guardadas: 2" in boletin
    backups = tmp_path / "copias" / "mayordomo_backups"
    total = sum(p.stat().st_size for p in backups.glob("*.zip"))
    assert f"Espacio que ocupan: {total} bytes" in boletin
    assert "CIERRE SEMANAL" in capsys.readouterr().out


def test_m18_sin_copias():
    from pathlib import Path

    res = m18.cierre_semanal(Path("no_existe_nunca"))
    assert "Copias .zip guardadas: 0" in res


# ---------- Misión 19 ----------


def test_m19_empaqueta_si_esta_limpio(tmp_path, monkeypatch):
    monkeypatch.setattr(m19, "BASE", tmp_path)
    (tmp_path / "uno.py").write_text("print(1)\n")
    (tmp_path / "README.md").write_text("# Hola\n")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "fuera.py").write_text("x = 1\n")
    m19.main()
    m19.main()
    kit = tmp_path / "salida" / "kit_compartir_taller.zip"
    assert kit.exists()
    assert kit.with_name("kit_compartir_taller_1.zip").exists()
    with zipfile.ZipFile(kit) as zf:
        assert sorted(zf.namelist()) == ["README.md", "uno.py"]


def test_m19_se_niega_con_alertas(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(m19, "BASE", tmp_path)
    (tmp_path / "malo.py").write_text(
        'TOKEN = "sk-falsa"\n', encoding="utf-8"
    )
    m19.main()
    assert not (tmp_path / "salida").exists()
    assert "No creo el .zip" in capsys.readouterr().out


# ---------- Misión 20 ----------


def test_m20_limpiar_nombre():
    assert m20.limpiar_nombre(" Clasificar Recibos ") == (
        "clasificar_recibos"
    )
    assert m20.limpiar_nombre("copia.py") == "copia"
    assert m20.limpiar_nombre("año-2026!") == "ao2026"
    assert m20.limpiar_nombre("¿?") == ""


def test_m20_esqueleto_funciona(tmp_path):
    ruta, creado = m20.crear_esqueleto(tmp_path, "mi_tarea")
    assert creado
    texto = ruta.read_text(encoding="utf-8")
    assert texto.startswith("# Archivo: mi_tarea.py\n")
    assert max(len(lin) for lin in texto.splitlines()) <= 60
    compile(texto, str(ruta), "exec")
    res = subprocess.run(
        [sys.executable, str(ruta)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert res.returncode == 0
    assert "Iniciando mi_tarea (SIMULACIÓN)" in res.stderr

    _, otra_vez = m20.crear_esqueleto(tmp_path, "mi_tarea")
    assert otra_vez is False
    assert ruta.read_text(encoding="utf-8") == texto
