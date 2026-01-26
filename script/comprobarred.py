import os

ruta = r'\\192.168.1.49\h\Revision\Fotos-Reportes'

try:
    with os.scandir(ruta) as entries:
        carpetas = [e.name for e in entries if e.is_dir()]

    print("Carpetas encontradas:")
    for c in carpetas:
        print(c)

except PermissionError:
    print("No tienes permisos para acceder a la carpeta")
except FileNotFoundError:
    print("La ruta no existe")
