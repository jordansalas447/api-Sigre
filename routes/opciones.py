from flask import Blueprint, jsonify, request
from ..config import get_connection

opciones_bp = Blueprint('opciones', __name__, url_prefix='/opciones')


@opciones_bp.route('/alimentadores', methods=['GET'])
def alimentadores():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        # ----------- CONSULTA 1 -------------------
        query = """select ALIM_Interno,ALIM_Etiqueta from Alimentadores order by ALIM_Etiqueta"""
        
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@opciones_bp.route('/seds', methods=['GET'])
def seds():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        # ----------- CONSULTA 1 -------------------
        query = """select SED_Interno,SED_Codigo from Seds order by SED_Codigo"""
        
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  