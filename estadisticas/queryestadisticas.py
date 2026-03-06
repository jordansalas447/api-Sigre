queryTotalELementos = """
declare @SED varchar(8) = ?
select 
s.SED_Codigo as SED,
iif(el.Tercero = 1,'SI','NO') as Eliminado,
count(el.Tercero) as Total
from  (   
   -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        p.POST_Etiqueta AS Etiqueta,
        p.ALIM_Interno AS Alimentador,
        p.POST_Subestacion AS Subestacion,
		p.POST_Terceros as Tercero,
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
		v.VANO_Terceros AS Tercero,
        v.VANO_NodoInicial as NodoInicial,
        v.VANO_NodoFinal as NodoFinal,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
	inner join Seds s on s.SED_Interno = el.Subestacion
	where s.SED_Codigo = @SED
	group by el.Tercero , s.SED_Codigo 
	union all
select 
s.SED_Codigo,
'Total' as Eliminado,
count(s.SED_Codigo) as Total
from  (   
   -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        p.POST_Etiqueta AS Etiqueta,
        p.ALIM_Interno AS Alimentador,
        p.POST_Subestacion AS Subestacion,
		p.POST_Terceros as Tercero,
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
		v.VANO_Terceros AS Tercero,
        v.VANO_NodoInicial as NodoInicial,
        v.VANO_NodoFinal as NodoFinal,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1 ) as el
	inner join Seds s on s.SED_Interno = el.Subestacion
	where s.SED_Codigo = @SED
	group by s.SED_Codigo ;
"""


queryElementosInspeccionadosPorInspector = f"""
select 
d.DEFI_CodigoElemento as CodIns,
--d.DEFI_FecModificacion,
CONVERT(VARCHAR(8), d.DEFI_FechaCreacion, 108) as 'Hora de Creación',
d.DEFI_Latitud as Latitud,
d.DEFI_Longitud as Longitud,
ui.USUA_Nombres as Inspector,
iif(c.CODI_Codigo is null,'S/D',c.CODI_Codigo) as Tipificación
--um.USUA_Nombres
from Deficiencias d
inner join Usuarios ui on convert(nvarchar,d.DEFI_UsuarioInic) = convert(nvarchar,ui.USUA_Interno)
inner join Usuarios um on convert(nvarchar,d.DEFI_UsuarioMod) = convert(nvarchar,um.USUA_Interno)
left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno
left join Codigos c on c.CODI_Interno = t.CODI_Interno
where convert(date,d.DEFI_FecRegistro) = ? and d.DEFI_UsuarioInic = ?
order by d.DEFI_Interno desc
"""