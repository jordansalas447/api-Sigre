queryElemetosxSed = """
select 
COUNT(el.TipoElemento) as Total,
el.TipoElemento,
s.SED_Codigo 
from (
select 
VANO_Interno as Interno,
VANO_Codigo as Codigo,
ALIM_Interno as Alim,
VANO_Etiqueta as Etiqueta,
VANO_Subestacion as Sed,
VANO_Terceros as Terceros,
'VANO' as TipoElemento
from Vanos
where VANO_EsBT = 1
union all
select 
POST_Interno as Interno,
POST_CodigoNodo as Codigo,
ALIM_Interno as Alim,
POST_Etiqueta as Etiqueta,
POST_Subestacion as Sed,
POST_Terceros as Terceros,
'POST' as TipoElemento
from Postes
where POST_EsBT = 1 ) as el
inner join Seds s on s.SED_Interno = el.Sed
where s.SED_Codigo = ? and el.Terceros = 0
group by el.TipoElemento,s.SED_Codigo """


queryElemetosNoInspeccionados = """
select distinct
el.Codigo,
el.TipoElemento,
d.DEFI_Estado,
s.SED_Codigo
from (
select 
VANO_Interno as Interno,
VANO_Codigo as Codigo,
ALIM_Interno as Alim,
VANO_Etiqueta as Etiqueta,
VANO_Subestacion as Sed,
VANO_Terceros as Terceros,
'VANO' as TipoElemento
from Vanos
where VANO_EsBT = 1
union all
select 
POST_Interno as Interno,
POST_CodigoNodo as Codigo,
ALIM_Interno as Alim,
POST_Etiqueta as Etiqueta,
POST_Subestacion as Sed,
POST_Terceros as Terceros,
'POST' as TipoElemento
from Postes
where POST_EsBT = 1 ) as el
inner join Seds s on s.SED_Interno = el.Sed
left join (select * from Deficiencias where DEFI_Activo = 1) as d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
--left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
--left join Codigos c on c.CODI_Interno = t.CODI_Interno
where s.SED_Codigo = ? and el.Terceros = 0 and d.DEFI_Estado is null
order by el.Codigo
"""

queryEstadodeElementos = """
select 
    CASE
        WHEN t.TIPI_Interno IS NULL THEN 'No Inspecionado'     
        WHEN t.TIPI_Interno = 0 THEN 'Sin Deficiencia(s)'
        WHEN t.TIPI_Interno <> 0 THEN 'Deficiencia(s)'
    END AS Estado,
COUNT(*) AS Total
from (
select distinct
el.Codigo,
el.TipoElemento,
d.TIPI_Interno,
d.DEFI_Estado,
s.SED_Codigo
from (
select 
VANO_Interno as Interno,
VANO_Codigo as Codigo,
ALIM_Interno as Alim,
VANO_Etiqueta as Etiqueta,
VANO_Subestacion as Sed,
VANO_Terceros as Terceros,
'VANO' as TipoElemento
from Vanos
where VANO_EsBT = 1
union all
select 
POST_Interno as Interno,
POST_CodigoNodo as Codigo,
ALIM_Interno as Alim,
POST_Etiqueta as Etiqueta,
POST_Subestacion as Sed,
POST_Terceros as Terceros,
'POST' as TipoElemento
from Postes
where POST_EsBT = 1 ) as el
inner join Seds s on s.SED_Interno = el.Sed
left join 
(select * from Deficiencias where DEFI_Activo = 1) as d
on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
--left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
--left join Codigos c on c.CODI_Interno = t.CODI_Interno
where s.SED_Codigo = ? and el.Terceros = 0
group by 
el.Codigo,
el.TipoElemento,
d.DEFI_Estado,
d.TIPI_Interno,
s.SED_Codigo,
d.DEFI_Activo
) as t
group by     
    CASE
        WHEN t.TIPI_Interno IS NULL THEN 'No Inspecionado'     
        WHEN t.TIPI_Interno = 0 THEN 'Sin Deficiencia(s)'
        WHEN t.TIPI_Interno <> 0 THEN 'Deficiencia(s)'
    END
"""