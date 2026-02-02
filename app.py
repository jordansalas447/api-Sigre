from flask import Flask, send_file, request , jsonify
from flask_cors import CORS
from SigreApiRest.routes.filtros import filtros_bp
from SigreApiRest.routes.reportes import reportes_bp
from SigreApiRest.generarreporteSealV1 import GenerarReporte
from SigreApiRest.config import get_connection
from SigreApiRest.globals import TotalDeficienciasxElemento, queryElemetosxSed , queryElemetosNoInspeccionados ,queryEstadodeElementos,queryReporteRevision,ConsInsTotalDesglosado,queryTotalElementoInspeccionadosxDeficiencia
from SigreApiRest.filtros.queryfiltros import queryElemetosDuplicadosxSed,querySindeffyDeffxSed,queryfiltroArchivosDuplicados
#cnxn = Config.cnxn
#cursor = cnxn.cursor()

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def Inicio():
    return "Hola Mundo"

@app.route('/ExportarReportePresentacionSeal', methods=['POST'])
def ExportarReportePresentacionSeal():

    #try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        CodSubestacion = request.form.get('CodSubestacion') 
        cursor.execute("EXEC sp_ObtenerSEDInterno ?" , CodSubestacion)

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
    

@app.route("/getelementosporsubestacion", methods=["GET"])
def get_elementos_por_subestacion():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        # Ejecutar procedimiento almacenado
        cursor.execute("EXEC sp_elementosporsubestacion ?", SEDCodigo)

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

        # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/getarchivosdeficienciaporelemento", methods=["GET"])
def get_archivos_deficiencia_por_elemento():
    try:
        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')
        Codigo = request.args.get('Codigo')

        # Ejecutar procedimiento almacenado
        cursor.execute("EXEC sp_archivosdeficienciaporelemento ?,?", SEDCodigo,Codigo)

        # Obtener columnas
        columns = [column[0] for column in cursor.description]

        # Convertir resultados a diccionario
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

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
    

