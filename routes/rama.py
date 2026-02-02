from flask import Blueprint, jsonify, request
from ..Reportes.queryreportes import queryReporteCosta
from ..config import get_connection

rama_bp = Blueprint('rama', __name__, url_prefix='/rama')


@rama_bp.route('/insertar-ramas', methods=['POST'])
def insertar_ramas():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        datos = request.get_json()
        
        if not datos or not isinstance(datos, list):
            return jsonify({"error": "Se requiere una lista de datos en formato JSON"}), 400
        
        resultados = []
        errores = []
        
        for idx, item in enumerate(datos):
            try:
                # Ejecutar procedimiento almacenado uno por uno
                # Ajusta el nombre del procedimiento y parámetros según tu BD
                # cursor.execute("EXEC sp_InsertarRama @param1=?, @param2=?", 
                #              (item.get('param1'), item.get('param2')))
                # cnxn.commit()
                # resultados.append({"index": idx, "status": "success"})
                print(item)  # Temporalmente solo imprimimos el item
            except Exception as e:
                cnxn.rollback()
                errores.append({"index": idx, "error": str(e)})
        
        return jsonify({
            "mensaje": f"Procesados {len(resultados)} registros exitosamente",
            "exitosos": resultados,
            "errores": errores
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()
