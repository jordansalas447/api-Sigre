queryElemetosDuplicadosxSed = """
select DISTINCT el.Codigo,d.DEFI_Comentario,c.CODI_Codigo from 
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
  FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) as el
inner join 
(
select 
d.DEFI_Interno as Interno,
d.TIPI_Interno as TIPI_Interno1,
d.DEFI_Comentario as DEFI_Comentario1,
d.DEFI_DistHorizontal as DEFI_DistHorizontal1,
d.DEFI_DistVertical as DEFI_DistVertical1,
d.DEFI_Observacion as DEFI_Observacion1,
ds.DEFI_Interno,
ds.TIPI_Interno,
ds.DEFI_IdElemento,
ds.DEFI_TipoElemento,
ds.DEFI_Comentario,
ds.DEFI_DistHorizontal,
ds.DEFI_DistVertical,
ds.DEFI_Observacion,
ds.DEFI_Activo
from Deficiencias d 
inner join Deficiencias ds on 
d.DEFI_Interno <> ds.DEFI_Interno 
and d.TIPI_Interno = ds.TIPI_Interno
and d.DEFI_Activo = ds.DEFI_Activo
and d.DEFI_Activo = 1 and ds.DEFI_Activo = 1
and d.DEFI_CodigoElemento = ds.DEFI_CodigoElemento
and d.DEFI_TipoElemento = ds.DEFI_TipoElemento
and d.DEFI_IdElemento = ds.DEFI_IdElemento
) as d 
on 
d.DEFI_IdElemento = el.Interno 
and d.DEFI_TipoElemento = el.TipoElemento
inner join Seds s on el.Subestacion = s.SED_Interno
left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
left join Codigos c on c.CODI_Interno = t.CODI_Interno
where s.SED_Codigo = ?
order by el.Codigo
"""

querySindeffyDeffxSed = """
select DISTINCT el.Codigo,d.TIPI_Interno,d.DEFI_Comentario,c.CODI_Codigo from 
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
  FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0) as el
inner join 
(
select 
d.DEFI_Interno as Interno,
d.TIPI_Interno as TIPI_Interno1,
d.DEFI_Comentario as DEFI_Comentario1,
d.DEFI_DistHorizontal as DEFI_DistHorizontal1,
d.DEFI_DistVertical as DEFI_DistVertical1,
d.DEFI_Observacion as DEFI_Observacion1,
ds.DEFI_Interno,
ds.TIPI_Interno,
ds.DEFI_IdElemento,
ds.DEFI_TipoElemento,
ds.DEFI_Comentario,
ds.DEFI_DistHorizontal,
ds.DEFI_DistVertical,
ds.DEFI_Observacion,
ds.DEFI_Activo
from Deficiencias d 
inner join Deficiencias ds on 
d.DEFI_Interno <> ds.DEFI_Interno 
and ((d.TIPI_Interno = 0 and ds.TIPI_Interno <> 0)
or (ds.TIPI_Interno = 0 and d.TIPI_Interno <> 0))
and d.DEFI_Activo = ds.DEFI_Activo
and d.DEFI_Activo = 1 and ds.DEFI_Activo = 1
and d.DEFI_CodigoElemento = ds.DEFI_CodigoElemento
and d.DEFI_TipoElemento = ds.DEFI_TipoElemento
and d.DEFI_IdElemento = ds.DEFI_IdElemento
) as d 
on 
d.DEFI_IdElemento = el.Interno 
and d.DEFI_TipoElemento = el.TipoElemento
inner join Seds s on el.Subestacion = s.SED_Interno
left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
left join Codigos c on c.CODI_Interno = t.CODI_Interno
where s.SED_Codigo = ?
order by el.Codigo
"""


queryfiltroArchivosDuplicados = """
select distinct t.* from (
select t.Codigo,t.ARCH_CodTabla,t.RutaOriginal,seg.value from (
select 
el.Codigo,
a.ARCH_CodTabla,
a.ARCH_Nombre,
s.SED_Codigo,
replace( a.ARCH_Nombre,RIGHT(a.ARCH_Nombre, CHARINDEX('/', REVERSE(a.ARCH_Nombre)) - 1),'') as RutaOriginal
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
inner join Archivos a on a.ARCH_TipoElemento = el.TipoElemento and a.ARCH_IdElemento = el.Interno
inner join Seds s on s.SED_Interno = el.Subestacion
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
where t.SED_Codigo = ?
) as t inner join
(select t.Codigo,t.ARCH_CodTabla,t.RutaOriginal,seg.value from (
select 
el.Codigo,
a.ARCH_CodTabla,
a.ARCH_Nombre,
s.SED_Codigo,
replace( a.ARCH_Nombre,RIGHT(a.ARCH_Nombre, CHARINDEX('/', REVERSE(a.ARCH_Nombre)) - 1),'') as RutaOriginal
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
inner join Archivos a on a.ARCH_TipoElemento = el.TipoElemento and a.ARCH_IdElemento = el.Interno
inner join Seds s on s.SED_Interno = el.Subestacion
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
where t.SED_Codigo = ?
) as t2 on t.Codigo = t2.Codigo and t.ARCH_CodTabla <> t2.ARCH_CodTabla and t.value = t2.value;
"""