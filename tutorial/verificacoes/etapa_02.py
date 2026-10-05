"""Etapa 2: primeiro comando enviado (pedido criado)."""
from verificador import executar, http, verificacao

COMANDO = "http://localhost:8011"


@verificacao("ao menos um pedido foi gravado pelo lado de comando")
def pedido_criado():
    _, corpo = http("GET", f"{COMANDO}/saude")
    assert corpo.get("pedidos_gravados", 0) >= 1, (
        "nenhum pedido gravado ainda. Clique em ▶ Executar no bloco 'curl -s -X POST ...' desta etapa."
    )


executar()
