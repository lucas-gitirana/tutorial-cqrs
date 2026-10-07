"""Lado de CONSULTA (leitura): projeções que constroem o modelo de leitura.

Uma *projeção* escuta os eventos publicados pelo lado de comando e mantém
uma visão dos dados já no formato em que as consultas vão precisar
(desnormalizada, pré-calculada). Consultar vira um simples "pegar no
dicionário" — sem JOINs, sem somas na hora da leitura.

Cada projeção é independente: recebe o modelo e um evento, e atualiza a sua
parte do modelo. Este módulo não conhece Flask nem Redis.
"""
from __future__ import annotations


class ModeloDeLeitura:
    """Modelo de leitura em memória. Pode ser jogado fora e reconstruído a
    qualquer momento reaplicando todos os eventos do stream."""

    def __init__(self) -> None:
        # pedido_id -> documento pronto para exibição (Etapas 6 e 7)
        self.pedidos: dict[str, dict] = {}
        # cliente -> {"cliente", "pedidos_ativos", "total_gasto"}
        self.resumo_por_cliente: dict[str, dict] = {}
        # produto -> quantidade vendida, desconsiderando cancelamentos (Etapa 9)
        self.vendas_por_produto: dict[str, int] = {}

    def mais_vendidos(self, limite: int = 5) -> list[dict]:
        ranking = sorted(self.vendas_por_produto.items(), key=lambda par: (-par[1], par[0]))
        return [{"produto": p, "quantidade": q} for p, q in ranking if q > 0][:limite]


# ---------------------------------------------------------------------------
# Projeção de EXEMPLO (já pronta): resumo de gastos por cliente
# ---------------------------------------------------------------------------
def projetar_resumo_por_cliente(modelo: ModeloDeLeitura, evento: dict) -> None:
    dados = evento["dados"]
    if evento["tipo"] not in ("PedidoCriado", "PedidoCancelado"):
        return

    resumo = modelo.resumo_por_cliente.setdefault(
        dados["cliente"], {"cliente": dados["cliente"], "pedidos_ativos": 0, "total_gasto": 0.0}
    )
    if evento["tipo"] == "PedidoCriado":
        resumo["pedidos_ativos"] += 1
        resumo["total_gasto"] = round(resumo["total_gasto"] + dados["total"], 2)
    else:  # PedidoCancelado
        resumo["pedidos_ativos"] -= 1
        resumo["total_gasto"] = round(resumo["total_gasto"] - dados["total"], 2)


# ---------------------------------------------------------------------------
# Etapas 6 e 7: projeção dos DETALHES de cada pedido
# ---------------------------------------------------------------------------
def projetar_pedido(modelo: ModeloDeLeitura, evento: dict) -> None:
    dados = evento["dados"]

    # ═══ Etapa 6 · ao receber "PedidoCriado" ═══════════════════════════════
    # ✏️  Escreva aqui o `if` que guarda o documento em modelo.pedidos.
    if evento["tipo"] == "PedidoCriado":
        modelo.pedidos[dados["pedido_id"]] = {
            "pedido_id": dados["pedido_id"],
            "cliente": dados["cliente"],
            "status": "CRIADO",
            "itens": dados["itens"],
            "quantidade_itens": sum(item["quantidade"] for item in dados["itens"]),
            "total": dados["total"],
            "criado_em": dados["criado_em"],
        }



    # ═══ Etapa 7 · ao receber "PedidoCancelado" ════════════════════════════
    # ✏️  Escreva aqui o `if` que marca o documento como CANCELADO.
    if evento["tipo"] == "PedidoCancelado" and dados["pedido_id"] in modelo.pedidos:
        documento = modelo.pedidos[dados["pedido_id"]]
        documento["status"] = "CANCELADO"
        documento["cancelado_em"] = dados["cancelado_em"]



# ---------------------------------------------------------------------------
# Etapa 9: um NOVO modelo de leitura — produtos mais vendidos
# ---------------------------------------------------------------------------
def projetar_vendas_por_produto(modelo: ModeloDeLeitura, evento: dict) -> None:
    dados = evento["dados"]

    # ═══ Etapa 9 ═══════════════════════════════════════════════════════════
    # ✏️  Escreva aqui os dois `if` (PedidoCriado soma, PedidoCancelado subtrai).
    if evento["tipo"] == "PedidoCriado":
        for item in dados["itens"]:
            produto = item["produto"]
            modelo.vendas_por_produto[produto] = modelo.vendas_por_produto.get(produto, 0) + item["quantidade"]

    if evento["tipo"] == "PedidoCancelado":
        for item in dados["itens"]:
            produto = item["produto"]
            modelo.vendas_por_produto[produto] = modelo.vendas_por_produto.get(produto, 0) - item["quantidade"]



PROJECOES = (projetar_resumo_por_cliente, projetar_pedido, projetar_vendas_por_produto)


def aplicar_evento(modelo: ModeloDeLeitura, evento: dict) -> None:
    """Entrega o evento a todas as projeções."""
    for projecao in PROJECOES:
        projecao(modelo, evento)
