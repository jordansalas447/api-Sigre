import os
import shutil


def copiar_carpetas_por_codigos(CodInsList=None, base_path_remoto=None,ListPath=None):
    """
    Copia las carpetas para los códigos dados.
    Puede ser llamado desde un endpoint.
    Retorna un resumen del proceso para cada código.
    """ 
    
    if CodInsList is None:
        CodInsList = ['8110']
    if base_path_remoto is None:
        base_path_remoto = '\\\\192.168.1.52\\h\\SubestacionesParaPresentarMejia\\'

    resultados = []

    def copiar_estructura_de_carpetas(PATH_origen, PATH_destino):
        try:
            if not os.path.exists(PATH_origen):
                return {"success": False, "error": "Origen no existe", "origen": PATH_origen}

            if not os.path.exists(PATH_destino):
                os.makedirs(PATH_destino)

            contenido_carpeta_origen = os.listdir(PATH_origen)

            for elemento in contenido_carpeta_origen:
                origen = os.path.join(PATH_origen, elemento)
                destino = os.path.join(PATH_destino, elemento)

                if os.path.isdir(origen):
                    shutil.copytree(origen, destino, dirs_exist_ok=True)
                else:
                    shutil.copy2(origen, destino)

            return {"success": True, "origen": PATH_origen, "destino": PATH_destino}

        except Exception as e:
            return {
                "success": False,
                "origen": PATH_origen,
                "destino": PATH_destino,
                "error": str(e)
            }

    procesados = []

    for row in ListPath:
        origen = os.path.join(base_path_remoto, row[0])
        destino = os.path.join(base_path_remoto, 'Corregido', row[0])

        resultado = copiar_estructura_de_carpetas(origen, destino)
        procesados.append(resultado)

    resultados.append({
        "procesados": procesados
    })

    return resultados