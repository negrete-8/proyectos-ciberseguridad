import argparse
import requests
from bs4 import BeautifulSoup
import time
import re
time.sleep(5) #poner el sleep (IMPORTANTE)

parser = argparse.ArgumentParser(description="webscraping")

#argumento 1
parser.add_argument(
    '-u', '--url',
    type=str,
    help="La URL base que se utilizara"
)

args = parser.parse_args() #parseamos

# ncluya una cabecera User-Agent para simular un navegador legítimo y evitar bloqueos.
URL_OBJETIVO = args.url
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://google.com'
    }

#Use requests para realizar una peticion GET a la URL 

response = requests.get(URL_OBJETIVO, headers=HEADERS)

#Utilice BeautifulSoup para procesar el contenido de la respuesta.
soup = BeautifulSoup(response.text, 'html.parser')

#Extraiga y liste todos los enlaces que apunten a subdominios o rutas internas que contengan las palabras clave: "contacto" o "privacidad".
resultado_enlaces = []

lista_enlaces = soup.find_all('a', href=True)
for linea in lista_enlaces:
    enlace = linea.get("href")
    enlace_min = enlace.lower()
    if "contacto" in enlace_min or "privacidad" in enlace_min:
        resultado_enlaces.append(enlace)

#Utilice el módulo re (Expresiones Regulares) para escanear el texto crudo de la página en busca de:
codigo_fuente = response.text

#Definición de patron para numero telefono
patron_telefono = r"(?:\+34\s?)?(?:6|7|8|9)\d{2}[\s\-]?\d{3}[\s\-]?\d{3}"

# Definición del patro para Correo Electronico
patron_Correo = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

####
Correos_encontrados = re.findall(patron_Correo, codigo_fuente)
Correos_encontrados = [c for c in Correos_encontrados if not c.lower() .endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]

Telefonos_encontrados = re.findall(patron_telefono, codigo_fuente)

print("--- Correos encontrados ---")
for correo in set(Correos_encontrados): 
    print(f"[+] Correo: {correo}")

for numero in set(Telefonos_encontrados):
    print(f"[+] Numero: {numero}")

if resultado_enlaces:
    with open("Reporte.txt", "w") as f:
        f.write("◆◆◆◆ ENLACES ENCONTRADOS ◆◆◆◆\n")  
        for a in resultado_enlaces:
            f.write(a + "\n")

        f.write("\n◆◆◆◆ CORREOS ◆◆◆◆\n")
        for c in set(Correos_encontrados):
            f.write(c + "\n")

        f.write("\n◆◆◆◆ TELEFONOS ◆◆◆◆\n")
        for t in set(Telefonos_encontrados):
            f.write(t + "\n")
