from flask import Blueprint, jsonify, request
from ..config import get_connection

elemento_bp = Blueprint('elemento', __name__, url_prefix='/elemento')

VANO_ALLOWED_FIELDS = {
    "VANO_Codigo",
    "VANO_LatitudIni",
    "VANO_LongitudIni",
    "VANO_LatitudFin",
    "VANO_LongitudFin",
    "ALIM_Interno",
    "VANO_Etiqueta",
    "VANO_Terceros",
    "VANO_Material",
    "VANO_NodoInicial",
    "VANO_NodoFinal",
    "VANO_Inspeccionado",
    "VANO_Subestacion",
    "VANO_EsMT",
    "VANO_EsBT",
    "TRAM_Interno",
    "VANO_Tramo",
}


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


@elemento_bp.route('/vano/<int:vano_interno>', methods=['PUT'])
def actualizar_vano(vano_interno):
    cnxn = None
    cursor = None
    try:
        data = request.get_json(silent=True) or {}
        update_payload = {
            key: value for key, value in data.items()
            if key in VANO_ALLOWED_FIELDS
        }
        if not update_payload:
            return jsonify({
                "ok": False,
                "error": "No se enviaron campos válidos para actualizar.",
            }), 400

        set_clause = ", ".join([f"{field} = ?" for field in update_payload.keys()])
        params = list(update_payload.values()) + [vano_interno]

        cnxn = get_connection()
        cursor = cnxn.cursor()
        cursor.execute(
            f"UPDATE Vanos SET {set_clause} WHERE VANO_Interno = ?",
            params,
        )

        if cursor.rowcount == 0:
            cnxn.rollback()
            return jsonify({
                "ok": False,
                "error": "No se encontró el vano solicitado.",
            }), 404

        cnxn.commit()
        return jsonify({
            "ok": True,
            "message": "Vano actualizado correctamente.",
            "VANO_Interno": vano_interno,
        }), 200

    except Exception as e:
        if cnxn:
            cnxn.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if cnxn:
            cnxn.close()