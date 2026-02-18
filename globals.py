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


queryTotalFotos = """
    select 
    t.Codigo,
    iif(t.CODI_Codigo is null, 'S/D',t.CODI_Codigo) as Deficiencia,
    count(t.ARCH_CodTabla) as NroFotos 
    from (
    select 
    el.Codigo,c.CODI_Codigo,ar.ARCH_CodTabla
    from (select * from Deficiencias d where d.DEFI_Activo = 1) d
    inner join Archivos ar on ar.ARCH_CodTabla = d.DEFI_Interno
    inner join    
    (-- POSTES
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
    on el.Codigo = d.DEFI_CodigoElemento and el.TipoElemento = d.DEFI_TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    inner join Seds s on s.SED_Interno = el.Subestacion
    where s.SED_Codigo = '8102') as t
    group by t.ARCH_CodTabla,t.CODI_Codigo,t.Codigo
"""


querydeficienciasduplicadas = """
select distinct el.Codigo,c.CODI_Codigo,s.SED_Codigo from 
(select * from Deficiencias where DEFI_Activo = 1) as d
inner join (select * from Deficiencias where DEFI_Activo = 1) as ds 
on d.DEFI_Interno <> ds.DEFI_Interno and 
d.DEFI_Estado = ds.DEFI_Estado and 
d.TIPI_Interno = ds.TIPI_Interno
inner join    
(-- POSTES
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
    on el.Codigo = d.DEFI_CodigoElemento and el.TipoElemento = d.DEFI_TipoElemento
    and el.Codigo = ds.DEFI_CodigoElemento and el.TipoElemento = ds.DEFI_TipoElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where  c.CODI_Codigo <> '7004' or c.CODI_Codigo is null;
"""



queryReporteRevision = """
select distinct
el.Codigo,
el.Etiqueta,
el.TipoElemento,
el.NodoInicial,
el.NodoFinal,
el.DEFI_Latitud,
el.DEFI_Longitud,
--el.DEFI_Estado,
iif( t.Criticidad is null ,convert(nvarchar,el.DEFI_EstadoCriticidad),t.Criticidad) as Criticidad,
iif(t.Tipificacion is null,convert(nvarchar,el.CODI_Codigo),t.Tipificacion) as Tipificacion,
iif(t.ALIM_Etiqueta is null,el.DEFI_CodAMT,t.ALIM_Etiqueta) as Alimentador,
t.SED_Codigo,
iif(el.DEFI_Col2 = 'Terceros',1,0) as Responsable,
iif(t.NumSuministro is null,el.DEFI_NumSuministro,t.NumSuministro) as NumSuministro ,
iif(t.DEFI_DistHorizontal is null,el.DEFI_DistHorizontal,t.DEFI_DistHorizontal) as DistanciaHorizontal,
iif(t.DEFI_DistVertical is null,el.DEFI_DistVertical,t.DEFI_DistVertical) as DEFI_DistVertical,
iif(t.DEFI_FecRegistro is null,convert(date,el.DEFI_FecRegistro),convert(date,t.DEFI_FecRegistro)) as FechaRegistro,
iif(t.Observacion is null,el.DEFI_Observacion,t.Observacion) as Observacion,
iif(t.Comentario is null,el.DEFI_Comentario,t.Comentario) as Comentario,
iif(t.CODI_ComentarioEstandar is null,el.CODI_ComentarioEstandar,t.CODI_ComentarioEstandar) as ComentarioStd,
iif(t.USUA_Nombres is null, el.USUA_Nombres,t.USUA_Nombres) as Inspector,
iif(t.Corregido is null,el.Ruta,t.Corregido) as Corregido
from (
select 
el.*,
u.*,
d.*,
c.CODI_Codigo,
c.CODI_ComentarioEstandar,
CONCAT(
--'D:/Fotos-Reportes/',
a.ALIM_Etiqueta,
'/',
s.SED_Codigo,
'/',
CASE 
    WHEN el.TipoElemento = 'POST' THEN 'Poste'
    ELSE 'Vano'
END,'/',
el.Codigo,
'/',
iif(c.CODI_Codigo is null,'SINDEF',c.CODI_Codigo),'/'
) as Ruta
from
 (   
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
    FROM  Postes p where POST_EsBT = 1 and p.POST_Terceros = 0
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
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0 
  ) as el 
  left join (select * from Deficiencias d where d.DEFI_Activo = 1) as d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
  left join Usuarios u on convert(nvarchar,u.USUA_Interno) = convert(nvarchar,d.DEFI_UsuarioInic)
  left join Seds s on s.SED_Interno = el.Subestacion
  left join Alimentadores a on a.ALIM_Interno = el.Alimentador
  left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
  left join Codigos c on c.CODI_Interno = t.CODI_Interno
) 
as el left  join
(
SELECT distinct
t.Codigo,
t.Etiqueta,
t.DEFI_Interno,
t.TipoElemento,
CASE 
    WHEN t.DEFI_EstadoCriticidad = 1 THEN 'Leve'
    WHEN t.DEFI_EstadoCriticidad = 3 THEN 'Critico'
    WHEN t.DEFI_EstadoCriticidad = 0 THEN 'S/D'
    ELSE CONVERT(nvarchar,t.DEFI_EstadoCriticidad)
END as Criticidad,
iif(t.CODI_Codigo is null,'S/D',t.CODI_Codigo) as Tipificacion,
t.ALIM_Etiqueta ,
t.SED_Codigo,
iif(t.DEFI_NumSuministro is null ,'', t.DEFI_NumSuministro) as NumSuministro,
t.DEFI_DistHorizontal,
t.DEFI_DistVertical,
t.DEFI_FecRegistro,
iif(t.DEFI_Observacion is null, '',t.DEFI_Observacion) as Observacion,
iif(t.DEFI_Comentario is null, '',t.DEFI_Comentario) as Comentario,
t.CODI_ComentarioEstandar,
t.USUA_Nombres,
t.Ruta as Corregido
FROM (
select * from (
select distinct
el.Codigo,
el.Etiqueta,
el.TipoElemento,
d.DEFI_Interno,
d.DEFI_EstadoCriticidad,
c.CODI_Codigo,
c.CODI_ComentarioEstandar,
a.ALIM_Etiqueta,
s.SED_Codigo,
d.DEFI_NumSuministro ,
d.DEFI_DistHorizontal,
d.DEFI_DistVertical,
d.DEFI_FecRegistro,
d.DEFI_Observacion,
d.DEFI_Comentario,
u.USUA_Nombres,
CONCAT(
--'D:/Fotos-Reportes/',
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
'/',t1.Contador
) as Ruta
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
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
    inner join Seds s on el.Subestacion = s.SED_Interno
    left join Deficiencias d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioInic
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
    left join (select * from Deficiencias where DEFI_Activo = 1 ) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where s.SED_Codigo = ? and c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
      where s.SED_Codigo = ? and d.DEFI_Activo = 1) as t
     -- where t.NombreArchivo not like '%.m4a'
) t
-- WHERE t.NombreArchivo NOT LIKE '%.m4a'
) as t on t.Codigo = el.Codigo and t.TipoElemento = el.TipoElemento and t.DEFI_Interno = el.DEFI_Interno
inner join Seds s on s.SED_Interno = el.Subestacion
where s.SED_Codigo = ?
order by iif(t.ALIM_Etiqueta is null,el.DEFI_CodAMT,t.ALIM_Etiqueta) desc
"""


