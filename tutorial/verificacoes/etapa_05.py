"""Etapa 5: novo modelo de leitura — produtos mais vendidos."""
import uuid

from verificador import aguardar, executar, http, importar, verificacao

projecoes = importar("servicos/pedidos-consulta", "projecoes")
COMANDO = "http://localhost:8011"
CONSULTA = "http://localhost:8012"


def criado(pedido_id, itens):
    return {"tipo": "PedidoCriado", "dados": {"pedido_id": pedido_id, "cliente": "ana", "itens": itens,
                                              "total": 1.0, "criado_em": "2026-10-04T10:00:00+00:00"}}


def cancelado(pedido_id, itens):
    return {"tipo": "PedidoCancelado", "dados": {"pedido_id": pedido_id, "cliente": "ana", "itens": itens,
                                                 "total": 1.0, "cancelado_em": "2026-10-04T11:00:00+00:00"}}


@verificacao("PedidoCriado soma as quantidades de cada produto em modelo.vendas_por_produto")
def soma():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_vendas_por_produto(modelo, criado("a", [{"produto": "caneca", "quantidade": 2, "preco": 1},
                                                               {"produto": "lápis", "quantidade": 5, "preco": 1}]))
    projecoes.projetar_vendas_por_produto(modelo, criado("b", [{"produto": "caneca", "quantidade": 3, "preco": 1}]))
    assert modelo.vendas_por_produto == {"caneca": 5, "lápis": 5}, f"vendas_por_produto = {modelo.vendas_por_produto}"


@verificacao("PedidoCancelado desconta as quantidades do pedido cancelado")
def desconta():
    modelo = projecoes.ModeloDeLeitura()
    itens = [{"produto": "caneca", "quantidade": 2, "preco": 1}]
    projecoes.projetar_vendas_por_produto(modelo, criado("a", itens))
    projecoes.projetar_vendas_por_produto(modelo, criado("b", [{"produto": "caneca", "quantidade": 3, "preco": 1}]))
    projecoes.projetar_vendas_por_produto(modelo, cancelado("a", itens))
    assert modelo.vendas_por_produto.get("caneca") == 3, f"vendas_por_produto = {modelo.vendas_por_produto}"


@verificacao("GET /produtos/mais-vendidos no pedidos-consulta reflete pedidos novos")
def ponta_a_ponta():
    produto = f"produto-verificacao-{uuid.uuid4().hex[:6]}"
    status, corpo = http("POST", f"{COMANDO}/pedidos", {
        "cliente": "verificacao", "itens": [{"produto": produto, "quantidade": 7, "preco": 1.0}],
    })
    assert status == 201, f"falha ao criar pedido: HTTP {status} {corpo}"

    def quantidade_no_ranking():
        _, ranking = http("GET", f"{CONSULTA}/produtos/mais-vendidos?limite=100000")
        return next((linha["quantidade"] for linha in ranking if linha["produto"] == produto), None)

    assert aguardar(quantidade_no_ranking, segundos=10) == 7, (
        "o produto do pedido novo não apareceu no ranking com quantidade 7. "
        "Você reiniciou o pedidos-consulta depois de alterar projecoes.py?"
    )


executar()
