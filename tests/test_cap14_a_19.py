"""Pruebas de los capítulos 14 a 19.

Sin red ni claves: las respuestas del modelo de IA (formato
chat/completions), de Open-Meteo y del webhook de Discord se
simulan con unittest.mock. Los scripts que calculan su carpeta
con __file__ (16 a 19) se prueban cambiando su constante BASE
por una carpeta temporal.
"""

import json
import logging
from pathlib import Path
import re
import sys
from unittest import mock
import zipfile

import pytest
import requests

import cap14_cliente_ia as cap14
import cap15_crear_ejemplos as cap15e
import cap15_el_escriba as cap15
import cap16_latido as cap16
import cap17_limpiador_robusto as cap17
import cap18_crear_ejemplos as cap18e
import cap18_el_mayordomo as cap18
import cap19_preparar_entrega as cap19

RAIZ = Path(__file__).resolve().parent.parent


def respuesta(cuerpo, estado=200):
    resp = requests.Response()
    resp.status_code = estado
    resp.reason = {200: "OK", 204: "No Content"}.get(
        estado, "Too Many Requests"
    )
    if isinstance(cuerpo, (dict, list)):
        cuerpo = json.dumps(cuerpo)
    resp._content = cuerpo.encode("utf-8")
    resp.headers["Content-Type"] = "application/json"
    resp.url = "https://ejemplo.invalid/"
    return resp


def chat(texto):
    """Respuesta con la forma real de chat/completions."""
    return {
        "id": "chatcmpl-1",
        "object": "chat.completion",
        "created": 1773570000,
        "model": "gemini-3.6-flash",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": texto,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 80,
            "completion_tokens": 30,
            "total_tokens": 110,
        },
    }


METEO_HOY = {
    "latitude": 42.6,
    "longitude": -8.64,
    "timezone": "Europe/Madrid",
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
        "precipitation_probability_max": "%",
    },
    "daily": {
        "time": ["2026-03-15"],
        "temperature_2m_max": [18.4],
        "temperature_2m_min": [8.1],
        "precipitation_probability_max": [15],
    },
}


@pytest.fixture
def sin_clave(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)


# ---------- Capítulo 14 ----------


def test_cap14_modo_prueba_sin_clave(sin_clave, capsys):
    with mock.patch("requests.post") as post:
        texto, prueba = cap14.consultar_ia("x", "Hola\nmundo")
    assert prueba is True
    post.assert_not_called()
    assert "Primera línea detectada: Hola" in texto
    assert "Longitud analizada: 10 caracteres." in texto
    assert "[MODO PRUEBA]" in capsys.readouterr().out


def test_cap14_clave_vacia_tambien_es_prueba(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "   ")
    with mock.patch("requests.post") as post:
        _, prueba = cap14.consultar_ia("x", "texto")
    assert prueba is True
    post.assert_not_called()


def test_cap14_llamada_real_simulada(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "clave-falsa")
    falsa = respuesta(chat("  - Renovar dominio\n"))
    with mock.patch("requests.post", return_value=falsa) as p:
        texto, prueba = cap14.consultar_ia(
            "Resume", "A" * 5000, max_caracteres=4000
        )
    assert (texto, prueba) == ("- Renovar dominio", False)
    args, kwargs = p.call_args
    assert args[0] == cap14.URL_API
    assert args[0].startswith("https://generativelanguage")
    assert "[" not in args[0]
    assert kwargs["timeout"] == 30
    cab = kwargs["headers"]
    assert cab["Authorization"] == "Bearer clave-falsa"
    carga = kwargs["json"]
    assert carga["model"] == "gemini-3.6-flash"
    assert carga["temperature"] == 0.2
    roles = [m["role"] for m in carga["messages"]]
    assert roles == ["system", "user"]
    assert len(carga["messages"][1]["content"]) == 4000


