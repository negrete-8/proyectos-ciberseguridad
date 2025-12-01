import argparse
from urllib.parse import urljoin, urlparse
import json
import requests
from bs4 import BeautifulSoup
import re

parser = argparse.ArgumentParser(
    description="Web Spider: URLs, correos y teléfonos."
)


parser.add_argument(
    '-u', '--url',
    type=str,
    required=True,
    help='URL de inicio'
)


parser.add_argument(
    '-d', '--max-depth',
    type=int,
    required=False,
    default=2,
    help='Profundidad máxima de rastreo de la operación'
)


parser.add_argument(
    '-o', '--output',
    type=str,
    required=True,
    help='Archivo donde se registrará el reporte de inteligencia (JSON)'
)

args = parser.parse_args()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://google.com'
}

URL = args.url
Archivo_Salida = args.output
Profundidad = args.max_depth

dominio = urlparse(URL).netloc
print(f"[i] Dominio: {dominio}")

visited_urls = set()
urls_to_visit = []
urls_descubiertas = set()
urls_to_visit.append((URL, 0))
urls_descubiertas.add(URL)
correos_totales = set()
telefonos_totales = set()

patron_Correo = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
patron_telefono = r"(?:\+34\s?)?(?:6|7|8|9)\d{2}[\s\-]?\d{3}[\s\-]?\d{3}"

while urls_to_visit:

    url_actual, nivel_actual = urls_to_visit.pop(0)

    if url_actual in visited_urls:
        continue

    print(f"\n[+] Visitando: {url_actual} (nivel {nivel_actual})")
    visited_urls.add(url_actual)

    try:
        response = requests.get(url_actual, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"[!] Error al acceder a {url_actual}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    codigo_fuente = response.text

    Correos_encontrados = re.findall(patron_Correo, codigo_fuente)
    
    Correos_encontrados = [c for c in Correos_encontrados if not c.lower().endswith(('.jpg', '.png', '.svg', '.gif', '.jpeg'))]

    Telefonos_encontrados = re.findall(patron_telefono, codigo_fuente)

    for c in Correos_encontrados:
        correos_totales.add(c)

    for t in Telefonos_encontrados:
        telefonos_totales.add(t)

    lista_enlaces = soup.find_all('a', href=True)

   
    if nivel_actual < Profundidad:
        for linea in lista_enlaces:
            enlace = linea.get("href")

            url_completa = urljoin(url_actual, enlace)
            parsed = urlparse(url_completa)
            dominio_enlace = parsed.netloc

            if parsed.scheme not in ("http", "https"):
                continue

            if dominio not in dominio_enlace:
                continue

            if url_completa in visited_urls:
                continue

            if url_completa in urls_descubiertas:
                continue

            urls_descubiertas.add(url_completa)
            urls_to_visit.append((url_completa, nivel_actual + 1))


reporte = {
    "urls_monitoreadas": list(visited_urls),
    "correos_encontrados": list(correos_totales),
    "telefonos_encontrados": list(telefonos_totales)
}

with open(Archivo_Salida, "w", encoding="utf-8") as archivo:
    json.dump(reporte, archivo, indent=4, ensure_ascii=False)

print(f"\n[✓] Reporte generado correctamente en: {Archivo_Salida}")
print(f"[i] Total de URLs: {len(visited_urls)}")
print(f"[i] Correos encontrados: {len(correos_totales)}")
print(f"[i] Teléfonos encontrados: {len(telefonos_totales)}")
