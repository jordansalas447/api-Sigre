queryValidarCarpetas = """
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
el.Etiqueta,
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


queryCorregirCarpetas = """
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



queryobtenerrutaelemento = """
    select 
    CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',
    CASE 
    WHEN el.TipoElemento = 'POST' 
    THEN 'Poste'  
    ELSE 'Vano'
    END,
    '/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/',iif(c.CODI_Codigo = 7004,convert(nvarchar,t1.Contador),'')) as Corregido
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
    where c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
    where el.Interno = ? and el.TipoElemento = ? and c.CODI_Codigo = ?
    order by el.Codigo
"""


queryEstructuraPresentacion = """
declare @NroOrden varchar(10) = ?
SELECT 
	concat('OT ',@NroOrden,'/',UPPER(a.ALIM_Etiqueta),'/',s.SED_Codigo,'/',t.letra) as Ruta
FROM Seds s
INNER JOIN Alimentadores a 
    ON s.ALIM_Interno = a.ALIM_Interno
CROSS JOIN (
    SELECT '1 Informe de ejecución' AS letra
    UNION ALL
    SELECT '2 Archivo de fotos/Fotos-Reportes'
    UNION ALL
    SELECT '3 Orden de servicio valorizada'
    UNION ALL
    SELECT '4 Formatos de Seguridad'
) AS t
WHERE s.SED_Codigo = ?;
"""


queryobtenerrutaelementoporinterno = """
    select 
    CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',
    CASE 
    WHEN el.TipoElemento = 'POST' 
    THEN 'Poste'  
    ELSE 'Vano'
    END,
    '/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/',iif(c.CODI_Codigo = 7004,convert(nvarchar,t1.Contador),'')) as Corregido
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
    where c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
    where d.DEFI_Interno = ?
    order by el.Codigo
"""


queryobtenerrutaelementoporCodyTipi = """
    select 
    CONCAT(a.ALIM_Etiqueta,'/',s.SED_Codigo,'/',
    CASE 
    WHEN el.TipoElemento = 'POST' 
    THEN 'Poste'  
    ELSE 'Vano'
    END,
    '/',el.Codigo,'/',iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/',iif(c.CODI_Codigo = 7004,convert(nvarchar,t1.Contador),'')) as Corregido
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
    where c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
    where d.DEFI_CodigoElemento = ? and c.CODI_Codigo = ?
"""