@pytest.mark.parametrize(
    "efecto",
    [
        requests.ConnectionError("sin red"),
        respuesta({"error": "cuota"}, 429),
        respuesta({"choices": []}),
        respuesta({"sin_choices": True}),
    ],
)
def test_cap14_fallos_vuelven_a_modo_prueba(
    monkeypatch, capsys, efecto
):
    monkeypatch.setenv("GEMINI_API_KEY", "clave-falsa")
    if isinstance(efecto, Exception):
        parche = mock.patch("requests.post", side_effect=efecto)
    else:
        parche = mock.patch("requests.post", return_value=efecto)
    with parche:
        texto, prueba = cap14.consultar_ia("x", "Hola")
    assert prueba is True
    assert texto.startswith("- [SIMULADO]")
    assert "[AVISO API]" in capsys.readouterr().out


def test_cap14_429_da_el_mensaje_del_libro():
    resp = respuesta({"error": "cuota"}, 429)
    with pytest.raises(requests.HTTPError) as err:
        resp.raise_for_status()
    assert str(err.value).startswith(
        "429 Client Error: Too Many Requests for url:"
    )


def test_cap14_main_guarda_markdown(taller, sin_clave):
    cap14.main()
    guardado = (taller / "salida" / "respuesta_ia.md").read_text(
        encoding="utf-8"
    )
    assert "267 caracteres" in guardado


# ---------- Capítulo 15 ----------


@pytest.fixture
def documentos(taller):
    cap15e.main()
    return taller / "entrada" / "documentos_escriba"


def test_cap15_leer_los_tres_formatos(documentos):
    textos = {
        p.name: cap15.leer_documento(p)
        for p in sorted(documentos.iterdir())
    }
    assert [len(t) for t in textos.values()] == [193, 186, 188]
    pdf = textos["03_presupuesto_imprenta.pdf"]
    assert pdf.startswith("PRESUPUESTO IMPRENTA P-2026-44")
    assert "60.00 EUR" in pdf


def test_cap15_ejemplos_con_saltos_unix(documentos):
    for p in documentos.glob("*.*"):
        if p.suffix != ".pdf":
            assert b"\r\n" not in p.read_bytes()


def test_cap15_pdf_sin_texto_no_llama_a_la_ia(taller, capsys):
    carpeta = taller / "docs"
    carpeta.mkdir()
    cap15e.escribir_pdf_minimo(carpeta / "vacio.pdf", [])
    (carpeta / "nada.txt").write_text("   \n", encoding="utf-8")
    with mock.patch.object(cap15, "resumir_con_ia") as ia:
        res = cap15.procesar_carpeta(carpeta)
    ia.assert_not_called()
    assert [r["resumen"] for r in res] == [
        "- *[Documento sin texto extraíble]*"
    ] * 2


def test_cap15_resumen_local():
    texto = "# Título\n\nLínea 2\nLínea 3\nLínea 4\n"
    res = cap15.resumen_local_prueba(texto)
    assert res.splitlines()[:3] == [
        "- Título",
        "- Línea 2",
        "- Línea 3",
    ]
    assert f"{len(texto)} caracteres leídos" in res


def test_cap15_con_clave_pausa_entre_documentos(
    documentos, monkeypatch
):
    monkeypatch.setenv("GEMINI_API_KEY", "clave-falsa")
    falsa = respuesta(chat("- Resumen IA"))
    with mock.patch(
        "requests.post", return_value=falsa
    ) as post, mock.patch("time.sleep") as pausa:
        res = cap15.procesar_carpeta(documentos)
    assert post.call_count == 3
    assert pausa.call_count == 2
    pausa.assert_called_with(2)
    assert all(not r["prueba"] for r in res)
    contenido = post.call_args.kwargs["json"]["messages"][1]
    assert contenido["content"].startswith(
        "Archivo: 03_presupuesto_imprenta.pdf"
    )


def test_cap15_main_de_principio_a_fin(
    documentos, sin_clave, capsys
):
    cap15.main()
    informe = (
        documentos.parent.parent / "salida" / "informe_escriba.md"
    ).read_text(encoding="utf-8")
    assert informe.startswith("# Informe de El Escriba")
    assert informe.count("\n## 0") == 3
    assert "(193 caracteres)" in informe
    assert "Resumen en modo prueba: 188" in informe


