import pyodbc 
import os
import shutil

CONNECTION_STRING = (
   r"Driver={ODBC Driver 18 for SQL Server};"
     r"Server=serversigre.database.windows.net,1433;"
     r"Database=sigre;"
     r"UID=usersigre;"
     r"PWD=Sigrebt#2025;"
     r"Encrypt=yes;"
     r"TrustServerCertificate=no;"
     r"Connection Timeout=30"
     r"MARS_Connection=Yes;"
)

# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect(CONNECTION_STRING)
cursor = cnxn.cursor()

query = """
    select 
    CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',
    CASE 
    WHEN el.TipoElemento = 'POST' 
    THEN 'Poste'  
    ELSE 'Vano'
    END,
    '/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/') as Corregido
    from (   
   -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        p.POST_Etiqueta AS Etiqueta,
        p.ALIM_Interno AS Alimentador,
        p.POST_Subestacion AS Subestacion,
        'POST' as TipoElemento
    FROM  Postes p where POST_EsBT = 1 and p.POST_Terceros = 0
    UNION ALL
    -- VANOS
    SELECT  
        v.VANO_Interno        AS Interno,
        v.VANO_Codigo         AS Codigo,
        v.VANO_Etiqueta AS Etiqueta,
        v.ALIM_Interno AS Alimentador,
        v.VANO_Subestacion AS Subestacion,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) as el 
    left join (select * from Deficiencias where DEFI_Activo = 1 ) d on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
    inner join Alimentadores a on a.ALIM_Interno = el.Alimentador  
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where s.SED_Codigo = ?
    order by el.Codigo
"""


def copiar_carpetas_por_codigos(CodInsList=None, base_path_remoto=None):
    """
    Copia las carpetas para los códigos dados.
    Puede ser llamado desde un endpoint.
    Retorna un resumen del proceso para cada código.
    """
    if CodInsList is None:
        CodInsList = ['8110']
    if base_path_remoto is None:
        base_path_remoto = '\\\\192.168.1.52\\h\\SubestacionesParaPresentarMejia\\'

    resultados = []

    def copiar_estructura_de_carpetas(PATH_origen, PATH_destino):
        try:
            if not os.path.exists(PATH_origen):
                return {"success": False, "error": "Origen no existe", "origen": PATH_origen}

            if not os.path.exists(PATH_destino):
                os.makedirs(PATH_destino)

            contenido_carpeta_origen = os.listdir(PATH_origen)

            for elemento in contenido_carpeta_origen:
                origen = os.path.join(PATH_origen, elemento)
                destino = os.path.join(PATH_destino, elemento)

                if os.path.isdir(origen):
                    shutil.copytree(origen, destino, dirs_exist_ok=True)
                else:
                    shutil.copy2(origen, destino)

            return {"success": True, "origen": PATH_origen, "destino": PATH_destino}

        except Exception as e:
            return {
                "success": False,
                "origen": PATH_origen,
                "destino": PATH_destino,
                "error": str(e)
            }

    for CodIns in CodInsList:
        cursor.execute(query, CodIns)
        row = cursor.fetchone()
        procesados = []

        while row:
            origen = os.path.join(base_path_remoto, row[0])
            destino = os.path.join(base_path_remoto, 'Corregido', row[0])

            resultado = copiar_estructura_de_carpetas(origen, destino)
            procesados.append(resultado)

            row = cursor.fetchone()

        resultados.append({
            "CodIns": CodIns,
            "procesados": procesados
        })

    return resultados