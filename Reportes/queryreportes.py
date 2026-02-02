queryReporteCosta = """
select 
ROW_NUMBER() OVER (ORDER BY t.Codigo) as Item,
'Mejia' as Distrito,
CONCAT('SEAL-',t.ALIM_Etiqueta,'-DEF-',
CASE 
    WHEN t.TipoElemento = 'POST' THEN 'EBT'
    ELSE 'CBT'
END
,'-2026-',ROW_NUMBER() OVER (ORDER BY t.Codigo)) as 'CodigoCorrelativoAutogenerado',
t.SED_Codigo as 'CodigodelaSed',
t.NumSuministro as 'SuministrodeReferencia',
t.NodoInicial as Estructura1,
t.NodoFinal as Estructura2,
t.Codigo as 'CodigoInspeccionado',
CASE 
    WHEN t.TipoElemento = 'POST' THEN 'EBT'
    ELSE 'CBT'
END as 'PuntoInspeccionado',
concat(
CASE 
    WHEN t.TipoElemento = 'POST' THEN 'EBT-'
    ELSE 'CBT-'
END
,
t.Tipificacion) as 'CodigoTipificaciondeladeficiencia',
t.Observacion as 'Descripciondeladeficiencia',
convert(date,t.DEFI_FecRegistro) as 'FechadeIdentificacion',
t.Corregido as 'HipervinculodeRegistroFotografico'
from (
SELECT distinct
t.Codigo,
t.Etiqueta,
t.TipoElemento,
CASE 
    WHEN t.DEFI_EstadoCriticidad = 1 THEN 'Leve'
    WHEN t.DEFI_EstadoCriticidad = 3 THEN 'Critico'
    WHEN t.DEFI_EstadoCriticidad = 0 THEN 'S/D'
    ELSE CONVERT(nvarchar,t.DEFI_EstadoCriticidad)
END as Criticidad,
iif(t.CODI_Codigo is null,'S/D',t.CODI_Codigo) as Tipificacion,
t.ALIM_Etiqueta ,
t.NodoInicial,
t.NodoFinal,
t.SED_Codigo,
iif(t.DEFI_NumSuministro is null ,'', t.DEFI_NumSuministro) as NumSuministro,
t.DEFI_DistHorizontal,
t.DEFI_DistVertical,
t.DEFI_FecRegistro,
iif(t.DEFI_Observacion is null, '',t.DEFI_Observacion) as Observacion,
iif(t.DEFI_Comentario is null, '',t.DEFI_Comentario) as Comentario,
t.USUA_Nombres,
case
       WHEN t.CODI_Codigo = '7004' THEN replace(t.Ruta,'/7004/',concat('/7004/',convert(nvarchar,t.Contador),'/'))
      ELSE t.Ruta--,
end as Corregido
--   seg.value AS segmento_6,
 --   t.ARCH_Nombre
FROM (
select * from (
select distinct
el.Codigo,
el.Etiqueta,
el.TipoElemento,
el.NodoInicial,
el.NodoFinal,
d.DEFI_EstadoCriticidad,
c.CODI_Codigo,
a.ALIM_Etiqueta ,
s.SED_Codigo,
d.DEFI_NumSuministro ,
d.DEFI_DistHorizontal,
d.DEFI_DistVertical,
d.DEFI_FecRegistro,
d.DEFI_Observacion,
d.DEFI_Comentario,
u.USUA_Nombres,
CONCAT(
'D:/Fotos-Reportes/',
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
'/'
--t1.Contador,
--iif(t1.Contador is null,'', '/'),
--RIGHT(ar.ARCH_Nombre, CHARINDEX('/', REVERSE(ar.ARCH_Nombre)) - 1)
) as Ruta,
t1.Contador,
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
        '' as NodoInicial,
        '' as NodoFinal,
        'POST' as TipoElemento
    FROM  Postes p where POST_EsBT = 1
    UNION ALL
    -- VANOS
    SELECT  
        v.VANO_Interno        AS Interno,
        v.VANO_Codigo         AS Codigo,
        v.VANO_Etiqueta AS Etiqueta,
        v.ALIM_Interno AS Alimentador,
        v.VANO_Subestacion AS Subestacion,
        v.VANO_NodoInicial as NodoInicial,
        v.VANO_NodoFinal as NodoFinal,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join Deficiencias d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
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
    FROM  Postes p where POST_EsBT = 1
    UNION ALL
    -- VANOS
    SELECT  
        v.VANO_Interno        AS Interno,
        v.VANO_Codigo         AS Codigo,
        v.VANO_Etiqueta AS Etiqueta,
        v.ALIM_Interno AS Alimentador,
        v.VANO_Subestacion AS Subestacion,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1
    ) as el 
    left join  Deficiencias d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where s.SED_Codigo = ? and c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
      where s.SED_Codigo = ? and d.DEFI_Activo = 1) as t
      where t.NombreArchivo not like '%.m4a' and t.DEFI_EstadoCriticidad in (3,2)
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
WHERE t.NombreArchivo NOT LIKE '%.m4a') as t
where t.Tipificacion <> 'S/D'
"""