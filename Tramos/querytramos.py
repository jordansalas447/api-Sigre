queryListarTramos = """
select count(el.TipoElemento) as Total,el.TipoElemento,t.TRAM_Codigo from Tramos t 
inner join 
(
 select
     'POST' as TipoElemento,
     p.POST_Interno as IdElemento,
     p.POST_CodigoNodo as CodIns,
     p.POST_Etiqueta as CodElemento,
     p.POST_Subestacion as Subestacion,
     p.ALIM_Interno,
     a.ALIM_Codigo,
     a.ALIM_Etiqueta,
     p.POST_Latitud as Latitud,
     p.POST_Longitud as Longitud,
     p.TRAM_Interno as Tramo
 from Postes p
 inner join Alimentadores a on p.ALIM_Interno = a.ALIM_Interno
 union all
 select
     'VANO' as TipoElemento,
     v.VANO_Interno,
     v.VANO_Codigo as CodIns,
     v.VANO_Etiqueta as CodElemento,
     v.VANO_Subestacion as Subestacion,
     v.ALIM_Interno,
     a.ALIM_Codigo,
     a.ALIM_Etiqueta,
     v.VANO_LatitudIni as Latitud,
     v.VANO_LongitudFin as Longitud,
     v.TRAM_Interno as Tramo
 from Vanos v
 inner join Alimentadores a on v.ALIM_Interno = a.ALIM_Interno
) as el on el.Tramo = t.TRAM_Interno
inner join Seds s on s.SED_Interno = el.Subestacion
where s.SED_Codigo = ? and t.TRAM_Activo = 1
group by el.TipoElemento,t.TRAM_Codigo
"""


queryListarTramosdesglosado = """
    declare @SedCodigo VARCHAR(20) = ?
    declare @CodigoTramo VARCHAR(100) = ? 
    declare @TipoElemento VARCHAR(20) = ?

    SELECT 
        el.IdElemento,
        t.TRAM_Orden,
        el.CodIns,
        el.TipoElemento,
        t.TRAM_Codigo
    FROM Tramos t 
    INNER JOIN 
    (
        SELECT
            'POST' as TipoElemento,
            p.POST_Interno as IdElemento,
            p.POST_CodigoNodo as CodIns,
            p.POST_Etiqueta as CodElemento,
            p.POST_Subestacion as Subestacion,
            p.ALIM_Interno,
            a.ALIM_Codigo,
            a.ALIM_Etiqueta,
            p.POST_Latitud as Latitud,
            p.POST_Longitud as Longitud,
            p.TRAM_Interno as Tramo
        FROM Postes p
        INNER JOIN Alimentadores a 
            ON p.ALIM_Interno = a.ALIM_Interno

        UNION ALL

        SELECT
            'VANO' as TipoElemento,
            v.VANO_Interno as IdElemento,
            v.VANO_Codigo as CodIns,
            v.VANO_Etiqueta as CodElemento,
            v.VANO_Subestacion as Subestacion,
            v.ALIM_Interno,
            a.ALIM_Codigo,
            a.ALIM_Etiqueta,
            v.VANO_LatitudIni as Latitud,
            v.VANO_LongitudFin as Longitud,
            v.TRAM_Interno as Tramo
        FROM Vanos v
        INNER JOIN Alimentadores a 
            ON v.ALIM_Interno = a.ALIM_Interno
    ) as el 
        ON el.Tramo = t.TRAM_Interno
    INNER JOIN Seds s 
        ON s.SED_Interno = el.Subestacion
    WHERE 
        s.SED_Codigo = @SedCodigo
        AND (@CodigoTramo = '' OR t.TRAM_Codigo = @CodigoTramo)
        AND (@TipoElemento = '' OR el.TipoElemento = @TipoElemento)
    ORDER BY 
        t.TRAM_Codigo,
        el.TipoElemento,
        t.TRAM_Orden
"""