"""Etapa 3: projeção dos detalhes do pedido (testada sem subir containers)."""
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


@verificacao("PedidoCriado adiciona o documento em modelo.pedidos com os campos esperados")
def cria_documento():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    documento = modelo.pedidos.get("p1")
    assert documento is not None, "modelo.pedidos['p1'] não foi criado."
    esperado = {"pedido_id": "p1", "cliente": "ana", "status": "CRIADO", "total": 65.0,
                "quantidade_itens": 3, "criado_em": "2026-10-04T10:00:00+00:00"}
    for campo, valor in esperado.items():
        assert documento.get(campo) == valor, f"documento['{campo}'] deveria ser {valor!r}, veio {documento.get(campo)!r}."
    assert documento.get("itens") == CRIADO["dados"]["itens"], "documento['itens'] deveria conter os itens do evento."


@verificacao("PedidoCancelado muda o status do documento para CANCELADO e registra cancelado_em")
def cancela_documento():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CRIADO)
    projecoes.projetar_pedido(modelo, CANCELADO)
    documento = modelo.pedidos.get("p1") or {}
    assert documento.get("status") == "CANCELADO", f"status: {documento.get('status')!r}."
    assert documento.get("cancelado_em") == "2026-10-04T11:00:00+00:00", "documento['cancelado_em'] não foi preenchido."
    assert documento.get("total") == 65.0, "os demais campos do documento devem ser mantidos."


@verificacao("PedidoCancelado de um pedido desconhecido é ignorado sem erro")
def ignora_desconhecido():
    modelo = projecoes.ModeloDeLeitura()
    projecoes.projetar_pedido(modelo, CANCELADO)
    assert "p1" not in modelo.pedidos, "não crie documento a partir de um cancelamento."


executar()
