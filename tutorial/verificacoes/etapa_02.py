"""Etapa 2: comando CancelarPedido (testado sem subir containers)."""
from verificador import executar, importar, verificacao

comandos = importar("servicos/pedidos-comando", "comandos")


class RepositorioFalso:
    def __init__(self):
        self.pedidos = {}

    def inserir_pedido(self, pedido_id, cliente, itens, criado_em):
        total = round(sum(i["quantidade"] * i["preco"] for i in itens), 2)
        self.pedidos[pedido_id] = {"id": pedido_id, "cliente": cliente, "status": "CRIADO",
                                   "itens": itens, "total": total}

    def obter_pedido(self, pedido_id):
        pedido = self.pedidos.get(pedido_id)
        return dict(pedido) if pedido else None

    def atualizar_status(self, pedido_id, status):
        self.pedidos[pedido_id]["status"] = status


def cenario():
    repositorio, publicados = RepositorioFalso(), []
    pedido_id = comandos.criar_pedido(repositorio, publicados.append, {
        "cliente": "ana", "itens": [{"produto": "caneca", "quantidade": 2, "preco": 25.0}],
    })
    publicados.clear()
    return repositorio, publicados, pedido_id


@verificacao("cancelar um pedido existente muda o status para CANCELADO no modelo de escrita")
def muda_status():
    repositorio, publicados, pedido_id = cenario()
    comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    assert repositorio.pedidos[pedido_id]["status"] == "CANCELADO", (
        "o status continua " + repr(repositorio.pedidos[pedido_id]["status"])
        + ". Use repositorio.atualizar_status(pedido_id, 'CANCELADO')."
    )


@verificacao("publica exatamente um evento PedidoCancelado com pedido_id, cliente, itens e total")
def publica_evento():
    repositorio, publicados, pedido_id = cenario()
    comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    assert len(publicados) == 1, f"esperado 1 evento publicado, mas foram {len(publicados)}."
    evento = publicados[0]
    assert evento.get("tipo") == "PedidoCancelado", f"tipo do evento: {evento.get('tipo')!r}."
    dados = evento.get("dados", {})
    for campo, esperado in (("pedido_id", pedido_id), ("cliente", "ana"), ("total", 50.0)):
        assert dados.get(campo) == esperado, f"dados['{campo}'] deveria ser {esperado!r}, veio {dados.get(campo)!r}."
    assert dados.get("itens") == [{"produto": "caneca", "quantidade": 2, "preco": 25.0}], (
        "dados['itens'] deveria trazer os itens do pedido (as projeções precisam deles)."
    )


@verificacao("pedido inexistente gera ErroDeComando com status 404 e nenhum evento")
def inexistente():
    repositorio, publicados, _ = cenario()
    try:
        comandos.cancelar_pedido(repositorio, publicados.append, "nao-existe")
    except comandos.ErroDeComando as erro:
        assert erro.status == 404, f"status do erro: {erro.status} (esperado 404)."
    else:
        raise AssertionError("nenhum ErroDeComando foi lançado.")
    assert not publicados, "nenhum evento deveria ser publicado quando o comando é rejeitado."


@verificacao("cancelar duas vezes gera ErroDeComando com status 409 na segunda vez")
def duas_vezes():
    repositorio, publicados, pedido_id = cenario()
    comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    try:
        comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    except comandos.ErroDeComando as erro:
        assert erro.status == 409, f"status do erro: {erro.status} (esperado 409)."
    else:
        raise AssertionError("o segundo cancelamento foi aceito; ele deveria ser rejeitado.")
    assert len(publicados) == 1, "o segundo cancelamento não pode publicar outro evento."


executar()
