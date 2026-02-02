from flask import Blueprint, jsonify, request
from ..Reportes.queryreportes import queryReporteCosta
from ..config import get_connection

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/reporte-costa', methods=['GET'])
def reporte_costa():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        cursor.execute(queryReporteCosta, (SEDCodigo, SEDCodigo))
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()
