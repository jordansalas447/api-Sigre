from flask import Blueprint, jsonify, request
from SigreApiRest.filtros.queryfiltros import queryElemetosDuplicadosxSed, querySindeffyDeffxSed, queryfiltroArchivosDuplicados , queryNodoIF
from ..config import get_connection

filtros_bp = Blueprint('filtros', __name__, url_prefix='/filtros')


@filtros_bp.route('/DeficienciasDuplicadas', methods=['GET'])
def DeficienciasDuplicadas():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryElemetosDuplicadosxSed
        
        cursor.execute(query, SEDCodigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

    #finally:
        #cursor.close()
        #cnxn.close()  


@filtros_bp.route('/DeficienciasSinDeffconDeff', methods=['GET'])
def DeficienciasSinDeffconDeff():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = querySindeffyDeffxSed
        
        cursor.execute(query, SEDCodigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    


@filtros_bp.route('/ArchivosDuplicados', methods=['GET'])
def ArchivosDuplicados():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryfiltroArchivosDuplicados
        
        cursor.execute(query, SEDCodigo,SEDCodigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@filtros_bp.route('/NodoIF', methods=['GET'])
def NodoIF():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryNodoIF
        
        cursor.execute(query, SEDCodigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  