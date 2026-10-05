"""Etapa 3: o evento chegou ao lado de leitura."""
from verificador import aguardar, executar, http, verificacao

CONSULTA = "http://localhost:8012"


@verificacao("o lado de leitura já conhece a cliente 'ana' (GET /clientes/ana/resumo)")
def resumo_da_ana():
    url = f"{CONSULTA}/clientes/ana/resumo"
    pronto = aguardar(lambda: http("GET", url)[0] == 200, segundos=6)
    assert pronto, (
        "a 'ana' ainda não aparece no pedidos-consulta. Você criou o pedido da 'ana' na Etapa 2?"
    )


executar()
