from flask import Flask, send_file, request , jsonify
from flask_cors import CORS
from generarreporteSealV1 import GenerarReporte
from config import get_connection

#cnxn = Config.cnxn
#cursor = cnxn.cursor()

app = Flask(__name__)
CORS(app)

@app.route('/ExportarReportePresentacionSeal', methods=['POST'])
def ExportarReportePresentacionSeal():

    #try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        CodSubestacion = request.form.get('CodSubestacion') 
        cursor.execute("EXEC sp_ObtenerSEDInterno " + CodSubestacion)

        pathSave = request.form.get('pathSave')
        path = request.form.get('path')
        rows = cursor.fetchone()

        Path, Name_File = GenerarReporte(str(rows[0]), pathSave, path)

        return send_file(Path, as_attachment=True, download_name=Name_File)

    #finally:
        cursor.close()
        #cnxn.close()


@app.route("/alimentadoresetiqueta", methods=["GET"])
def get_alimentadores_etiqueta():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()
    
        # Ejecutar tu procedimiento almacenado
        cursor.execute("EXEC sp_GetAlimentadoresEtiqueta")

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

     # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        #cursor.close()
            #cnxn.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #finally:
        #cursor.close()
        #cnxn.close()
        
    
    
@app.route("/GetSubestacionbyAlimCode", methods=["POST"])
def get_subestacion_by_alim_code():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        data = request.get_json()
        Alimentador = data.get("Alimentador")
        #cursor.open()
        
        # Ejecutar tu procedimiento almacenado
        cursor.execute("EXEC sp_GetSEDCodeByAlim ?", Alimentador)

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

        # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        #cursor.close()
        #cnxn.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #finally:
        #cursor.close()
        #cnxn.close()
    

@app.route("/getsedcodigo", methods=["POST"])
def get_sed_code():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        data = request.get_json()
        SEDCodigo = data.get("SEDCodigo")
        #cursor.open()
        
        # Ejecutar tu procedimiento almacenado
        cursor.execute("EXEC sp_ObtenerSEDInterno ?", SEDCodigo)

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

        # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        #cursor.close()
        #cnxn.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route("/ElementosFaltantes", methods=["POST"])
def Elementos_Faltantes():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        data = request.get_json()
        SEDCodigo = data.get("SEDCodigo")
        #cursor.open()
        
        # Ejecutar tu procedimiento almacenado
        cursor.execute("EXEC sp_ListarPostesYVanosPorSed ?", SEDCodigo)

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

        # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        while cursor.nextset():
            pass

        #cursor.close()
        #cnxn.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #finally:
        #cursor.close()
        #cnxn.close()
    
    
@app.route('/buscarelemento', methods=['GET'])
def buscarelemento():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        codIns = request.args.get('codins')
        Elemento = request.args.get('elemento')

        if not codIns:
            return jsonify({"error": "codIns es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        cursor.execute("exec sp_GetElementoDetailsByCodigo ? , ?", codIns , Elemento)
        
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
    

@app.route('/listardeficienciasxelemento', methods=['GET'])
def listardeficienciasxelemento():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        idelemento = request.args.get('idelemento')
        tipoelemento = request.args.get('tipoelemento')

        if not idelemento:
            return jsonify({"error": "codIns es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        cursor.execute("exec sp_GetDeficienciasPorElemento ? , ?", tipoelemento , idelemento)
        
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



@app.route('/GetLatLongPost', methods=['GET'])
def GetLatLongPost():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        sed_codigo = request.args.get('sedCodigo')

        if not sed_codigo:
            return jsonify({"error": "sedCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        cursor.execute("exec sp_GetListLatLongPOSTbySed ?", sed_codigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    #finally:
        cursor.close()
        #cnxn.close()

@app.route('/GetLatLongVanos', methods=['GET'])
def GetLatLongVanos():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        sed_codigo = request.args.get('sedCodigo')

        if not sed_codigo:
            return jsonify({"error": "sedCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        cursor.execute("exec sp_GetListLatLongVANOSbySed ?", sed_codigo)
        
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


@app.route('/reporteinspectores', methods=['POST','GET'])
def reporteinspectores():  
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        data = request.get_json()
        fecha = data.get("fecha")

        if not fecha:
            return jsonify({"error": "alim  es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        cursor.execute("exec sp_ReporteInspectoresV3 '" + fecha +"'")
        
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
    
@app.route("/insertposte", methods=["POST"])
def insertar_poste():

    cnxn = get_connection()
    cursor = cnxn.cursor()

    data = request.get_json()
    cursor = cnxn.cursor()

    try:
        cursor.execute("""
            EXEC dbo.sp_InsertarPoste
                @POST_Etiqueta = ?,
                @POST_Latitud = ?,
                @POST_Longitud = ?,
                @ALIM_Interno = ?,
                @POST_CodigoNodo = ?,
                @POST_Material = ?,
                @POST_RetenidaTipo = ?,
                @POST_RetenidaMaterial = ?,
                @POST_ArmadoTipo = ?,
                @POST_ArmadoMaterial = ?,
                @POST_Subestacion = ?
        """,
        data.get("POST_Etiqueta"),
        data.get("POST_Latitud"),
        data.get("POST_Longitud"),
        data.get("ALIM_Interno"),
        data.get("POST_CodigoNodo"),
        data.get("POST_Material"),
        data.get("POST_RetenidaTipo"),
        data.get("POST_RetenidaMaterial"),
        data.get("POST_ArmadoTipo"),
        data.get("POST_ArmadoMaterial"),
        data.get("POST_Subestacion")
        )
        
        row = cursor.fetchone()
        poste_id = row[0]
        
        cnxn.commit()


        return jsonify({
            "ok": True,
            "message": "Poste insertado correctamente",
            "POST_Id": poste_id
        }), 201

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500
    
    #finally:
        #cursor.close()
        #cnxn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
