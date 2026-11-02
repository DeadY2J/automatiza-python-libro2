"""Pruebas de los capítulos 04 a 06 (archivos y carpetas)."""

from datetime import datetime
import json
import os
import zipfile

import cap04_crear_ejemplos as cap04e
import cap04_inventario_carpeta as cap04
import cap05_crear_ejemplos as cap05e
import cap05_deshacer_renombrado as cap05d
import cap05_renombrar_fotos as cap05
import cap06_copia_seguridad as cap06
import cap06_crear_ejemplos as cap06e


def test_sha256_por_bloques(tmp_path):
    ruta = tmp_path / "x.bin"
    ruta.write_bytes(b"abc")
    esperado = (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )
    assert cap04.calcular_sha256(ruta) == esperado


def test_inventario_del_libro(taller):
    cap04e.crear_almacen_prueba()
    base = taller / "entrada" / "almacen_prueba"
    total, bytes_, por_ext, por_tam = (
        cap04.escanear_carpeta(base)
    )
    assert total == 7
    assert bytes_ == 14181
    assert por_ext[".png"] == {"cantidad": 3, "bytes": 7833}
    dups = cap04.buscar_duplicados(por_tam)
    assert sorted(t for t, _, _ in dups) == [1520, 2608]
    texto = cap04.generar_informe(
        base, total, bytes_, por_ext, dups
    )
    assert "Espacio recuperable: 4128 bytes" in texto


def test_inventario_ignora_vacios(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"")
    (tmp_path / "b.txt").write_bytes(b"")
    _, _, _, por_tam = cap04.escanear_carpeta(tmp_path)
    assert cap04.buscar_duplicados(por_tam) == []


def test_calcular_destino_reserva_en_simulacion(tmp_path):
    marca = datetime(2025, 8, 14, 10, 30).timestamp()
    fotos = []
    for nombre in ["a.JPG", "b.jpg"]:
        ruta = tmp_path / nombre
        ruta.write_bytes(b"x")
        os.utime(ruta, (marca, marca))
        fotos.append(ruta)
    reservados = set()
    d1 = cap05.calcular_destino(fotos[0], tmp_path, reservados)
    d2 = cap05.calcular_destino(fotos[1], tmp_path, reservados)
    assert d1.name == "2025-08-14_001.jpg"
    assert d2.name == "2025-08-14_002.jpg"
    assert d1.parent.relative_to(tmp_path).as_posix() == (
        "2025/2025-08"
    )


def test_obtener_fotos_filtra_extensiones(taller):
    cap05e.crear_fotos_prueba()
    base = taller / "entrada" / "fotos_desordenadas"
    nombres = [p.name for p in cap05.obtener_fotos(base)]
    assert "nota_suelta.txt" not in nombres
    assert len(nombres) == 4


def test_renombrar_y_deshacer(taller):
    cap05e.crear_fotos_prueba()
    base = taller / "entrada" / "fotos_desordenadas"
    ruta_json = taller / "salida" / "ultimo_lote_fotos.json"
    antes = sorted(p.name for p in base.iterdir())

    cap05.procesar_lote(base, ruta_json, True)
    assert sorted(p.name for p in base.iterdir()) == antes
    assert not ruta_json.exists()

    cap05.procesar_lote(base, ruta_json, False)
    lote = json.loads(ruta_json.read_text(encoding="utf-8"))
    assert len(lote) == 4
    assert (base / "2026" / "2026-01").is_dir()

    cap05d.deshacer_lote(ruta_json, False)
    archivos = sorted(
        p.name for p in base.iterdir() if p.is_file()
    )
    assert archivos == antes
    assert not ruta_json.exists()


def test_rotacion_simulada_cuenta_la_nueva(taller, capsys):
    cap06e.preparar_escenario_backup()
    backups = taller / "copias" / "backups_proyecto"
    nuevo = backups / "backup_2026-03-15_112030.zip"
    cap06.rotar_copias_antiguas(backups, nuevo, 3, True)
    salida = capsys.readouterr().out
    assert salida.count("[SIMULACIÓN] Rotaría") == 2
    assert len(list(backups.glob("backup_*.zip"))) == 4


def test_copia_real_y_rotacion(taller):
    cap06e.preparar_escenario_backup()
    origen = taller / "entrada" / "proyecto_activo"
    backups = taller / "copias" / "backups_proyecto"
    archivos = cap06.listar_archivos_origen(origen)
    nuevo = backups / "backup_2026-03-15_112030.zip"
    cap06.crear_zip(origen, nuevo, archivos, False)
    with zipfile.ZipFile(nuevo) as zf:
        assert sorted(zf.namelist()) == [
            "capitulos/borrador_01.md",
            "capitulos/presupuesto.csv",
            "notas.txt",
        ]
        assert zf.testzip() is None
    cap06.rotar_copias_antiguas(backups, nuevo, 3, False)
    quedan = sorted(p.name for p in backups.glob("*.zip"))
    assert quedan == [
        "backup_2026-01-20_090000.zip",
        "backup_2026-01-25_090000.zip",
        nuevo.name,
    ]
    historico = backups / "historico_antiguo"
    assert len(list(historico.glob("*.zip"))) == 2
