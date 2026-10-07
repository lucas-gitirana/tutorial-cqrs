"""Etapa 7: projeção dos detalhes do pedido, evento PedidoCancelado. Testada sem containers."""
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


@verificacao("PedidoCancelado muda o status do documento para CANCELADO")
def cancela_documento():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    projecoes.projetar_pedido(modelo, CANCELADO)
    documento = modelo.pedidos.get("p1") or {}
    assert documento.get("status") == "CANCELADO", f"status: {documento.get('status')!r} (esperado 'CANCELADO')."


@verificacao("PedidoCancelado registra cancelado_em e mantém os outros campos")
def registra_data():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    projecoes.projetar_pedido(modelo, CANCELADO)
    documento = modelo.pedidos.get("p1") or {}
    assert documento.get("cancelado_em") == "2026-10-04T11:00:00+00:00", (
        f"documento['cancelado_em'] = {documento.get('cancelado_em')!r}. Use dados[\"cancelado_em\"]."
    )
    assert documento.get("total") == 65.0, "os demais campos do documento devem ser mantidos."


@verificacao("PedidoCancelado de um pedido desconhecido é ignorado sem erro")
def ignora_desconhecido():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CANCELADO)
    assert "p1" not in modelo.pedidos, "não crie documento a partir de um cancelamento."


executar()
