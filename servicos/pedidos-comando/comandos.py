"""Lado de COMANDO (escrita) do serviço de pedidos.

Um comando expressa a intenção de MUDAR o estado do sistema. Todo comando:

  1. valida as regras de negócio;
  2. grava a mudança no modelo de escrita (aqui, um banco SQLite normalizado);
  3. publica um evento de domínio contando o que aconteceu.

Comandos não devolvem dados para exibição — no máximo o id do que foi criado.
Quem quer CONSULTAR pedidos usa outro serviço: o ``pedidos-consulta``.

Este módulo não conhece Flask nem Redis: recebe o repositório e a função
``publicar`` por parâmetro. Assim ele pode ser testado sem subir nada.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Callable

Publicar = Callable[[dict], object]


class ErroDeComando(Exception):
    """Regra de negócio violada. ``status`` é o código HTTP devolvido ao cliente."""

    def __init__(self, mensagem: str, status: int = 400) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def criar_pedido(repositorio, publicar: Publicar, dados: dict) -> str:
    """Comando CriarPedido. Exemplo completo — use-o como referência nas Etapas 4 e 5."""
    cliente = str(dados.get("cliente") or "").strip()
    itens = dados.get("itens") or []

    # 1. Validar regras de negócio
    if not cliente:
        raise ErroDeComando("O campo 'cliente' é obrigatório.")
    if not itens:
        raise ErroDeComando("O pedido precisa ter ao menos um item.")
    for item in itens:
        if not item.get("produto") or item.get("quantidade", 0) <= 0 or item.get("preco", 0) <= 0:
            raise ErroDeComando("Cada item precisa de 'produto', 'quantidade' > 0 e 'preco' > 0.")

    pedido_id = uuid.uuid4().hex[:8]
    total = round(sum(item["quantidade"] * item["preco"] for item in itens), 2)
    criado_em = agora()

    # 2. Gravar no modelo de escrita
    repositorio.inserir_pedido(pedido_id, cliente, itens, criado_em)

    # 3. Publicar o evento de domínio (no passado: algo que JÁ aconteceu)
    publicar({
        "tipo": "PedidoCriado",
        "dados": {
            "pedido_id": pedido_id,
            "cliente": cliente,
            "itens": itens,
            "total": total,
            "criado_em": criado_em,
        },
    })
    return pedido_id


def cancelar_pedido(repositorio, publicar: Publicar, pedido_id: str) -> None:
    """Comando CancelarPedido. Você vai completá-lo nas Etapas 4 e 5."""
    # Busca o pedido no modelo de escrita. Devolve None se ele não existir, ou um dict:
    #   {"id": "a1b2c3d4", "cliente": "ana", "status": "CRIADO", "itens": [...], "total": 109.9}
    pedido = repositorio.obter_pedido(pedido_id)

    # ═══ PASSO 1 · VALIDAR (Etapa 4) ═══════════════════════════════════════
    # ✏️  Escreva aqui os dois `if` que rejeitam o comando (404 e 409).
    if pedido is None:
        raise ErroDeComando("Pedido não encontrado.", status=404)

    if pedido["status"] == "CANCELADO":
        raise ErroDeComando("Pedido já está cancelado.", status=409)



    # ═══ PASSO 2 · GRAVAR (Etapa 5) ════════════════════════════════════════
    # ✏️  Escreva aqui a linha que muda o status do pedido para "CANCELADO".
    repositorio.atualizar_status(pedido_id, "CANCELADO")



    # ═══ PASSO 3 · PUBLICAR O EVENTO (Etapa 5) ═════════════════════════════
    # ✏️  Escreva aqui a chamada publicar({...}) com o evento "PedidoCancelado".
    publicar({
        "tipo": "PedidoCancelado",
        "dados": {
            "pedido_id": pedido_id,
            "cliente": pedido["cliente"],
            "itens": pedido["itens"],
            "total": pedido["total"],
            "cancelado_em": agora(),
        },
    })

