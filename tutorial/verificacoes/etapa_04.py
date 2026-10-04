"""Etapa 4: fluxo ponta a ponta com os containers rodando."""
import uuid

from verificador import aguardar, executar, http, verificacao

COMANDO = "http://localhost:8011"
CONSULTA = "http://localhost:8012"
CLIENTE = f"verificacao-{uuid.uuid4().hex[:6]}"
estado = {}


@verificacao("POST /pedidos no pedidos-comando devolve 201 com o pedido_id")
def cria():
    status, corpo = http("POST", f"{COMANDO}/pedidos", {
        "cliente": CLIENTE, "itens": [{"produto": "caderno", "quantidade": 4, "preco": 12.5}],
    })
    assert status == 201, f"esperado HTTP 201, veio {status}: {corpo}"
    estado["id"] = corpo["pedido_id"]


@verificacao("o pedido aparece no pedidos-consulta (consistência eventual: aguardando até 10s)")
def aparece():
    url = f"{CONSULTA}/pedidos/{estado['id']}"
    pronto = aguardar(lambda: http("GET", url)[0] == 200, segundos=10)
    assert pronto, (
        "o pedido não apareceu no modelo de leitura. Você reiniciou o pedidos-consulta depois da Etapa 3? "
        "Veja os logs: docker compose logs pedidos-consulta"
    )
    _, pedido = http("GET", url)
    assert pedido.get("status") == "CRIADO" and pedido.get("total") == 50.0, f"documento inesperado: {pedido}"


@verificacao("POST /pedidos/<id>/cancelar no pedidos-comando é aceito")
def cancela():
    status, corpo = http("POST", f"{COMANDO}/pedidos/{estado['id']}/cancelar")
    assert status == 200, (
        f"esperado HTTP 200, veio {status}: {corpo}. Você reiniciou o pedidos-comando depois da Etapa 2?"
    )


@verificacao("o cancelamento chega ao modelo de leitura (status CANCELADO)")
def cancelamento_projetado():
    url = f"{CONSULTA}/pedidos/{estado['id']}"
    pronto = aguardar(lambda: http("GET", url)[1].get("status") == "CANCELADO", segundos=10)
    assert pronto, "o status no pedidos-consulta não virou CANCELADO."


@verificacao("o resumo do cliente reflete criação e cancelamento (0 pedidos ativos, total 0)")
def resumo():
    status, corpo = http("GET", f"{CONSULTA}/clientes/{CLIENTE}/resumo")
    assert status == 200, f"HTTP {status}: {corpo}"
    assert corpo.get("pedidos_ativos") == 0 and corpo.get("total_gasto") == 0, f"resumo inesperado: {corpo}"


executar(parar_na_primeira_falha=True)
