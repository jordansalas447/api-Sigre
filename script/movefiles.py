import pyodbc 
import os
import shutil

CONNECTION_STRING2 = (
   r"Driver={ODBC Driver 18 for SQL Server};"
   r"Server=.\SQLEXPRESS;"
   r"Database=Sigre;"
   r"Trusted_Connection=yes;"
   r"TrustServerCertificate=yes;"
) 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect(CONNECTION_STRING2)
cursor = cnxn.cursor()

query = """
SELECT distinct
CASE 
    WHEN seg.value = '7004' THEN replace(t.Ruta,'/7004/',concat('/',seg.value,'/',convert(nvarchar,t.Contador),'/'))
    ELSE replace(t.Ruta,'/7004/',concat('/',seg.value,'/'))
  --    ELSE t.Ruta
END as Corregido,
CASE 
    WHEN t.CODI_Codigo = '7004' THEN replace(t.Ruta,'/7004/',concat('/7004/',convert(nvarchar,t.Contador),'/'))
      ELSE t.Ruta
END as Corregido2--,
--t.CODI_Codigo,
  --  seg.value AS segmento_6
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
'/'--,t1.Contador
) as Ruta,
t1.Contador,
c.CODI_Codigo,
--replace(ar.ARCH_Nombre,RIGHT(ar.ARCH_Nombre, CHARINDEX('/', REVERSE(ar.ARCH_Nombre)) - 1),'') AS ARCH_Nombre--,
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join (select * from Deficiencias d where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioMod
    left join (
   select * from (
    select distinct
    el.Codigo,
    case 
    when replace(ARCH_Nombre,RIGHT(ARCH_Nombre, CHARINDEX('/', REVERSE(ARCH_Nombre)) - 1),'') 
    like concat('%', d.DEFI_NumSuministro,'%')
    then replace(ARCH_Nombre,RIGHT(ARCH_Nombre, CHARINDEX('/', REVERSE(ARCH_Nombre)) - 1),'') 
    end ARCH_Nombre,
    ARCH_IdElemento,
    ARCH_TipoElemento,
    d.DEFI_Interno--,
    --replace(ARCH_Nombre,RIGHT(ARCH_Nombre, CHARINDEX('/', REVERSE(ARCH_Nombre)) - 1),'') AS ARCH_Nombre 
    from  Archivos a
    inner join Deficiencias d on d.DEFI_IdElemento = a.ARCH_IdElemento and d.DEFI_TipoElemento = a.ARCH_TipoElemento
    inner join 
    (   
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) as el on 
    el.TipoElemento = a.ARCH_TipoElemento and 
    el.Interno = a.ARCH_IdElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    where s.SED_Codigo = ?
    ) as t where t.ARCH_Nombre is not null
    )
    ar on ar.ARCH_IdElemento = el.Interno and ar.ARCH_TipoElemento = el.TipoElemento and d.DEFI_Interno = ar.DEFI_Interno
    left join
    (
    select 
    el.Codigo,
    el.Interno,
    c.CODI_Codigo,
    d.DEFI_Interno,
    el.TipoElemento,
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
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno,el.TipoElemento,el.Interno
     ) as t1 on 
     t1.DEFI_Interno = d.DEFI_Interno -- and 
--     t1.Codigo = d.DEFI_CodigoElemento and 
 --    t1.TipoElemento = d.DEFI_TipoElemento and
  --   t1.TipoElemento = ar.ARCH_TipoElemento and
 ---    t1.Interno = ar.ARCH_IdElemento
      where s.SED_Codigo = ? and d.DEFI_Activo = 1) as t
    --  where t.NombreArchivo not like '%.m4a'
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
"""

CodIns = '2095'

cursor.execute(query,CodIns,CodIns,CodIns) 
row = cursor.fetchone() 

BasePATH = 'D:\\Fotos-Reportes\\'

#BasePATHRemoto = '\\\\192.168.1.52\\h\\Revision\\Arequipa\\Fotos-Reportes\\'

def mover_estructura_de_carpetas(PATH_origen, PATH_destino):
    try:
        if not os.path.exists(PATH_destino):
            os.makedirs(PATH_destino)
        # Mueve la carpeta y su contenido al nuevo destino
        contenido_carpeta_origen = os.listdir(PATH_origen)
        
        for elemento in contenido_carpeta_origen:
            origen = os.path.join(PATH_origen, elemento)
            #destino = os.path.join(PATH_destino, elemento)
            shutil.move(origen, PATH_destino)
        
        #shutil.move(origen, destino)
        print(f"movido")
    except Exception as e:
        print(f"Ocurrió un error al mover la estructura de carpetas: {e}")

# Ejemplo de uso

while row: 
    #ruta_origen = "/ruta/original"
    #ruta_destino = "/ruta/nueva_destino"
    mover_estructura_de_carpetas(BasePATH+row[0], BasePATH+'Corregido/'+row[1])
    row = cursor.fetchone()