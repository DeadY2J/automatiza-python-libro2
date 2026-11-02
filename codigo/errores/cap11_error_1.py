# ERROR A PROPÓSITO
import requests

url = "https://pokeapi.co/api/v2/pokemon/noexiste999"
resp = requests.get(url)
datos = resp.json()
