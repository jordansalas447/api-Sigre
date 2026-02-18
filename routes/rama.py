from flask import Blueprint, jsonify, request
from ..Reportes.queryreportes import queryReporteCosta
from ..config import get_connection
from ..Tramos.querytramos import queryListarTramos, queryListarTramosdesglosado

rama_bp = Blueprint('rama', __name__, url_prefix='/rama')


@rama_bp.route('/insertar-ramas', methods=['POST'])
def insertar_ramas():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        NombreTramo = request.args.get('NombreTramo')
        
        datos = request.get_json()
        
        if not datos or not isinstance(datos, list):
            return jsonify({"error": "Se requiere una lista de datos en formato JSON"}), 400
        
        resultados = []
        errores = []
        
        ListVanos = [x for x in datos if x.get('TipoElemento') == 'VANO']
        ListPostes = [x for x in datos if x.get('TipoElemento') == 'POST']
                
        for idx, item in enumerate(ListVanos):
            try:
                 #Ejecutar procedimiento almacenado uno por uno
                 #Ajusta el nombre del procedimiento y parámetros según tu BD
                 cursor.execute("SP_Insertar_TRAM_VANO ?, ?, ?", 
                              (item.get('Interno'),
                               item.get('Orden'),
                               NombreTramo))
                 cnxn.commit()
                 resultados.append({"index": idx, "status": "success"})
                #print("")  # Temporalmente solo imprimimos el item
            except Exception as e:
                cnxn.rollback()
                errores.append({"index": idx, "error": str(e)})
                
        for idx, item in enumerate(ListPostes):
            try:
                 #Ejecutar procedimiento almacenado uno por uno
                 #Ajusta el nombre del procedimiento y parámetros según tu BD
                 cursor.execute("SP_Insertar_TRAM_POST ?, ?, ?", 
                              (item.get('Interno'),
                               item.get('Orden'),
                               NombreTramo))
                 cnxn.commit()
                 resultados.append({"index": idx, "status": "success"})
                #print("")  # Temporalmente solo imprimimos el item
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


@rama_bp.route('/listar-tramo', methods=['GET'])
def listar_tramo():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryListarTramos
        
        cursor.execute(query, SEDCodigo)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()    
        
        

@rama_bp.route('/listar-tramo-desglosado', methods=['GET'])
def listar_tramo_desglosado():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')
        CodigoTramo = request.args.get('CodigoTramo')
        TipoElemento = request.args.get('TipoElemento')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryListarTramosdesglosado
        
        cursor.execute(query, SEDCodigo,CodigoTramo,TipoElemento)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()    
        
        
        
@rama_bp.route('/desactivar-codigo-rama', methods=['POST'])
def desactivar_codigo_rama():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')
        CodigoTramo = request.args.get('CodigoTramo')
        TipoElemento = request.args.get('TipoElemento')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = """exec sp_DesactivarTramo ?,?,?"""
        
        try:
            cursor.execute(query, SEDCodigo, TipoElemento, CodigoTramo)
            cnxn.commit()
            if cursor.rowcount > 0:
                return jsonify({
                    "success": True,
                    "message": "El tramo fue desactivado exitosamente"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "No se encontró el tramo o ya estaba desactivado"
                }), 404
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error al desactivar el tramo: {str(e)}"
            }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()    