ConsInsTotalDesglosado = """
select * from (
select 
el.Codigo,
iif(c.CODI_Codigo is null,'SIN DEF',c.CODI_Codigo) as Deficiencia,
el.TipoElemento
from (select * from Deficiencias where DEFI_Activo = 1) d 
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ? and el.TipoElemento = ?
) as t
order by t.TipoElemento,t.Deficiencia
"""


TotalDeficienciasxElemento = """
select t.Total,t.Deficiencia,t.TipoElemento from (
select 
iif(t.Deficiencia = 'SIN DEF',3,1) as Orden,
count(t.Deficiencia) as Total,
t.Deficiencia,
t.TipoElemento, 
iif(t.Deficiencia = 'SIN DEF','SIN DEF','CON DEF') as Estado
from (
select
el.Codigo,
iif(c.CODI_Codigo is null,'SIN DEF',c.CODI_Codigo) as Deficiencia,
el.TipoElemento
from (select * from Deficiencias where DEFI_Activo = 1) d  
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ?
) as t 
group by t.Deficiencia,t.TipoElemento

union all

select 
2 as Ordern,
count(t.Deficiencia) as Total,
'TOTAL DEF' as Defiencia,
t.TipoElemento,
t.Deficiencia as Estado 
from (
select
el.Codigo,
iif(c.CODI_Codigo is null,'SIN DEF','CON DEF') as Deficiencia,
el.TipoElemento
from (select * from Deficiencias where DEFI_Activo = 1) d  
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ? and c.CODI_Codigo is not null
) as t 
group by t.Deficiencia,t.TipoElemento

union all 

select 
4 as Ordern,
count(t.Deficiencia) as Total,
'TOTAL' as Defiencia,
t.TipoElemento,
t.Deficiencia as Estado 
from (
select
el.Codigo,
iif(c.CODI_Codigo is null,'TOTAL','TOTAL') as Deficiencia,
el.TipoElemento
from (select * from Deficiencias where DEFI_Activo = 1) d  
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ?
) as t
group by t.Deficiencia,t.TipoElemento
) as t
order by t.TipoElemento,t.Orden
"""

queryTotalElementoInspeccionadosxDeficiencia = """
select  t.Codigo,t.Deficiencia,t.TipoElemento from (
select * from (
select distinct
el.Codigo,
iif(c.CODI_Codigo is null,'SIN DEF','DEF') as Deficiencia,
el.TipoElemento,
iif(c.CODI_Codigo is null,3,1) as Orden
from (select * from Deficiencias where DEFI_Activo = 1) d 
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ? and el.TipoElemento = ?
) as t

union all

select 
convert( varchar,count(t.Deficiencia)) as Total,
t.Deficiencia,
t.TipoElemento,
iif(t.Deficiencia = 'TOTAL SIN DEF',4,2) as Orden
from (
select distinct
el.Codigo,
iif(c.CODI_Codigo is null,'TOTAL SIN DEF','TOTAL DEF') as Deficiencia,
el.TipoElemento
from (select * from Deficiencias where DEFI_Activo = 1) d  
inner join (
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
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = ? and el.TipoElemento = ?
) as t 
group by t.Deficiencia,t.TipoElemento 

) as t
order by TipoElemento, Orden
"""
