from pathlib import Path
import pyodbc

CONNECTION_STRING3 = (
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

cnxn = pyodbc.connect(CONNECTION_STRING2)
cursor = cnxn.cursor()

query = """
SELECT distinct
CASE 
    WHEN t.CODI_Codigo = '7004' THEN replace(t.Ruta,'/7004/',concat('/7004/',convert(nvarchar,t.Contador),'/'))
      ELSE t.Ruta
END as Corregido
FROM (
select * from (
select distinct
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
c.CODI_Codigo,
RIGHT(ar.ARCH_Nombre, CHARINDEX('/', REVERSE(ar.ARCH_Nombre)) - 1) AS NombreArchivo,
ar.ARCH_Nombre
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
    left join Archivos ar on ar.ARCH_CodTabla = d.DEFI_Interno
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
      where s.SED_Codigo = ? and d.DEFI_Activo = 1) as t
      where t.NombreArchivo not like '%.m4a'
) t
CROSS APPLY (
    SELECT value
    FROM (
        SELECT value,
               ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS pos
        FROM STRING_SPLIT(t.ARCH_Nombre, '/')
    ) x
    WHERE x.pos = 6
) seg
WHERE t.NombreArchivo NOT LIKE '%.m4a';
        """


CodIns = '1609'

cursor.execute(query,CodIns,CodIns)

BASE_ruta = r'D:\Fotos-Reportes/'

#BASE_ruta1 = r'D:\compartir\Fotos-Reportes/'

rutas = [BASE_ruta + fila[0] for fila in cursor.fetchall()]

cnxn.close()

# for ruta in rutas:
#     if ruta and Path(ruta).exists():
#         ""
#     else:
#         print(f"❌ No existe: {ruta}")


for ruta in rutas:
    if ruta and Path(ruta).exists():
        carpeta = Path(ruta)

        jpgs = list(carpeta.glob("*.jpg")) + list(carpeta.glob("*.jpeg"))

        if jpgs:
            ""
            print(f"✅ {ruta} existe y tiene {len(jpgs)} archivos JPG")
        else:   
            print(f"⚠️ {ruta} existe pero no tiene archivos JPG")
    else:
        print(f"❌ No existe: {ruta}")


print("Evaluación completada.")