def test_cap15_utf8_rebelde():
    malo = "Reunión en Málaga".encode("latin-1")
    with pytest.raises(UnicodeDecodeError) as err:
        malo.decode("utf-8")
    assert "position 5" in str(err.value)


# ---------- Capítulo 16 ----------


def test_cap16_latido_y_lanzador(tmp_path):
    ruta_log = cap16.registrar_latido(tmp_path, True)
    linea = ruta_log.read_text(encoding="utf-8")
    assert "[TAREA_AUTO] OK | Python 3." in linea
    bat = cap16.generar_lanzador_bat(tmp_path).read_bytes()
    assert bat.count(b"\r\n") == 8
    assert b"\r\r\n" not in bat
    assert b'cd /d "%~dp0"\r\n' in bat
    assert b"cap16_latido.py --auto >> salida" in bat


def test_cap16_main_codigo_de_salida(tmp_path, monkeypatch):
    monkeypatch.setattr(
        cap16, "obtener_carpeta_base", lambda: tmp_path
    )
    monkeypatch.setattr(sys, "argv", ["cap16_latido.py"])
    with pytest.raises(SystemExit) as fin:
        cap16.main()
    assert fin.value.code == 0
    assert (tmp_path / "cap16_lanzador.bat").exists()

    def falla(base, auto):
        raise PermissionError("sin permiso")

    monkeypatch.setattr(cap16, "registrar_latido", falla)
    with pytest.raises(SystemExit) as fin:
        cap16.main()
    assert fin.value.code == 1


def campo_cron_valido(campo, minimo, maximo):
    for parte in campo.split(","):
        base, _, paso = parte.partition("/")
        if paso and not paso.isdigit():
            return False
        if base == "*":
            continue
        ini, _, fin = base.partition("-")
        for valor in (ini, fin or ini):
            if not valor.isdigit():
                return False
            if not minimo <= int(valor) <= maximo:
                return False
    return True


def test_cap16_linea_crontab_del_libro():
    md = RAIZ / "manuscrito" / "capitulos"
    texto = (md / "16-programar-tareas.md").read_text(
        encoding="utf-8"
    )
    bloque = re.search(r"```bash\n(.+?)\n```", texto, re.S)
    campos = bloque.group(1).split()
    rangos = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 7)]
    for campo, (lo, hi) in zip(campos[:5], rangos):
        assert campo_cron_valido(campo, lo, hi), campo
    assert campos[5].endswith("/.venv/bin/python")
    assert campos[6].endswith("cap16_latido.py")
    assert campos[7] == "--auto"
    assert campos[-2:] == [campos[-2], "2>&1"]


# ---------- Capítulo 17 ----------


def test_cap17_candidato_y_colision(tmp_path):
    a = tmp_path / "a.BAK"
    a.write_text("x" * 150, encoding="utf-8")
    assert cap17.es_candidato(a, [".bak"], 100)
    assert not cap17.es_candidato(a, [".bak"], 151)
    assert not cap17.es_candidato(tmp_path, [".bak"], 0)
    (tmp_path / "b.tmp").touch()
    (tmp_path / "b_1.tmp").touch()
    libre = cap17.ruta_sin_colision(tmp_path, "b.tmp")
    assert libre.name == "b_2.tmp"


def test_cap17_error_de_disco_no_para_el_lote(
    tmp_path, caplog
):
    archivo = tmp_path / "bloqueado.tmp"
    archivo.touch()
    with mock.patch(
        "shutil.move", side_effect=PermissionError("en uso")
    ), caplog.at_level(logging.INFO):
        ok = cap17.mover_con_seguridad(
            archivo, tmp_path / "dest", simulacion=False
        )
    assert ok is False
    assert archivo.exists()
    assert "No se pudo mover bloqueado.tmp" in caplog.text


