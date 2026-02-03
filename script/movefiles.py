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
select distinct
 iif(t.Origen is null,t.Corregido,t.Origen) as Origen,
 t.Corregido,
 t.CODI_Codigo
from (
select 
CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',CASE WHEN el.TipoElemento = 'POST' THEN 'Poste'  ELSE 'Vano'END,
'/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/',cc.Contador) as Corregido,
c.CODI_Codigo,
t2.Origen
from 
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) 
    as el     
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join (select * from Deficiencias d where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Archivos ar on ar.ARCH_IdElemento = el.Interno and ar.ARCH_TipoElemento = el.TipoElemento
    left join (
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
    where s.SED_Codigo = '2095' and c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno,el.TipoElemento,el.Interno
    ) as cc on d.DEFI_Interno = cc.DEFI_Interno
    left join (   
    select  
        t.DEFI_Interno,
        REPLACE(t.Corregido,'/7004/',Code7004) as Origen
    from (
    select distinct
    d.DEFI_Interno,
    CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',CASE WHEN el.TipoElemento = 'POST' THEN 'Poste'  ELSE 'Vano'END,
    '/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/') as Corregido,
    CONCAT('/7004.1.',d.DEFI_NumSuministro,'/') as Code7004
    from 
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) 
    as el   
    inner join Seds s on el.Subestacion = s.SED_Interno
    inner join Deficiencias d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento 
    inner join Archivos ar on 
            d.DEFI_TipoElemento = ar.ARCH_TipoElemento and 
            d.DEFI_IdElemento = ar.ARCH_IdElemento and
            ar.ARCH_IdElemento = el.Interno and
            ar.ARCH_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    where ar.ARCH_Nombre like '%7004.1.'+d.DEFI_NumSuministro+'%' and s.SED_Codigo = '2095' and c.CODI_Codigo = '7004') as t
    ) as t2 on t2.DEFI_Interno = d.DEFI_Interno
    where s.SED_Codigo = '2095'
    ) as t order by t.CODI_Codigo
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