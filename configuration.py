
# DATABASE
DATABASE = {
    "DB_HOST": "161.35.60.197",
    "DB_SERVICE": "tcs7",
    "DB_USER": "modulo4",
    "DB_PASSWORD": "modulo4"
}

# SITIO-COMPUTRABAJO
COMPUTRABAJO = {
    "WS_PORTAL_LABORAL": "computrabajo",
    "WS_PORTAL_LABORAL_URL": "https://www.computrabajo.com.pe/",
    "WS_PAGINAS": 2,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL": 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_OFERTAS": None,
    # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
    "WS_AREA": None,
    "PAGINADO": "&p="
}

# SITIO-INDEED
INDEED = {
    "WS_PORTAL_LABORAL": "indeed",
    "WS_PORTAL_LABORAL_URL": "https://pe.indeed.com",
    "WS_PAGINAS": 2,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL": 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_OFERTAS": None,
    # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
    "WS_AREA": None,
}

CONVOCATORIATRABAJO = {
    "WS_PORTAL_LABORAL": "convocatoriatrabajo",
    "WS_PORTAL_LABORAL_URL": "https://www.convocatoriasdetrabajo.com/",
    "WS_PAGINAS": 2,  # 500 CANTIDAD DE PAGINAS A SCRAPEAR
    "WS_PAGINA_INICIAL": 1,  # NUMERO DE PAGINA DESDE DONDE SE EMPEZARA A SCRAPEAR
    # CANTIDAD DE OFERTAS POR PAGINA A SCRAPEAR (None: Sin limite)
    "WS_OFERTAS": None,
    # FILTRO DE AREA PARA REALIZAR LA BUSQUEDA (None: Sin filtro)
    "WS_AREA": None,
}