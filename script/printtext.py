from PIL import Image, ImageDraw, ImageFont

def imprimir_texto_en_imagen(ruta_imagen, texto, ruta_salida, posicion=(10, 10), tamaño_fuente=40, color=(255,255,255)):
    """
    Dibuja un texto sobre una imagen existente y guarda el resultado.

    ruta_imagen: ruta a la imagen de entrada
    texto: texto a dibujar
    ruta_salida: ruta donde se guardará la imagen modificada
    posicion: tupla (x, y) indicando la posición del texto
    tamaño_fuente: tamaño de la fuente
    color: color del texto, por defecto blanco
    """
    # Abrir la imagen
    imagen = Image.open(ruta_imagen).convert("RGBA")
    # Crear un objeto para dibujar
    dibujo = ImageDraw.Draw(imagen)

    try:
        fuente = ImageFont.truetype("arial.ttf", tamaño_fuente)
    except IOError:
        fuente = ImageFont.load_default()

    # Escribir el texto en la imagen
    dibujo.text(posicion, texto, font=fuente, fill=color)

    # Guardar la imagen resultante
    imagen.save(ruta_salida)

# Ejemplo de uso:
imprimir_texto_en_imagen("imagen.jpg", "Hola, mundo!", "imagen_salida.png", posicion=(200, 200), tamaño_fuente=100, color=(255,0,0))
