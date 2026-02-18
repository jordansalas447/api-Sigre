from pathlib import Path

def buscar_no_jpg(ruta_base):
    ruta = Path(ruta_base)
    for archivo in ruta.rglob('*'):
        if archivo.is_file() and archivo.suffix.lower() != '.jpg':
            print(archivo)

# Cambia esta ruta por la carpeta que quieres analizar
buscar_no_jpg("C:/ruta/a/tu/carpeta")