queryupdateposte = """
EXEC sp_UpdatePostes
    @POST_Interno = 266738,
    @POST_Etiqueta = '380500',
    @POST_Latitud = '-15.4316810899702',
    @POST_Longitud = '-74.6093207738535',
    @ALIM_Interno = 200,
    @POST_CodigoNodo = 'PTO000021855',
    @POST_Terceros = 0,
    @POST_Material = null,
    @POST_Inspeccionado = 0,
    @POST_RetenidaTipo = 5,
    @POST_RetenidaMaterial = null,
    @POST_ArmadoTipo = null,
    @POST_ArmadoMaterial = null,
    @POST_Subestacion = null,
    @POST_Altura = null
"""