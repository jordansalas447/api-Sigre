queryBuscarporEtiqueta = """
select 
el.Interno,
el.Codigo,
el.Etiqueta,
el.Latitud,
el.Longitud,
el.Latitud2,
el.Longitud2,
c.CODI_Codigo as Tipificacion,
d.DEFI_EstadoCriticidad as Criticidad,
s.SED_Codigo as Subestacion,
a.ALIM_Etiqueta as Alimentador
from (
       -- POSTES
    SELECT  
        p.POST_Interno        AS Interno,
        p.POST_CodigoNodo     AS Codigo,
        p.POST_Etiqueta AS Etiqueta,
        p.ALIM_Interno AS Alimentador,
        p.POST_Subestacion AS Subestacion,
		p.POST_Latitud as Latitud,
		p.POST_Longitud as Longitud,
		'' as Latitud2,
		'' as Longitud2,
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
		v.VANO_LatitudIni as Latitud,
		v.VANO_LongitudIni as Longitud,
		v.VANO_LatitudFin as Latitud2,
		v.VANO_LongitudFin as Longitud2,
        'VANO' as TipoElemento
    FROM  Vanos v where v.VANO_EsBT = 1
    ) as el 
	left join (select * from Deficiencias where DEFI_Activo = 1) d on 
	d.DEFI_TipoElemento = el.TipoElemento and 
	d.DEFI_IdElemento = el.Interno
	left join Seds s on s.SED_Interno = el.Subestacion
	left join Tipificaciones t on t.TIPI_Interno = d.TIPI_Interno 
	left join Codigos c on c.CODI_Interno = t.CODI_Interno
	left join Alimentadores a on a.ALIM_Interno = el.Alimentador
	where el.Etiqueta = ?
"""