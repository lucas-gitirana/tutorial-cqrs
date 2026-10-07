"""Etapa 1: os dois lados do CQRS estão no ar."""
from verificador import executar, http, verificacao

COMANDO = "http://localhost:8011"
CONSULTA = "http://localhost:8012"


@verificacao("pedidos-comando (escrita) responde em http://localhost:8011/saude")
def comando_no_ar():
    status, _ = http("GET", f"{COMANDO}/saude")
    assert status == 200, f"/saude devolveu HTTP {status}."


@verificacao("pedidos-consulta (leitura) responde em http://localhost:8012/saude")
def consulta_no_ar():
    status, _ = http("GET", f"{CONSULTA}/saude")
    assert status == 200, f"/saude devolveu HTTP {status}."


executar(parar_na_primeira_falha=True)
