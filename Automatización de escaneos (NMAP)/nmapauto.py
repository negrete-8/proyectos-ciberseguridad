import subprocess  
import argparse    


parser = argparse.ArgumentParser(description="Escaneo con nmap")

# argumento 1
parser.add_argument("-t", "--target",
    required=True,
    help="IP del objetivo")

# argumento 2
parser.add_argument("-l", "--port_list",
    required=True,
    help="Lista de puertos")

# argumento 3
parser.add_argument("-s", "--scan_type",
    required=True,
    help="Tipo de escaneo T,S,V")

args = parser.parse_args()  # el que siempre hay que poner

# leer puertos desde el archivo que seleccionamos
puertos = []
with open(args.port_list, 'r') as archivo:
    for line in archivo:
        puertos.append(line.strip())


if args.scan_type.upper() == "T":
    tipo = "-sT"
elif args.scan_type.upper() == "S":
    tipo = "-sS"
elif args.scan_type.upper() == "V":
    tipo = "-sV"
else:
    tipo = "-sS"  # por defecto

# construir comando
comando = ["nmap", tipo, "-p", ",".join(puertos), args.target]

print("Ejecutando:", " ".join(comando))
resultado = subprocess.run(comando, capture_output=True, text=True)
print(resultado.stdout)

# analizar salida y buscar alertas
alertas = []
for linea in resultado.stdout.splitlines():
    if "/tcp" in linea and "open" in linea:
        if "telnet" in linea or "ftp" in linea:
            alertas.append("ALERTA: Servicio inseguro -> " + linea)

# guardar alertas si hay en un archivo txt
if alertas:
    with open("alertas.txt", "w") as f:
        f.write("\n".join(alertas))
    print("Alertas guardadas en alertas.txt")