def test_cap17_main_simulacion_y_real(
    tmp_path, monkeypatch, caplog
):
    monkeypatch.setattr(cap17, "CARPETA_BASE", tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["x", "--min-bytes", "280"]
    )
    with caplog.at_level(logging.INFO):
        cap17.main()
    assert "Archivos afectados: 1" in caplog.text
    cfg = tmp_path / "entrada" / "config_limpiador.json"
    assert json.loads(cfg.read_text())["min_bytes"] == 100
    assert b"\r\n" not in cfg.read_bytes()

    caplog.clear()
    monkeypatch.setattr(sys, "argv", ["x", "--hacer"])
    with caplog.at_level(logging.INFO):
        cap17.main()
    cuarentena = tmp_path / "salida" / "cuarentena_temp"
    assert sorted(p.name for p in cuarentena.iterdir()) == [
        "cache_01.tmp",
        "copia_vieja.bak",
    ]
    sucia = tmp_path / "entrada" / "taller_sucio"
    assert (sucia / "mini.tmp").exists()


def test_cap17_las_pruebas_del_libro_pasan(tmp_path):
    import test_cap17_limpiador as libro

    for nombre in dir(libro):
        if nombre.startswith("test_"):
            carpeta = tmp_path / nombre
            carpeta.mkdir()
            getattr(libro, nombre)(carpeta)


# ---------- Capítulo 18 ----------


@pytest.fixture
def mayordomo(tmp_path, monkeypatch, sin_clave):
    monkeypatch.setattr(cap18e, "BASE", tmp_path)
    monkeypatch.setattr(cap18, "BASE", tmp_path)
    cap18e.preparar_escenario_mayordomo()
    return tmp_path


def test_cap18_ordenar_simulado_y_real(mayordomo):
    desc = mayordomo / "entrada" / "descargas_mayordomo"
    cats = {".pdf": "Documentos", ".png": "Imagenes"}
    res = cap18.ordenar_descargas(desc, cats, True)
    assert res == "Simulados 4 archivo(s) en Descargas."
    assert len(list(desc.iterdir())) == 4
    (desc / "Otros").mkdir()
    (desc / "Otros" / "gastos_abril.csv").touch()
    res = cap18.ordenar_descargas(desc, cats, False)
    assert res == "Ordenados 4 archivo(s) en Descargas."
    assert (desc / "Otros" / "gastos_abril_1.csv").exists()
    assert (desc / "Documentos" / "recibo_luz.pdf").exists()


def test_cap18_copia_y_rotacion(mayordomo):
    trabajo = mayordomo / "entrada" / "trabajo_mayordomo"
    backups = mayordomo / "copias" / "mayordomo_backups"
    res = cap18.hacer_copia_trabajo(trabajo, backups, 2, True)
    assert "(2 arch., 1 copia(s) rotada(s))" in res
    assert len(list(backups.glob("*.zip"))) == 2

    res = cap18.hacer_copia_trabajo(trabajo, backups, 2, False)
    assert res.startswith("Creado backup_")
    hist = backups / "historico_antiguo"
    assert [p.name for p in hist.iterdir()] == [
        "backup_2026-02-01_080000.zip"
    ]
    nuevo = sorted(backups.glob("backup_*.zip"))[-1]
    with zipfile.ZipFile(nuevo) as zf:
        assert sorted(zf.namelist()) == [
            "clientes.csv",
            "guion_libro.md",
        ]


def test_cap18_tiempo_open_meteo_simulado():
    with mock.patch(
        "requests.get", return_value=respuesta(METEO_HOY)
    ) as get:
        res = cap18.consultar_tiempo_hoy(42.603, -8.644)
    assert res == (
        "8.1 °C a 18.4 °C | Lluvia: 15 % "
        "(Cielo tranquilo) [Open-Meteo]."
    )
    url = get.call_args.args[0]
    assert url == "https://api.open-meteo.com/v1/forecast"
    params = get.call_args.kwargs["params"]
    assert params["forecast_days"] == 1
    assert get.call_args.kwargs["timeout"] == 10


