from pathlib import Path

def verificar_rutas(filas,PathValide):
    try:
        rutas = [PathValide + fila[0] for fila in filas]
        Comentarios = [fila[1] for fila in filas]
        #cnxn.close()

        contador = 0
        total = len(rutas)

        existe_con_foto = 0
        existe_sin_foto = 0
        no_existe = 0
        resultados = []

        for ruta in rutas:
            contador += 1
            if ruta and Path(ruta).exists():
                carpeta = Path(ruta)
                jpgs = list(carpeta.glob("*.jpg")) + list(carpeta.glob("*.jpeg"))
                if not jpgs:
                    existe_sin_foto += 1
                    resultado = {
                        "ruta": ruta,
                        "estado": "existe_sin_foto",
                        "mensaje": f"{ruta} existe pero no tiene archivos JPG",
                        "Comentario": Comentarios[contador-1]
                    }
                    resultados.append(resultado)
                elif len(jpgs) < 4:
                    existe_con_foto += 1
                    resultado = {
                        "ruta": ruta,
                        "estado": "existe_con_foto",
                        "mensaje": f"{ruta} existe y tiene {len(jpgs)} archivos JPG - menos de 4 archivos JPG",
                        "Comentario": Comentarios[contador-1]
                    }
                    resultados.append(resultado)
                # Si hay 4 o más fotos, no se agrega al array
            else:
                no_existe += 1
                resultado = {
                    "ruta": ruta,
                    "estado": "no_existe",
                    "mensaje": f"No existe: {ruta}",
                    "Comentario": Comentarios[contador-1]
                }
                resultados.append(resultado)
    except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Convertir resultados a JSON
    #print(resultados_json)
    return resultados
