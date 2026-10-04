# Etapa 3 — Construindo o modelo de leitura

**Objetivo:** implementar a projeção que mantém os **detalhes de cada pedido**
prontos para consulta.

Uma **projeção** é uma função que recebe um evento e atualiza o modelo de
leitura. Aqui, o modelo de leitura é um dicionário em memória:
`modelo.pedidos[pedido_id] -> documento`.

O arquivo `servicos/pedidos-consulta/projecoes.py` foi aberto ao lado.
Compare com a projeção de exemplo `projetar_resumo_por_cliente`, logo acima.

## O que implementar em `projetar_pedido`

**Ao receber `PedidoCriado`**, guarde em `modelo.pedidos[dados["pedido_id"]]`
um documento **pronto para exibição**:

```python
{
    "pedido_id": ...,
    "cliente": ...,
    "status": "CRIADO",
    "itens": ...,
    "quantidade_itens": ...,  # soma das quantidades de todos os itens
    "total": ...,
    "criado_em": ...,
}
```

**Ao receber `PedidoCancelado`**, se o pedido existir em `modelo.pedidos`,
mude `status` para `"CANCELADO"` e grave `cancelado_em`. Se não existir,
ignore o evento.

Repare que `quantidade_itens` é calculado **uma vez, na escrita da projeção**,
e não a cada consulta. No modelo de escrita (SQLite), o mesmo dado exigiria
um `JOIN` com `SUM` em toda leitura.

## Teste no serviço

```bash
docker compose restart pedidos-consulta && sleep 3
docker compose logs pedidos-consulta --tail 15
```

Nos logs, o serviço reaplica **todos os eventos desde o início** do stream.
Como o modelo de leitura é só uma projeção dos eventos, dá para apagá-lo e
reconstruí-lo a qualquer momento. Por isso o pedido que você criou na Etapa 1
agora aparece:

```bash
PRIMEIRO_PEDIDO=$(python3 -c 'import json; print(json.load(open("/tmp/primeiro-pedido.json"))["pedido_id"])')
curl -s -w '\n' localhost:8012/pedidos/$PRIMEIRO_PEDIDO
```

Clique em **Verificar**. Esta verificação testa `projecoes.py` diretamente.
