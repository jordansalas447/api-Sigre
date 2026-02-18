from pathlib import Path

def analizar_directorio(ruta_base):
    ruta = Path(ruta_base)

    archivos_no_jpg = []
    carpetas_vacias = []

    for elemento in ruta.rglob('*'):
        # Detectar archivos que NO sean .jpg
        if elemento.is_file() and elemento.suffix.lower() != '.jpg':
            archivos_no_jpg.append(elemento)

        # Detectar carpetas vacías
        elif elemento.is_dir():
            if not any(elemento.iterdir()):  # Si no tiene contenido
                carpetas_vacias.append(elemento)

    return archivos_no_jpg, carpetas_vacias


# Cambia esta ruta
ruta = "C:/ruta/a/tu/carpeta"

archivos, carpetas = analizar_directorio(ruta)

print("📁 Archivos que NO son JPG:")
for a in archivos:
    print(a)

print("\n📂 Carpetas vacías:")
for c in carpetas:
    print(c)

print(f"\nTotal archivos no JPG: {len(archivos)}")
print(f"Total carpetas vacías: {len(carpetas)}")
