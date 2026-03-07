from flask import Blueprint, jsonify, request
from ..Carpetas.query import queryEstructuraPresentacion, queryValidarCarpetas , queryCorregirCarpetas, queryobtenerrutaelemento, queryobtenerrutaelementoporCodyTipi, queryobtenerrutaelementoporinterno
from ..config import get_connection
from ..Utils.corregircarpetas import copiar_carpetas_por_codigos
from ..Utils.validarcarpetas import verificar_rutas
import requests
from requests.auth import HTTPBasicAuth

carpetas_bp = Blueprint('carpetas', __name__, url_prefix='/carpetas')
url = "https://api.imagekit.io/v1/files"

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


@carpetas_bp.route('/ObtenerFotosElemento', methods=['GET'])
def ObtenerFotosElemento():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        Interno = request.args.get('Interno')
        TippoElemento = request.args.get('TippoElemento')
        Tipificacion = request.args.get('Tipificacion')

        cursor.execute(queryobtenerrutaelemento, (Interno,TippoElemento,Tipificacion))
        #
        #rows = copiar_carpetas_por_codigos(SEDCodigo,PathRemoto,cursor.fetchall())

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @carpetas_bp.route('/ObtenerFotosElemento', methods=['GET'])
# def ObtenerFotosElemento():
#     try:
#         cnxn = get_connection()
#         cursor = cnxn.cursor()
        
#         Interno = request.args.get('Interno')
#         TippoElemento = request.args.get('TippoElemento')
#         Tipificacion = request.args.get('Tipificacion')

#         cursor.execute(queryobtenerrutaelemento, (Interno,TippoElemento,Tipificacion))
#         #
#         #rows = copiar_carpetas_por_codigos(SEDCodigo,PathRemoto,cursor.fetchall())

#         columns = [column[0] for column in cursor.description]
#         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
#         return jsonify({"data": rows})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@carpetas_bp.route('/ObtenerFotosElementoporinterno', methods=['GET'])
def ObtenerFotosElementoporinterno():
    #try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        CodIns = request.args.get('CodIns')
        Tipi = request.args.get('Tipi')
        ResponseURL = []

        cursor.execute(queryobtenerrutaelementoporCodyTipi, (CodIns,Tipi))
        #
        #rows = copiar_carpetas_por_codigos(SEDCodigo,PathRemoto,cursor.fetchall())
        params = { "path": f"/Fotos-Reportes/{cursor.fetchone()[0]}", "limit": 100    }

        response = requests.get(url,params=params,auth=HTTPBasicAuth("private_/1jjGA95byeV3n8ZIVR0f1CrVMg=", ""))

        files = response.json()
        
        for f in files:
            ResponseURL.append(f["url"])
        #columns = [column[0] for column in cursor.description]
        #rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": ResponseURL})
    #except Exception as e:
        return jsonify({"error": str(e)}), 500



@carpetas_bp.route('/ObtenerEstructuraPresentacion', methods=['GET'])
def ObtenerEstructuraPresentacion():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        CodigoSED = request.args.get('CodigoSED')
        NroOrden = request.args.get('NroOrden')

        cursor.execute(queryEstructuraPresentacion, (NroOrden,CodigoSED))

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return jsonify({"data": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

