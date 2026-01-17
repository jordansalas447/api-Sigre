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

cnxn = pyodbc.connect(CONNECTION_STRING3)
cursor = cnxn.cursor()

query = """
select distinct * from (
select distinct
--el.Codigo,
--u.USUA_Nombres,
--replace(replace(replace(ar.ARCH_Nombre,'SIGRE.MOVIL/',''),'Poste','POST'),'Vano','VANO') as Archivo,
concat(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',el.TipoElemento,'/',el.Codigo,'/') as Elemento
from (   
   -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        p.POST_Etiqueta AS Etiqueta,
        p.ALIM_Interno AS Alimentador,
        p.POST_Subestacion AS Subestacion,
        p.POST_Terceros as Terceros,
        'POST' as TipoElemento
    FROM  Postes p where POST_EsBT = 1
    UNION ALL
    -- VANOS
    SELECT  
        v.VANO_Interno        AS Interno,
        v.VANO_Codigo         AS Codigo,
        v.VANO_Etiqueta AS Etiqueta,
        v.ALIM_Interno AS Alimentador,
        v.VANO_Terceros as Terceros,
        v.VANO_Subestacion AS Subestacion,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join Deficiencias d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
--    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
 --   left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioMod
    inner join Archivos ar on ar.ARCH_CodTabla = d.DEFI_Interno
    where el.Terceros = 0 and s.SED_Codigo = ? ) as t order by t.Elemento 
        """

cursor.execute(query,'2095')
rutas = ['D:\\compartir\\Fotos-Reportes\\' + fila[0] for fila in cursor.fetchall()]

cnxn.close()

for ruta in rutas:
    if not Path(ruta).exists():
        print(f"❌ No existe: {ruta}")

print("Evaluación completada.")
