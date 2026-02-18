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

#CodIns = '1459'

CodInsList = ['8153']


#cursor.execute(query,CodIns,CodIns,CodIns) 
#row = cursor.fetchone() 

BasePATH = 'D:\\Fotos-Reportes\\'

BasePATHRemoto = '\\\\192.168.1.52\\h\\SubestacionesParaPresentarMejia\\Corregido/'

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
        #print(f"✅ Movido")
    except Exception as e:
        print(f"❌Error al mover carpeta: {e}")

# Ejecutar para cada código en la lista
for CodIns in CodInsList:
    cursor.execute(query,CodIns) 
    row = cursor.fetchone() 
    
    while row: 
        #ruta_origen = "/ruta/original"
        #ruta_destino = "/ruta/nueva_destino"
        mover_estructura_de_carpetas(BasePATHRemoto+row[0], BasePATHRemoto+'Corregido/'+row[0])
        row = cursor.fetchone()