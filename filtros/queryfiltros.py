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


queryNodoIF = """
select V.VANO_Codigo,V.VANO_NodoInicial,V.VANO_NodoFinal,S.SED_Codigo from Vanos V
inner join Seds S on V.VANO_Subestacion = S.SED_Interno
where 
(VANO_NodoInicial is null or VANO_NodoFinal is null) and 
VANO_EsBT  = 1 and
VANO_Terceros = 0 and
s.SED_Codigo = ?
"""


queryFechas = """
select 
count(t.FechaRegistro) as Total,
t.FechaRegistro,
t.SED_Codigo
from (
select 
convert(date,d.DEFI_FecRegistro) as FechaRegistro,
s.SED_Codigo 
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
        v.VANO_Subestacion AS Subestacion,
        v.VANO_Terceros as Terceros,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join (select * from Deficiencias d where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioMod
	where el.Terceros = 0 and s.SED_Codigo = ?
    ) as t
    group by t.FechaRegistro, t.SED_Codigo 
"""


queryNroSuministroErroneo = """
	select el.Codigo,d.DEFI_NumSuministro,d.DEFI_TipoElemento,s.SED_Codigo,d.TIPI_Interno from 
	 (   
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
        v.VANO_Subestacion AS Subestacion,
        v.VANO_Terceros as Terceros,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
	inner join (select * from Deficiencias where DEFI_Activo = 1) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
	inner join seds s on s.SED_Interno = el.Subestacion
	where d.TIPI_Interno > 0 and ( LEN(convert(varchar,d.DEFI_NumSuministro)) < 3 or LEN(convert(varchar,d.DEFI_NumSuministro)) > 7  ) and s.SED_Codigo = ?
    """

queryDeficienciaSinCriticidad = """
select DEFI_Interno,DEFI_CodigoElemento,c.CODI_Codigo,DEFI_EstadoCriticidad,s.SED_Codigo
from Deficiencias d inner join
(
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
    ) as el on el.Interno = d.DEFI_IdElemento and el.TipoElemento = d.DEFI_TipoElemento
	inner join Seds s on s.SED_Interno = el.Subestacion
	left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno 
	left join Codigos c on c.CODI_Interno = t.CODI_Interno
where d.TIPI_Interno > 0 and DEFI_EstadoCriticidad = 0 and d.DEFI_Activo = 1 and s.SED_Codigo = ?
"""


query7004y7006en0 = """
select DEFI_Interno,DEFI_CodigoElemento,c.CODI_Codigo,d.DEFI_DistHorizontal,d.DEFI_DistVertical,s.SED_Codigo,d.DEFI_Observacion
from Deficiencias d inner join
(
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
    ) as el on el.Interno = d.DEFI_IdElemento and el.TipoElemento = d.DEFI_TipoElemento
	inner join Seds s on s.SED_Interno = el.Subestacion
	left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno 
	left join Codigos c on c.CODI_Interno = t.CODI_Interno
where 
((c.CODI_Codigo = '7004' and (d.DEFI_DistHorizontal is null or d.DEFI_DistHorizontal = '0')) or (c.CODI_Codigo = '7006' and (d.DEFI_DistVertical is null or d.DEFI_DistVertical = '0'))) 
and d.DEFI_Activo = 1 and s.SED_Codigo = ?
"""