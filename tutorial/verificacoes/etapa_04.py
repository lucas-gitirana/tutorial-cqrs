"""Etapa 4: CancelarPedido, passo 1 (validar). Testado sem subir containers."""
from verificador import executar, importar, verificacao

comandos = importar("servicos/pedidos-comando", "comandos")


class RepositorioFalso:
    """Faz o papel do SQLite, em memória, para testar o comando sem containers."""

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


@verificacao("pedido inexistente: lança ErroDeComando com status 404")
def inexistente():
    repositorio, publicados, _ = cenario()
    try:
        comandos.cancelar_pedido(repositorio, publicados.append, "nao-existe")
    except comandos.ErroDeComando as erro:
        assert erro.status == 404, f"status do erro: {erro.status} (esperado 404)."
    else:
        raise AssertionError("nenhum erro foi lançado. Escreva o 'if pedido is None: raise ...' no PASSO 1.")
    assert not publicados, "nenhum evento deveria ser publicado quando o comando é rejeitado."


@verificacao("pedido já CANCELADO: lança ErroDeComando com status 409")
def ja_cancelado():
    repositorio, publicados, pedido_id = cenario()
    repositorio.pedidos[pedido_id]["status"] = "CANCELADO"
    try:
        comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    except comandos.ErroDeComando as erro:
        assert erro.status == 409, f"status do erro: {erro.status} (esperado 409)."
    else:
        raise AssertionError(
            "o pedido já estava cancelado e nenhum erro foi lançado. Complete o segundo 'if' do PASSO 1."
        )
    assert not publicados, "nenhum evento deveria ser publicado quando o comando é rejeitado."


executar()
