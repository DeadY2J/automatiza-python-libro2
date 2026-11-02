"""Pruebas de los capítulos 11 a 13 (internet).

No dependen de la red: las respuestas de Open-Meteo, PokéAPI
y books.toscrape.com se simulan con unittest.mock y objetos
requests.Response con la misma forma que las reales.
"""

import json
from unittest import mock

import requests

import cap11_ficha_pokemon as cap11p
import cap11_tiempo_manana as cap11t
import cap12_crear_ejemplos as cap12e
import cap12_lector_web as cap12
import cap13_aviso_correo as cap13c
import cap13_aviso_discord as cap13d


def respuesta(cuerpo, estado=200, tipo="application/json"):
    resp = requests.Response()
    resp.status_code = estado
    if isinstance(cuerpo, (dict, list)):
        cuerpo = json.dumps(cuerpo)
    resp._content = cuerpo.encode("utf-8")
    resp.headers["Content-Type"] = tipo
    resp.url = "https://ejemplo.invalid/"
    return resp


METEO = {
    "latitude": 42.6,
    "longitude": -8.64,
    "generationtime_ms": 0.05,
    "utc_offset_seconds": 7200,
    "timezone": "Europe/Madrid",
    "timezone_abbreviation": "CEST",
    "elevation": 25.0,
    "daily_units": {
        "time": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
        "precipitation_probability_max": "%",
    },
    "daily": {
        "time": ["2026-05-04", "2026-05-05"],
        "temperature_2m_max": [21.3, 17.9],
        "temperature_2m_min": [11.2, 10.4],
        "precipitation_probability_max": [10, 64],
    },
}

CHARIZARD = {
    "id": 6,
    "name": "charizard",
    "height": 17,
    "weight": 905,
    "base_experience": 267,
    "types": [
        {"slot": 1, "type": {"name": "fire", "url": "u"}},
        {"slot": 2, "type": {"name": "flying", "url": "u"}},
    ],
    "stats": [
        {"base_stat": v, "effort": 0, "stat": {"name": n}}
        for n, v in [
            ("hp", 78),
            ("attack", 84),
            ("defense", 78),
            ("special-attack", 109),
            ("special-defense", 85),
            ("speed", 100),
        ]
    ],
}

LIBROS = """<!DOCTYPE html>
<html lang="en-us"><head><meta charset="utf-8">
<title>All products | Books to Scrape - Sandbox</title>
</head><body><section><ol class="row">
<li class="col-xs-6"><article class="product_pod">
  <div class="image_container"><a href="c/a_1000/index.html">
  <img src="m/a.jpg" alt="A Light in the Attic"
   class="thumbnail"></a></div>
  <p class="star-rating Three"><i class="icon-star"></i></p>
  <h3><a href="c/a_1000/index.html"
   title="A Light in the Attic">A Light in the ...</a></h3>
  <div class="product_price">
    <p class="price_color">£51.77</p>
    <p class="instock availability">
      <i class="icon-ok"></i>
        In stock
    </p>
  </div>
</article></li>
<li class="col-xs-6"><article class="product_pod">
  <h3><a href="c/t_999/index.html"
   title="Tipping the Velvet">Tipping the Velvet</a></h3>
  <div class="product_price">
    <p class="price_color">£53.74</p>
    <p class="instock availability">In stock</p>
  </div>
</article></li>
</ol></section></body></html>
"""


# --- Capítulo 11: Open-Meteo ---------------------------------

def test_tiempo_analiza_respuesta_real(taller, capsys):
    with mock.patch(
        "requests.get", return_value=respuesta(METEO)
    ) as get:
        datos, simulado = cap11t.obtener_prevision(42.6, -8.6)
    assert simulado is False
    params = get.call_args.kwargs["params"]
    assert params["forecast_days"] == 2
    assert get.call_args.kwargs["timeout"] == 10
    cap11t.mostrar_y_guardar(datos, simulado)
    salida = capsys.readouterr().out
    assert "PREVISIÓN METEOROLÓGICA (OPEN-METEO)" in salida
    assert "[MAÑANA - 2026-05-05]" in salida
    assert "64 % -> ¡Coge paraguas!" in salida
    guardado = taller / "salida" / "prevision_tiempo.json"
    assert json.loads(guardado.read_text("utf-8")) == METEO


