from flask import Blueprint, jsonify, request
from app.busqueda.querybusqueda import queryBuscarporEtiqueta
from ..config import get_connection

busqueda_bp = Blueprint('busqueda', __name__, url_prefix='/busqueda')

@busqueda_bp.route('/buscarpostexetiqueta', methods=['GET'])
def reporte_costa():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('Etiqueta')

        if not SEDCodigo:
            return jsonify({"error": "Etiqueta es requerido"}), 400

        cursor.execute(queryBuscarporEtiqueta, (SEDCodigo))
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()





