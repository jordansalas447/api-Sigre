from datetime import datetime
from flask import Blueprint, jsonify, request
from ..config import get_connection


deficiencia_bp = Blueprint('deficiencia', __name__, url_prefix='/deficiencia')


ALLOWED_UPDATE_FIELDS = {
    "DEFI_Estado",
    "INSP_Interno",
    "TABL_Interno",
    "DEFI_CodigoElemento",
    "TIPI_Interno",
    "DEFI_NumSuministro",
    "DEFI_FechaDenuncia",
    "DEFI_FechaInspeccion",
    "DEFI_FechaSubsanacion",
    "DEFI_Observacion",
    "DEFI_EstadoSubsanacion",
    "DEFI_Latitud",
    "DEFI_Longitud",
    "DEFI_TipoElemento",
    "DEFI_DistHorizontal",
    "DEFI_DistVertical",
    "DEFI_DistTransversal",
    "DEFI_IdElemento",
    "DEFI_FecRegistro",
    "DEFI_CodDef",
    "DEFI_CodRes",
    "DEFI_CodDen",
    "DEFI_Refer1",
    "DEFI_Refer2",
    "DEFI_CoordX",
    "DEFI_CoordY",
    "DEFI_CodAMT",
    "DEFI_NroOrden",
    "DEFI_PointX",
    "DEFI_PointY",
    "DEFI_UsuCre",
    "DEFI_UsuNPC",
    "DEFI_FecModificacion",
    "DEFI_FechaCreacion",
    "DEFI_TipoMaterial",
    "DEFI_NodoInicial",
    "DEFI_NodoFinal",
    "DEFI_TipoRetenida",
    "DEFI_RetenidaMaterial",
    "DEFI_TipoArmado",
    "DEFI_ArmadoMaterial",
    "DEFI_NumPostes",
    "DEFI_PozoTierra",
    "DEFI_Responsable",
    "DEFI_Comentario",
    "DEFI_PozoTierra2",
    "DEFI_UsuarioInic",
    "DEFI_UsuarioMod",
    "DEFI_Activo",
    "DEFI_EstadoCriticidad",
    "DEFI_Inspeccionado",
    "DEFI_KeyWords",
    "DEFI_Col1",
    "DEFI_Col2",
    "DEFI_Col3",
    "DEFI_Accesibilidad",
    "DEFI_TipoCruce",
}


@deficiencia_bp.route('/<int:defi_interno>', methods=['PUT'])
def actualizar_deficiencia(defi_interno):
    cnxn = None
    cursor = None
    try:
        data = request.get_json(silent=True) or {}

        update_payload = {
            key: value
            for key, value in data.items()
            if key in ALLOWED_UPDATE_FIELDS
        }

        if not update_payload:
            return jsonify({
                "ok": False,
                "error": "No se enviaron campos validos para actualizar."
            }), 400

        if "DEFI_FecModificacion" not in update_payload:
            update_payload["DEFI_FecModificacion"] = datetime.now()

        set_clause = ", ".join([f"{field} = ?" for field in update_payload.keys()])
        params = list(update_payload.values())
        params.append(defi_interno)

        cnxn = get_connection()
        cursor = cnxn.cursor()

        cursor.execute(
            f"UPDATE Deficiencias SET {set_clause} WHERE DEFI_Interno = ?",
            params
        )

        if cursor.rowcount == 0:
            cnxn.rollback()
            return jsonify({
                "ok": False,
                "error": "No se encontro la deficiencia solicitada."
            }), 404

        cnxn.commit()

        return jsonify({
            "ok": True,
            "message": "Deficiencia actualizada correctamente.",
            "DEFI_Interno": defi_interno
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