def test_tiempo_sin_red_entra_en_modo_prueba(taller, capsys):
    error = requests.ConnectionError("sin red")
    with mock.patch("requests.get", side_effect=error):
        cap11t.main()
    salida = capsys.readouterr().out
    assert "[MODO PRUEBA] Usando datos simulados." in salida
    assert "PREVISIÓN METEOROLÓGICA (SIMULADO)" in salida
    assert "75 % -> ¡Coge paraguas!" in salida


def test_tiempo_error_http_usa_respaldo(taller):
    error_500 = respuesta("Internal error", 500, "text/plain")
    with mock.patch("requests.get", return_value=error_500):
        datos, simulado = cap11t.obtener_prevision(0, 0)
    assert simulado is True
    assert datos == cap11t.datos_respaldo()


# --- Capítulo 11: PokéAPI ------------------------------------

def test_pokemon_analiza_respuesta_real(capsys):
    with mock.patch(
        "requests.get", return_value=respuesta(CHARIZARD)
    ) as get:
        datos, simulado = cap11p.consultar_pokemon(" Charizard ")
    assert simulado is False
    assert get.call_args.args[0].endswith("/pokemon/charizard")
    cap11p.mostrar_ficha(datos)
    salida = capsys.readouterr().out
    assert "FICHA #006: CHARIZARD" in salida
    assert "Tipos:   fire, flying" in salida
    assert "Altura:  1.7 m" in salida
    assert "Peso:    90.5 kg" in salida
    assert "special-attack  : 109" in salida


def test_pokemon_404_y_sin_red(capsys):
    no_existe = respuesta("Not Found", 404, "text/plain")
    with mock.patch("requests.get", return_value=no_existe):
        datos, simulado = cap11p.consultar_pokemon("x999")
    assert simulado is True
    error = requests.ConnectionError("sin red")
    with mock.patch("requests.get", side_effect=error):
        datos, simulado = cap11p.consultar_pokemon("25")
    assert simulado is True
    cap11p.mostrar_ficha(datos)
    salida = capsys.readouterr().out
    assert "FICHA #025: PIKACHU" in salida
    assert salida.count("    - ") == 6


# --- Capítulo 12: lectura de webs ----------------------------

def test_extraer_productos_de_books_toscrape():
    productos = cap12.extraer_productos(LIBROS)
    assert productos == [
        {
            "titulo": "A Light in the Attic",
            "precio": 51.77,
            "stock": "In stock",
        },
        {
            "titulo": "Tipping the Velvet",
            "precio": 53.74,
            "stock": "In stock",
        },
    ]


def test_extraer_productos_catalogo_local(taller):
    cap12e.crear_html_ejemplo()
    html = (taller / "entrada" / "catalogo_retro.html")
    productos = cap12.extraer_productos(
        html.read_text(encoding="utf-8")
    )
    assert [p["precio"] for p in productos] == [
        34.9, 18.5, 22.0, 14.95
    ]
    assert productos[2]["stock"] == "Últimas unidades"


def test_extraer_productos_sin_precio():
    html = "<article class='product_pod'><h3>X</h3></article>"
    productos = cap12.extraer_productos(html)
    assert productos[0]["precio"] == 0.0
    assert productos[0]["stock"] == "Desconocido"


def falsa_web(robots, estado_robots=200):
    def get(url, headers=None, timeout=None):
        assert timeout is not None
        assert "TallerPythonLibro2" in headers["User-Agent"]
        if url.endswith("/robots.txt"):
            return respuesta(robots, estado_robots, "text/plain")
        return respuesta(LIBROS, 200, "text/html")
    return get


