from drf_yasg import openapi

limit_param = openapi.Parameter(
    "limit",
    openapi.IN_QUERY,
    description="Número máximo de resultados a retornar por página",
    type=openapi.TYPE_INTEGER,
)

offset_param = openapi.Parameter(
    "offset",
    openapi.IN_QUERY,
    description="Número de resultados a pular antes de começar a retornar as páginas",
    type=openapi.TYPE_INTEGER,
)

symbol_param = openapi.Parameter(
    "symbol",
    openapi.IN_QUERY,
    description="Símbolo da moeda alvo",
    type=openapi.TYPE_STRING,
)

start_date_param = openapi.Parameter(
    "start_date",
    openapi.IN_QUERY,
    description="Data inicial para filtrar as cotações",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)

end_date_param = openapi.Parameter(
    "end_date",
    openapi.IN_QUERY,
    description="Data final para filtrar as cotações",
    type=openapi.TYPE_STRING,
    format=openapi.FORMAT_DATE,
)
