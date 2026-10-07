![Mapa: projeções](tutorial/img/mapa-projecao.svg)

📍 **Você está aqui:** na mesma projeção, agora tratando o evento `PedidoCancelado`.

## O que deve acontecer

| Evento | Efeito no documento do pedido |
| --- | --- |
| `PedidoCancelado` de um pedido **conhecido** | `status` vira `"CANCELADO"` e ganha `cancelado_em` |
| `PedidoCancelado` de um pedido **desconhecido** | ignora (não cria documento a partir de um cancelamento) |

## 🐍 Python rápido

| Código | Significa |
| --- | --- |
| `chave in dicionario` | `True` se a chave existe no dicionário |
| `documento["status"] = "X"` | troca o valor de uma chave; as outras ficam como estavam |

## ✏️ Faça

Abaixo do marcador **Etapa 7**, escreva o `if` e complete os `___`:

```python
    if evento["tipo"] == "PedidoCancelado" and dados["pedido_id"] in modelo.pedidos:
        documento = modelo.pedidos[dados["pedido_id"]]
        documento["status"] = ___
        documento["cancelado_em"] = ___
```

> Dica: o evento traz `dados["cancelado_em"]` (veja o `publicar` que você
> escreveu na Etapa 5).

**Salve** (`Ctrl+S`).

## 🧪 Teste: o pedido da `ana` de novo

```bash
curl -s localhost:8012/pedidos/$(cut -s -d'"' -f4 /tmp/pedido-ana.json) -w '← HTTP %{http_code}\n'
```

Agora deve vir `"status": "CANCELADO"`. Você não mexeu em nenhum dado: só ensinou
a projeção a **reinterpretar o mesmo histórico de eventos**.

## Clique em Verificar ✔
