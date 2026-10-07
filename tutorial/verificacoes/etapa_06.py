"""Etapa 6: projeção dos detalhes do pedido, evento PedidoCriado. Testada sem containers."""
from verificador import executar, importar, verificacao

projecoes = importar("servicos/pedidos-consulta", "projecoes")

CRIADO = {"tipo": "PedidoCriado", "dados": {
    "pedido_id": "p1", "cliente": "ana", "total": 65.0, "criado_em": "2026-10-04T10:00:00+00:00",
    "itens": [{"produto": "caneca", "quantidade": 2, "preco": 25.0},
              {"produto": "camiseta", "quantidade": 1, "preco": 15.0}],
}}
CANCELADO = {"tipo": "PedidoCancelado", "dados": {
    "pedido_id": "p1", "cliente": "ana", "total": 65.0, "itens": CRIADO["dados"]["itens"],
    "cancelado_em": "2026-10-04T11:00:00+00:00",
}}


@verificacao("PedidoCriado guarda o documento em modelo.pedidos['<pedido_id>']")
def cria_documento():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    assert "p1" in modelo.pedidos, (
        "modelo.pedidos['p1'] não foi criado. Escreva o 'if evento[\"tipo\"] == \"PedidoCriado\":' da Etapa 6."
    )


@verificacao("o documento tem pedido_id, cliente, status, itens, quantidade_itens, total e criado_em")
def campos_do_documento():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    documento = modelo.pedidos.get("p1") or {}
    esperado = {"pedido_id": "p1", "cliente": "ana", "status": "CRIADO", "itens": CRIADO["dados"]["itens"],
                "quantidade_itens": 3, "total": 65.0, "criado_em": "2026-10-04T10:00:00+00:00"}
    for campo, valor in esperado.items():
        assert documento.get(campo) == valor, f"documento['{campo}'] deveria ser {valor!r}, veio {documento.get(campo)!r}."


executar()
