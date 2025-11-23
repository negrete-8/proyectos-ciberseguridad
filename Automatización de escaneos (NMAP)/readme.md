# proyectos-ciberseguridad
"Ejercicios y prácticas sobre seguridad informática 

## Proyecto: Escaneo automatico para nmap
Este script en Python permite automatizar un escaneo de puertos usando la herramienta nmap. Sus funciones principales son:


Recibe parámetros por consola:

-t → IP del objetivo.
-l → Archivo con lista de puertos a analizar.
-s → Tipo de escaneo (T para TCP Connect, S para SYN Stealth, V para detección de versión).

Lee los puertos desde el archivo indicado..
Ejecuta nmap con subprocess.run() y muestra la salida completa en pantalla
Analiza la salida para detectar puertos abiertos y servicios inseguros como telnet o ftp.
Genera un archivo alertas.txt si encuentra servicios inseguros, guardando las alertas.


## Uso ejemplo
python escaneo.py -t (ip) -l puertos.txt -s S
(sustituir (ip) por el objetivo ejemplo: 192.168.1.1

## Aviso Legal
Este repositorio tiene fines **educativos y demostrativos**.  
**No me hago responsable del uso indebido de los scripts aquí publicados.**  
El uso de estas herramientas para actividades ilegales, sin consentimiento o que vulneren la privacidad de terceros está estrictamente prohibido.  
Por favor, utilízalas únicamente en entornos controlados y con autorización.