def test_web_en_vivo_simulada(taller):
    local = taller / "no_hace_falta.html"
    with mock.patch(
        "requests.get", side_effect=falsa_web("", 404)
    ), mock.patch("time.sleep") as pausa:
        html, origen = cap12.obtener_html(True, local)
    assert origen == "WEB EN VIVO"
    pausa.assert_called_once_with(1.5)
    assert "A Light in the Attic" in html


def test_robots_que_prohibe_usa_respaldo(taller):
    cap12e.crear_html_ejemplo()
    local = taller / "entrada" / "catalogo_retro.html"
    prohibido = "User-agent: *\nDisallow: /\n"
    with mock.patch(
        "requests.get", side_effect=falsa_web(prohibido)
    ), mock.patch("time.sleep"):
        html, origen = cap12.obtener_html(True, local)
    assert origen == "ARCHIVO LOCAL"


def test_web_sin_red_usa_respaldo(taller):
    cap12e.crear_html_ejemplo()
    local = taller / "entrada" / "catalogo_retro.html"
    error = requests.ConnectionError("sin red")
    with mock.patch("requests.get", side_effect=error), \
            mock.patch("time.sleep"):
        html, origen = cap12.obtener_html(True, local)
    assert origen == "ARCHIVO LOCAL"
    assert "Joystick" in html


# --- Capítulo 13: avisos -------------------------------------

def test_discord_modo_prueba(taller, capsys):
    with mock.patch("requests.post") as post:
        assert cap13d.enviar_aviso_discord("T", "D") is False
    post.assert_not_called()
    salida = capsys.readouterr().out
    assert "[MODO PRUEBA] Falta DISCORD_WEBHOOK_URL." in salida
    assert '"username": "Taller Python"' in salida


def test_discord_envio_simulado(taller, monkeypatch):
    url = "https://discord.invalid/api/webhooks/1/x"
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", url)
    ok = respuesta("", 204, "text/plain")
    with mock.patch("requests.post", return_value=ok) as post:
        assert cap13d.enviar_aviso_discord("T", "D") is True
    carga = post.call_args.kwargs["json"]
    assert carga["content"].startswith("**[T]** (")
    assert post.call_args.kwargs["timeout"] == 10


def test_discord_error_de_red(taller, monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://x.invalid")
    error = requests.ConnectionError("sin red")
    with mock.patch("requests.post", side_effect=error):
        assert cap13d.enviar_aviso_discord("T", "D") is False


def test_correo_modo_prueba(taller, capsys):
    with mock.patch("smtplib.SMTP_SSL") as smtp:
        assert cap13c.enviar_correo("Asunto", "Cuerpo") is False
    smtp.assert_not_called()
    salida = capsys.readouterr().out
    assert "Servidor: smtp.gmail.com:465" in salida
    assert "Para:     destino@ejemplo.local" in salida


def test_correo_envio_simulado(taller, monkeypatch):
    monkeypatch.setenv("SMTP_SERVIDOR", "smtp.ejemplo.invalid")
    monkeypatch.setenv("SMTP_PUERTO", "no-numero")
    monkeypatch.setenv("SMTP_USUARIO", "yo@ejemplo.invalid")
    monkeypatch.setenv("SMTP_CLAVE", "clave-de-prueba")
    monkeypatch.setenv("SMTP_DESTINO", "tu@ejemplo.invalid")
    with mock.patch("smtplib.SMTP_SSL") as smtp:
        assert cap13c.enviar_correo("Asunto", "Cuerpo") is True
    smtp.assert_called_once_with(
        "smtp.ejemplo.invalid", 465, timeout=10
    )
    sesion = smtp.return_value.__enter__.return_value
    sesion.login.assert_called_once_with(
        "yo@ejemplo.invalid", "clave-de-prueba"
    )
    mensaje = sesion.send_message.call_args.args[0]
    assert mensaje["Subject"] == "Asunto"