def test_cap18_tiempo_sin_red_y_paraguas(caplog):
    with mock.patch(
        "requests.get",
        side_effect=requests.ConnectionError("sin red"),
    ):
        res = cap18.consultar_tiempo_hoy(0, 0)
    assert res.endswith("(Cielo tranquilo) [Simulado].")
    assert "Usando clima simulado" in caplog.text
    lluvia = json.loads(json.dumps(METEO_HOY))
    lluvia["daily"]["precipitation_probability_max"] = [80]
    with mock.patch(
        "requests.get", return_value=respuesta(lluvia)
    ):
        res = cap18.consultar_tiempo_hoy(0, 0)
    assert "Lluvia: 80 % (Paraguas)" in res


def test_cap18_discord(monkeypatch, capsys, caplog):
    cap18.notificar_parte("Hola")
    assert "Hola" in capsys.readouterr().out
    url = "https://discord.com/api/webhooks/1/abc"
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", url)
    with mock.patch(
        "requests.post", return_value=respuesta("", 204)
    ) as post, caplog.at_level(logging.INFO):
        cap18.notificar_parte("Hola")
    assert post.call_args.kwargs["json"] == {
        "username": "El Mayordomo",
        "content": "Hola",
    }
    assert "enviado a Discord" in caplog.text


def test_cap18_main_sin_red(mayordomo, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["x"])
    with mock.patch(
        "requests.get",
        side_effect=requests.ConnectionError("sin red"),
    ):
        cap18.main()
    out = capsys.readouterr().out
    assert "Simulados 4 archivo(s)" in out
    assert "[Simulado]." in out
    cfg = mayordomo / "entrada" / "mayordomo_config.json"
    assert b"\r\n" not in cfg.read_bytes()


# ---------- Capítulo 19 ----------


@pytest.mark.parametrize(
    "linea, alerta",
    [
        ('ruta = "C:\\\\Users\\\\Ana\\\\x"', True),
        ('ruta = r"C:\\Users\\Ana\\x"', True),
        ("# Copia en c:/users/ana/", True),
        ('ruta = "/home/ana/x"', True),
        ('CLAVE = "AIzaSyFalsa"', True),
        ('URL = "https://discord.com/api/webhooks/1"', True),
        ('correo = "ana@gmail.com"', True),
        ('destino = "yo@ejemplo.local"', False),
        ('"@echo off",', False),
        ("@property", False),
        ("print('hola')", False),
    ],
)
def test_cap19_revisar_linea(linea, alerta):
    assert bool(cap19.revisar_linea(linea)) is alerta


def test_cap19_auditoria_y_archivos(tmp_path, monkeypatch):
    (tmp_path / "bueno.py").write_text("print(1)\n")
    (tmp_path / "malo.py").write_text(
        "x = 1\nruta = '/home/ana/notas'\n"
    )
    venv = tmp_path / ".venv" / "lib"
    venv.mkdir(parents=True)
    (venv / "ajeno.py").write_text("ruta = '/home/x'\n")
    total, alertas = cap19.auditar_codigo(tmp_path)
    assert total == 2
    assert alertas == [
        ("malo.py", 2, "Patrón sensible '/home/'")
    ]
    git = cap19.escribir_gitignore(tmp_path).read_bytes()
    assert b".venv/\n" in git and b"\r\n" not in git
    doc = cap19.escribir_readme(tmp_path, 7).read_text(
        encoding="utf-8"
    )
    assert "Colección de 7 scripts" in doc


def test_cap19_el_auditor_se_salta_a_si_mismo():
    propios = cap19.listar_scripts_py(RAIZ / "codigo")
    nombres = {p.name for p in propios}
    assert "cap19_preparar_entrega.py" not in nombres
    assert "cap18_el_mayordomo.py" in nombres


def test_cap19_codigo_del_libro_sin_alertas():
    total, alertas = cap19.auditar_codigo(RAIZ / "codigo")
    assert total > 30
    assert alertas == []
