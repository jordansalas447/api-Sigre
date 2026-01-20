import cv2

# Cargar imagen
imagen = cv2.imread("foto.jpg")

# Verificar que la imagen se cargó
if imagen is None:
    print("Error: no se pudo cargar la imagen")
    exit()

# Texto a escribir
texto = "Texto guardado"

# Escribir texto
cv2.putText(
    imagen,
    texto,
    (100,500),                     # posición (x, y)
    cv2.FONT_HERSHEY_SIMPLEX,       # fuente
    8,                              # tamaño
    (0, 0, 0),                    # color (BGR)
    10,                              # grosor
    cv2.LINE_AA
)

# Guardar imagen con texto
cv2.imwrite("foto_con_texto.jpg", imagen)

print("Imagen guardada correctamente")
