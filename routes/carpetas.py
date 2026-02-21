from flask import Blueprint, jsonify, request
from ..Carpetas.query import queryValidarCarpetas , queryCorregirCarpetas
from ..config import get_connection
from ..Utils.corregircarpetas import copiar_carpetas_por_codigos
from ..Utils.validarcarpetas import verificar_rutas

carpetas_bp = Blueprint('carpetas', __name__, url_prefix='/carpetas')

@carpetas_bp.route('/validar', methods=['POST'])
def validar():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        SEDCodigo = request.args.get('SEDCodigo')
        data = request.get_json()
        Path = data.get("Path")

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        cursor.execute(queryValidarCarpetas, (SEDCodigo,SEDCodigo))
    
        rows = verificar_rutas(cursor.fetchall(),Path)
        
        #columns = [column[0] for column in cursor.description]
        #rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()

@carpetas_bp.route('/corregir', methods=['POST'])
def corregir():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        SEDCodigo = request.args.get('SEDCodigo')
        data = request.get_json()
        PathRemoto = data.get("Path")

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        cursor.execute(queryCorregirCarpetas, (SEDCodigo))
            
        rows = copiar_carpetas_por_codigos(SEDCodigo,PathRemoto,cursor.fetchall())
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()


@carpetas_bp.route('/validarListado', methods=['GET'])
def validarListado():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        cursor.execute(queryValidarCarpetas, (SEDCodigo,SEDCodigo))
    
        #rows = verificar_rutas(cursor.fetchall(),Path)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()

@carpetas_bp.route('/corregirListado', methods=['GET'])
def corregirListado():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        cursor.execute(queryCorregirCarpetas, (SEDCodigo))
            
        #rows = copiar_carpetas_por_codigos(SEDCodigo,PathRemoto,cursor.fetchall())

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500