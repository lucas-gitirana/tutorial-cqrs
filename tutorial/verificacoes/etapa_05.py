"""Etapa 5: CancelarPedido, passos 2 e 3 (gravar e publicar)."""
from verificador import executar, http, importar, verificacao

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


COMANDO = "http://localhost:8011"


@verificacao("PASSO 2: o status do pedido vira CANCELADO no modelo de escrita")
def muda_status():
    repositorio, publicados, pedido_id = cenario()
    comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    assert repositorio.pedidos[pedido_id]["status"] == "CANCELADO", (
        "o status continua " + repr(repositorio.pedidos[pedido_id]["status"])
        + ". Escreva repositorio.atualizar_status(pedido_id, \"CANCELADO\") no PASSO 2."
    )


@verificacao("PASSO 3: publica um evento PedidoCancelado com pedido_id, cliente, itens, total e cancelado_em")
def publica_evento():
    repositorio, publicados, pedido_id = cenario()
    comandos.cancelar_pedido(repositorio, publicados.append, pedido_id)
    assert len(publicados) == 1, f"esperado 1 evento publicado, mas foram {len(publicados)}."
    evento = publicados[0]
    assert evento.get("tipo") == "PedidoCancelado", f"tipo do evento: {evento.get('tipo')!r} (esperado 'PedidoCancelado')."
    dados = evento.get("dados", {})
    for campo, esperado in (("pedido_id", pedido_id), ("cliente", "ana"), ("total", 50.0)):
        assert dados.get(campo) == esperado, f"dados['{campo}'] deveria ser {esperado!r}, veio {dados.get(campo)!r}."
    assert dados.get("itens") == [{"produto": "caneca", "quantidade": 2, "preco": 25.0}], (
        "dados['itens'] deveria trazer os itens do pedido (as projeções precisam deles)."
    )
    assert dados.get("cancelado_em"), "dados['cancelado_em'] está vazio. Use agora()."


@verificacao("cancelar duas vezes: a segunda é rejeitada (409) e não publica outro evento")
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


@verificacao("o serviço pedidos-comando em execução já usa o seu código (POST .../cancelar devolve 200)")
def servico_atualizado():
    status, corpo = http("POST", f"{COMANDO}/pedidos", {
        "cliente": "verificacao", "itens": [{"produto": "lápis", "quantidade": 1, "preco": 2.0}],
    })
    assert status == 201, f"falha ao criar pedido de teste: HTTP {status} {corpo}"
    status, corpo = http("POST", f"{COMANDO}/pedidos/{corpo['pedido_id']}/cancelar")
    assert status == 200, (
        f"esperado HTTP 200, veio {status}: {corpo}. O arquivo foi salvo? "
        "Veja os logs: docker compose logs pedidos-comando --tail 20"
    )


executar(parar_na_primeira_falha=True)
