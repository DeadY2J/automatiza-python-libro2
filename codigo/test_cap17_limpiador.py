# Archivo: test_cap17_limpiador.py

from cap17_limpiador_robusto import (
    es_candidato,
    mover_con_seguridad,
)


def test_es_candidato_filtra_por_ext_y_tamano(tmp_path):
    grande_tmp = tmp_path / "datos.TMP"
    grande_tmp.write_text("A" * 200, encoding="utf-8")

    pequeno_tmp = tmp_path / "chico.tmp"
    pequeno_tmp.write_text("A" * 20, encoding="utf-8")

    bueno_txt = tmp_path / "nota.txt"
    bueno_txt.write_text("A" * 200, encoding="utf-8")

    exts = [".tmp", ".bak"]
    assert es_candidato(grande_tmp, exts, 100) is True
    assert es_candidato(pequeno_tmp, exts, 100) is False
    assert es_candidato(bueno_txt, exts, 100) is False


def test_simulacion_no_mueve_el_archivo(tmp_path):
    origen = tmp_path / "origen"
    destino = tmp_path / "destino"
    origen.mkdir()

    archivo = origen / "prueba.bak"
    archivo.write_text("contenido", encoding="utf-8")

    ok = mover_con_seguridad(
        archivo, destino, simulacion=True
    )
    assert ok is True
    assert archivo.exists() is True
    assert not (destino / "prueba.bak").exists()


def test_modo_real_mueve_y_evita_colision(tmp_path):
    origen = tmp_path / "origen"
    destino = tmp_path / "destino"
    origen.mkdir()
    destino.mkdir()

    (destino / "item.tmp").write_text(
        "viejo", encoding="utf-8"
    )
    nuevo = origen / "item.tmp"
    nuevo.write_text("nuevo", encoding="utf-8")

    ok = mover_con_seguridad(
        nuevo, destino, simulacion=False
    )
    assert ok is True
    assert not nuevo.exists()
    assert (destino / "item_1.tmp").exists() is True
