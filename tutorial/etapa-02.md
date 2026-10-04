# Etapa 2 — Implementando um comando

**Objetivo:** implementar o comando **CancelarPedido** no lado de escrita.

O arquivo `servicos/pedidos-comando/comandos.py` foi aberto ao lado. Use a
função `criar_pedido`, logo acima, como modelo. Todo comando segue três passos:

1. **validar** as regras de negócio;
2. **gravar** a mudança no modelo de escrita;
3. **publicar** um evento de domínio, com o nome no passado: algo que *já aconteceu*.

## O que implementar em `cancelar_pedido`

| Situação | O que fazer |
| --- | --- |
| `repositorio.obter_pedido(pedido_id)` devolve `None` | `raise ErroDeComando("...", status=404)` |
| o pedido já está com status `"CANCELADO"` | `raise ErroDeComando("...", status=409)` |
| caso contrário | `repositorio.atualizar_status(pedido_id, "CANCELADO")` e publicar o evento |

O evento deve ter este formato:

```python
{
    "tipo": "PedidoCancelado",
    "dados": {
        "pedido_id": pedido_id,
        "cliente": pedido["cliente"],
        "itens": pedido["itens"],
        "total": pedido["total"],
        "cancelado_em": agora(),
    },
}
```

> **Por que repetir cliente, itens e total no evento?** O lado de consulta só
> conhece o mundo pelos eventos. Se o evento trouxer tudo o que as projeções
> precisam, nenhuma delas tem que perguntar nada ao lado de comando. Isso
> mantém os dois lados desacoplados.

## Teste no serviço

O código é montado como volume no container, então basta reiniciar o serviço:

```bash
docker compose restart pedidos-comando && sleep 2
```

Crie um pedido e cancele-o:

```bash
PEDIDO=$(curl -s -w '\n' -X POST localhost:8011/pedidos -H 'Content-Type: application/json' \
  -d '{"cliente": "bruno", "itens": [{"produto": "livro", "quantidade": 1, "preco": 80.0}]}' \
  | python3 -c 'import sys, json; print(json.load(sys.stdin)["pedido_id"])')
echo "Pedido criado: $PEDIDO"
curl -s -w '\n' -X POST localhost:8011/pedidos/$PEDIDO/cancelar
```

Rode o cancelamento de novo: a resposta agora deve ser HTTP 409.

```bash
curl -s -w '\n' -X POST localhost:8011/pedidos/$PEDIDO/cancelar
```

Clique em **Verificar**. Esta verificação testa `comandos.py` diretamente,
sem precisar dos containers.