@app.route('/historialinspecciones', methods=['GET'])
def historialinspecciones():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        fecha = request.args.get('fecha')

        if not fecha:
            return jsonify({"error": "fecha es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = """
        select 
            d.DEFI_Interno,
            case
                when d.TIPI_Interno <> 0 then 'Deficiencia'
                else 'Sin Deficiencia'
            end as Estado,
            d.DEFI_CodigoElemento,
            c.CODI_Codigo,
            d.DEFI_Latitud,
            d.DEFI_Longitud,
            d.DEFI_NumSuministro,
            d.DEFI_TipoElemento,
            d.DEFI_FecRegistro,
            d.DEFI_Observacion,
            d.DEFI_EstadoCriticidad,
            el.SED_Codigo,
            el.ALIM_Etiqueta,
            u.USUA_Nombres 
        from Deficiencias d
        inner join Usuarios u on d.DEFI_UsuarioInic = u.USUA_Interno
        inner join (
            select t.*, s.SED_Codigo 
            from (
                select
                    'POST' as TipoElemento,
                    p.POST_Interno as IdElemento,
                    p.POST_CodigoNodo as CodIns,
                    p.POST_Etiqueta as CodElemento,
                    p.POST_Subestacion as Subestacion,
                    p.ALIM_Interno,
                    a.ALIM_Codigo,
                    a.ALIM_Etiqueta,
                    p.POST_Latitud as Latitud,
                    p.POST_Longitud as Longitud
                from Postes p
                inner join Alimentadores a on p.ALIM_Interno = a.ALIM_Interno
                union all
                select
                    'VANO' as TipoElemento,
                    v.VANO_Interno,
                    v.VANO_Codigo as CodIns,
                    v.VANO_Etiqueta as CodElemento,
                    v.VANO_Subestacion as Subestacion,
                    v.ALIM_Interno,
                    a.ALIM_Codigo,
                    a.ALIM_Etiqueta,
                    v.VANO_LatitudIni as Latitud,
                    v.VANO_LongitudFin as Longitud
                from Vanos v
                inner join Alimentadores a on v.ALIM_Interno = a.ALIM_Interno
            ) as t
            inner join Seds s on s.SED_Interno = t.Subestacion
        ) el on d.DEFI_IdElemento = el.IdElemento and d.DEFI_TipoElemento = el.TipoElemento
        left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
        left join Codigos c on t.CODI_Interno = c.CODI_Interno
        where Convert(date,DEFI_FecRegistro) = ?
        order by DEFI_Interno desc
        """
        cursor.execute(query, fecha)
        
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


@app.route('/ElemetosxSed', methods=['GET'])
def ElemetosxSed():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryElemetosxSed
        
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

@app.route('/EstadodeElementos', methods=['GET'])
def EstadodeElementos():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryEstadodeElementos
        
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

@app.route('/ElemetosNoInspeccionados', methods=['GET'])
def ElemetosNoInspeccionados():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryElemetosNoInspeccionados
        
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


@app.route('/desglosadoelementosdeficiencia', methods=['GET'])
def desglosadoelementosdeficiencia():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')
        TipoElemento = request.args.get('TipoElemento')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400
        
        if not TipoElemento:
            return jsonify({"error": "TipoElemento es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryTotalElementoInspeccionadosxDeficiencia
        
        cursor.execute(query, SEDCodigo,TipoElemento,SEDCodigo,TipoElemento)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@app.route('/totalelementosxdeficiencias', methods=['GET'])
def totalelementosxdeficiencias():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = TotalDeficienciasxElemento
        
        cursor.execute(query, SEDCodigo,SEDCodigo,SEDCodigo)
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify({
            "data": rows
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@app.route('/exportar-reporte-revision', methods=['GET'])
def ExportarReporteRevision():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        SEDCodigo = request.args.get('SEDCodigo')

        if not SEDCodigo:
            return jsonify({"error": "SEDCodigo es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = queryReporteRevision
        
        cursor.execute(query, SEDCodigo ,SEDCodigo, SEDCodigo)
        
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

# @app.route('/filtro/DeficienciasDuplicadas', methods=['GET'])
# def DeficienciasDuplicadas():
#     try:

#         cnxn = get_connection()
#         cursor = cnxn.cursor()

#         SEDCodigo = request.args.get('SEDCodigo')

#         if not SEDCodigo:
#             return jsonify({"error": "SEDCodigo es requerido"}), 400

#         # ----------- CONSULTA 1 -------------------
#         query = queryElemetosDuplicadosxSed
        
#         cursor.execute(query, SEDCodigo)
        
#         columns = [column[0] for column in cursor.description]
#         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         return jsonify({
#             "data": rows
#         })
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  

#     #finally:
#         #cursor.close()
#         #cnxn.close()  


# @app.route('/filtro/DeficienciasSinDeffconDeff', methods=['GET'])
# def DeficienciasSinDeffconDeff():
#     try:

#         cnxn = get_connection()
#         cursor = cnxn.cursor()

#         SEDCodigo = request.args.get('SEDCodigo')

#         if not SEDCodigo:
#             return jsonify({"error": "SEDCodigo es requerido"}), 400

#         # ----------- CONSULTA 1 -------------------
#         query = querySindeffyDeffxSed
        
#         cursor.execute(query, SEDCodigo)
        
#         columns = [column[0] for column in cursor.description]
#         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         return jsonify({
#             "data": rows
#         })
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  
    


# @app.route('/filtro/ArchivosDuplicados', methods=['GET'])
# def ArchivosDuplicados():
#     try:

#         cnxn = get_connection()
#         cursor = cnxn.cursor()

#         SEDCodigo = request.args.get('SEDCodigo')

#         if not SEDCodigo:
#             return jsonify({"error": "SEDCodigo es requerido"}), 400

#         # ----------- CONSULTA 1 -------------------
#         query = queryfiltroArchivosDuplicados
        
#         cursor.execute(query, SEDCodigo,SEDCodigo)
        
#         columns = [column[0] for column in cursor.description]
#         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

#         return jsonify({
#             "data": rows
#         })
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  


@app.route('/reporteinspectoresxfecha', methods=['GET'])
def reporteinspectoresxfecha():
    try:

        cnxn = get_connection()
        cursor = cnxn.cursor()

        fecha = request.args.get('fecha')

        if not fecha:
            return jsonify({"error": "fecha es requerido"}), 400

        # ----------- CONSULTA 1 -------------------
        query = """
    SELECT 
        COUNT(t.Codigo) AS Total,
        t.TipoElemento,
        t.USUA_Nombres
    FROM (
        SELECT DISTINCT
            el.Codigo,
            el.TipoElemento,
            u.USUA_Nombres
        FROM (   
            -- POSTES
            SELECT  
                p.POST_Interno        AS Interno,
                p.POST_CodigoNodo     AS Codigo,
                p.POST_Etiqueta       AS Etiqueta,
                p.ALIM_Interno        AS Alimentador,
                p.POST_Subestacion    AS Subestacion,
                'POST'                AS TipoElemento
            FROM Postes p 
            WHERE p.POST_EsBT = 1

            UNION ALL

            -- VANOS
            SELECT  
                v.VANO_Interno        AS Interno,
                v.VANO_Codigo         AS Codigo,
                v.VANO_Etiqueta       AS Etiqueta,
                v.ALIM_Interno        AS Alimentador,
                v.VANO_Subestacion    AS Subestacion,
                'VANO'                AS TipoElemento
            FROM Vanos v 
            WHERE v.VANO_EsBT = 1
        ) AS el
        INNER JOIN Seds s 
            ON el.Subestacion = s.SED_Interno
        INNER JOIN Deficiencias d 
            ON d.DEFI_IdElemento = el.Interno 
           AND d.DEFI_TipoElemento = el.TipoElemento
        LEFT JOIN Tipificaciones t 
            ON t.TIPI_Interno = d.TIPI_Interno
        LEFT JOIN Codigos c 
            ON c.CODI_Interno = t.CODI_Interno
        LEFT JOIN Alimentadores a 
            ON a.ALIM_Interno = el.Alimentador
        LEFT JOIN Usuarios u 
            ON u.USUA_Interno = d.DEFI_UsuarioInic
        WHERE CONVERT(DATE, d.DEFI_FechaCreacion) = ?
    ) AS t
    GROUP BY 
        t.USUA_Nombres,
        t.TipoElemento
    ORDER BY 
        t.USUA_Nombres;
        """
        cursor.execute(query, fecha)
        
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

app.register_blueprint(reportes_bp) 
app.register_blueprint(filtros_bp) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')
