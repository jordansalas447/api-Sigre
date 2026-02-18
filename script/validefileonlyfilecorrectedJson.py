import json
from pathlib import Path
import pyodbc

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

CONNECTION_STRING2 = (
   r"Driver={ODBC Driver 18 for SQL Server};"
   r"Server=.\SQLEXPRESS;"
   r"Database=Sigre;"
   r"Trusted_Connection=yes;"
   r"TrustServerCertificate=yes;"
)

cnxn = pyodbc.connect(CONNECTION_STRING)
cursor = cnxn.cursor()

query = """
SELECT distinct
CASE 
    WHEN t.CODI_Codigo = '7004' THEN replace(t.Ruta,'/7004/',concat('/7004/',convert(nvarchar,t.Contador),'/'))
      ELSE t.Ruta
END as Corregido,
t.DEFI_Comentario,
t.DEFI_Observacion
FROM (
select * from (
select distinct
d.DEFI_CodigoElemento,
d.DEFI_Activo,
d.DEFI_Comentario,
d.DEFI_Observacion,
CONCAT(
a.ALIM_Etiqueta,
'/',
s.SED_Codigo,
'/',
CASE 
    WHEN el.TipoElemento = 'POST' THEN 'Poste'
    ELSE 'Vano'
END,
'/',
el.Codigo,
'/',
iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),
'/'--,
--t1.Contador,
--iif(t1.Contador is null,'', '/'),
--RIGHT(ar.ARCH_Nombre, CHARINDEX('/', REVERSE(ar.ARCH_Nombre)) - 1)
) as Ruta,
t1.Contador,
c.CODI_Codigo--,
--RIGHT(ar.ARCH_Nombre, CHARINDEX('/', REVERSE(ar.ARCH_Nombre)) - 1) AS NombreArchivo,
--ar.ARCH_Nombre
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0 ) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join (select * from Deficiencias d where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioMod
    left join
    (
    select 
    el.Codigo,
    c.CODI_Codigo,
    d.DEFI_Interno,
    ROW_NUMBER() OVER (PARTITION BY el.Codigo,c.CODI_Codigo ORDER BY el.Codigo,c.CODI_Codigo) AS Contador
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0
    ) as el 
    inner join (select * from Deficiencias where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where s.SED_Codigo = ? and c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
      where s.SED_Codigo = ?) as t
) t
where t.DEFI_Activo = 1
        """


def verificar_rutas(CodIns,PathValide):
    try:
        cursor.execute(query, CodIns, CodIns)
        filas = cursor.fetchall()
        rutas = [PathValide + fila[0] for fila in filas]
        Comentarios = [fila[1] for fila in filas]
        #cnxn.close()

        contador = 0
        total = len(rutas)

        existe_con_foto = 0
        existe_sin_foto = 0
        no_existe = 0
        resultados = []

        for ruta in rutas:
            contador += 1
            if ruta and Path(ruta).exists():
                carpeta = Path(ruta)
                jpgs = list(carpeta.glob("*.jpg")) + list(carpeta.glob("*.jpeg"))
                if not jpgs:
                    existe_sin_foto += 1
                    resultado = {
                        "ruta": ruta,
                        "estado": "existe_sin_foto",
                        "mensaje": f"{ruta} existe pero no tiene archivos JPG",
                        "Comentario": Comentarios[contador-1]
                    }
                    resultados.append(resultado)
                elif len(jpgs) < 4:
                    existe_con_foto += 1
                    resultado = {
                        "ruta": ruta,
                        "estado": "existe_con_foto",
                        "mensaje": f"{ruta} existe y tiene {len(jpgs)} archivos JPG - menos de 4 archivos JPG",
                        "Comentario": Comentarios[contador-1]
                    }
                    resultados.append(resultado)
                # Si hay 4 o más fotos, no se agrega al array
            else:
                no_existe += 1
                resultado = {
                    "ruta": ruta,
                    "estado": "no_existe",
                    "mensaje": f"No existe: {ruta}",
                    "Comentario": Comentarios[contador-1]
                }
                resultados.append(resultado)
    except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Convertir resultados a JSON
    #print(resultados_json)
    return resultados
