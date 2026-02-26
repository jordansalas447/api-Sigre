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
t.CODI_ComentarioEstandar as 'Descripciondeladeficiencia',
t.Criticidad as 'Gravedaddeladeficiencia',
iif(t.DEFI_Col2 = 'Tercero','TERCERO','SEAL') as 'Responsabilidadgeneracióndeficiencia',
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
t.DEFI_Col2,
iif(t.DEFI_NumSuministro is null ,'', t.DEFI_NumSuministro) as NumSuministro,
t.DEFI_DistHorizontal,
t.DEFI_DistVertical,
t.DEFI_FecRegistro,
iif(t.DEFI_Observacion is null, '',t.DEFI_Observacion) as Observacion,
iif(t.DEFI_Comentario is null, '',t.DEFI_Comentario) as Comentario,
--t.USUA_Nombres,
t.CODI_ComentarioEstandar,
t.Ruta as Corregido
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
c.CODI_ComentarioEstandar,
a.ALIM_Etiqueta ,
s.SED_Codigo,
d.DEFI_Col2,
d.DEFI_NumSuministro ,
d.DEFI_DistHorizontal,
d.DEFI_DistVertical,
d.DEFI_FecRegistro,
d.DEFI_Observacion,
d.DEFI_Comentario,
--u.USUA_Nombres,
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
'/',
t1.Contador
) as Ruta,
t1.Contador
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
    left join (select * from Deficiencias where DEFI_Activo = 1 and TIPI_Interno <> 0) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    left join Alimentadores a on a.ALIM_Interno = el.Alimentador
    --left join Usuarios u on u.USUA_Interno = d.DEFI_UsuarioMod
    left join Archivos ar on ar.ARCH_IdElemento = el.Interno and ar.ARCH_TipoElemento = el.TipoElemento
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
    left join (select * from Deficiencias where DEFI_Activo = 1 and TIPI_Interno <> 0) d on d.DEFI_IdElemento = el.Interno and d.DEFI_TipoElemento = el.TipoElemento
    inner join Seds s on s.SED_Interno = el.Subestacion
    left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
    left join Codigos c on c.CODI_Interno = t.CODI_Interno
    where s.SED_Codigo = ? and c.CODI_Codigo = '7004'
    GROUP BY el.Codigo,c.CODI_Codigo,d.DEFI_Interno
     ) as t1 on t1.DEFI_Interno = d.DEFI_Interno
      where s.SED_Codigo = ? and d.DEFI_Activo = 1) as t
) t
) as t
"""



queryValorizacion = """
DECLARE @TipoElemento VARCHAR(10);
DECLARE @SED VARCHAR(10);
Set @SED = ?;
Set @TipoElemento = ?;

select distinct * from (
select 
max(convert(date,d.DEFI_FecRegistro)) as Fecha,
a.ALIM_Etiqueta as Alimentador,
el.NodoInicial,
el.NodoFinal,
el.Etiqueta,
el.Codigo,
iif(el.TipoElemento = 'POST',iif(c.CODI_Codigo is null,'0','1'),'') as 'BT-109',
iif(el.TipoElemento = 'VANO' ,iif(c.CODI_Codigo is null,'0','1'),'') as 'BT-110',
iif(el.TipoElemento = 'POST',iif(c.CODI_Codigo is null,'1','0'),'') as 'BT-111',
iif(el.TipoElemento = 'VANO' ,iif(c.CODI_Codigo is null,'1','0'),'') as 'BT-112',
IIF(el.TipoElemento = 'POST','EBT',el.TipoElemento) as TipoElemento,
iif(el.TipoElemento = 'VANO',CONCAT(el.NodoInicial,'-',el.NodoFinal),el.Etiqueta) as CodigoNodo
from (select * from Deficiencias where DEFI_Activo = 1) d 
inner join (
   -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        '' as NodoInicial,
        '' as NodoFinal,
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
        v.VANO_NodoInicial as NodoInicial,
        v.VANO_NodoFinal as NodoFinal,
        v.VANO_Etiqueta AS Etiqueta,
        v.ALIM_Interno AS Alimentador,
        v.VANO_Subestacion AS Subestacion,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 and v.VANO_Terceros = 0
) as el on el.TipoElemento = d.DEFI_TipoElemento and el.Interno = d.DEFI_IdElemento
inner join Seds s on s.SED_Interno = el.Subestacion
left join Alimentadores a on a.ALIM_Interno = el.Alimentador
left join Tipificaciones t on d.TIPI_Interno = t.TIPI_Interno
left join Codigos c on t.CODI_Interno = c.CODI_Interno
where s.SED_Codigo = @SED and el.TipoElemento =     
CASE 
          WHEN @TipoElemento = 'AMBOS' THEN el.TipoElemento
          ELSE @TipoElemento
END
group by 
a.ALIM_Etiqueta,
el.NodoInicial,
el.NodoFinal,
el.Etiqueta,
el.Codigo,
iif(el.TipoElemento = 'POST',iif(c.CODI_Codigo is null,'0','1'),''),
iif(el.TipoElemento = 'POST',iif(c.CODI_Codigo is null,'1','0'),''),
iif(el.TipoElemento = 'VANO' ,iif(c.CODI_Codigo is null,'0','1'),''),
iif(el.TipoElemento = 'VANO' ,iif(c.CODI_Codigo is null,'1','0'),''),
el.TipoElemento
) as t
order by t.Codigo
"""

