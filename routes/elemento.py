from flask import Blueprint, jsonify, request
from ..config import get_connection
from ..elemento.queryelemento import queryupdateposte

elemento_bp = Blueprint('elemento', __name__, url_prefix='/elemento')

@elemento_bp.route('/poste', methods=['POST'])
def validarListado():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()
        
        data = request.get_json()

        POST_Interno = data.get('POST_Interno')
        POST_Etiqueta = data.get('POST_Etiqueta')
        POST_Latitud = data.get('POST_Latitud')
        POST_Longitud = data.get('POST_Longitud')
        ALIM_Interno = data.get('ALIM_Interno')
        POST_CodigoNodo = data.get('POST_CodigoNodo')
        POST_Subestacion = data.get('POST_Subestacion')


        cursor.execute("""EXEC sp_UpdatePostes ?, ?, ?, ?, ?, ?, ?""",
            (POST_Interno,
            POST_Etiqueta,
            POST_Latitud,
            POST_Longitud,
            POST_CodigoNodo,
            ALIM_Interno,
            POST_Subestacion)
        )

        # Obtener la(s) respuesta(s) de la base de datos después de ejecutar el query
        #result = cursor.fetchone()
        cnxn.commit()

        return jsonify({
            "ok": True, 
            "message": "Poste actualizado correctamente"#,
            #"data": result if result is None else dict(zip([column[0] for column in cursor.description], result))
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        cursor.close()
        cnxn.close()