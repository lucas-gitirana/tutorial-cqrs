"""Etapa 1: ambiente no ar e primeiro pedido criado."""
from verificador import executar, http, verificacao

COMANDO = "http://localhost:8011"
CONSULTA = "http://localhost:8012"


@verificacao("pedidos-comando responde em http://localhost:8011/saude")
def comando_no_ar():
    status, _ = http("GET", f"{COMANDO}/saude")
    assert status == 200, f"/saude devolveu HTTP {status}."


@verificacao("pedidos-consulta responde em http://localhost:8012/saude")
def consulta_no_ar():
    status, _ = http("GET", f"{CONSULTA}/saude")
    assert status == 200, f"/saude devolveu HTTP {status}."


@verificacao("ao menos um pedido foi criado pelo lado de comando")
def pedido_criado():
    _, corpo = http("GET", f"{COMANDO}/saude")
    assert corpo.get("pedidos_gravados", 0) >= 1, (
        "nenhum pedido gravado ainda. Rode o comando 'curl -X POST .../pedidos' desta etapa."
    )


executar(parar_na_primeira_falha=True)
