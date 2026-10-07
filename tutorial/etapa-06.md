![Mapa: projeções](tutorial/img/mapa-projecao.svg)

📍 **Você está aqui:** dentro do `pedidos-consulta`, na seta **projeta**.

## O que é PROJETAR?

Pense em um **projetor de cinema**: o filme é sempre o mesmo, mas o que aparece
na tela depende de como você projeta.

- O **filme** é a lista de eventos no Redis: tudo o que aconteceu, em ordem.
- A **tela** é o modelo de leitura: os dados no formato que uma consulta precisa.
- **Projetar** é passar pelos eventos, um por um, e ir atualizando a tela.

Veja a projeção pronta `projetar_resumo_por_cliente` (no arquivo aberto ao lado)
transformando 3 eventos no resumo da `ana`:

| Evento recebido | Resumo da `ana` depois dele |
| --- | --- |
| *(nenhum)* | *(não existe)* |
| `PedidoCriado`, total 109.9 | `pedidos_ativos: 1, total_gasto: 109.9` |
| `PedidoCriado`, total 50.0 | `pedidos_ativos: 2, total_gasto: 159.9` |
| `PedidoCancelado`, total 50.0 | `pedidos_ativos: 1, total_gasto: 109.9` |

Uma projeção é só uma função: **recebe um evento e atualiza o modelo**. Os
mesmos eventos podem alimentar **várias** projeções, cada uma montando uma
"tela" diferente.

## Sua tarefa: a tela de detalhes do pedido

Em `projetar_pedido`, quando chegar um evento como este:

```json
{
  "tipo": "PedidoCriado",
  "dados": {
    "pedido_id": "a1b2c3d4",
    "cliente": "ana",
    "itens": [{ "produto": "caneca", "quantidade": 2, "preco": 25.0 }, "..."],
    "total": 109.9,
    "criado_em": "2026-10-05T14:00:00+00:00"
  }
}
```

guarde em `modelo.pedidos` um **documento pronto para exibição**.

## 🐍 Python rápido

| Código | Significa |
| --- | --- |
| `dados["cliente"]` | pega o valor da chave `"cliente"` do dicionário |
| `modelo.pedidos[chave] = {...}` | guarda um dicionário dentro de outro, na `chave` |
| `sum(item["quantidade"] for item in dados["itens"])` | soma a quantidade de todos os itens |

## ✏️ Faça

Abaixo do marcador **Etapa 6**, escreva o `if` e complete os `___`:

```python
    if evento["tipo"] == "PedidoCriado":
        modelo.pedidos[dados["pedido_id"]] = {
            "pedido_id": dados["pedido_id"],
            "cliente": dados["cliente"],
            "status": "CRIADO",
            "itens": ___,
            "quantidade_itens": sum(item["quantidade"] for item in dados["itens"]),
            "total": ___,
            "criado_em": ___,
        }
```

Repare: `quantidade_itens` é calculado **uma vez**, quando o evento chega, e não
a cada consulta. **Salve** (`Ctrl+S`).

## 🧪 Teste: veja o pedido da `ana`

Ao salvar, o `pedidos-consulta` reinicia e **reprojeta todos os eventos desde
o início**. Por isso o pedido da Etapa 2 aparece, mesmo tendo sido criado antes
desta projeção existir:

**`GET http://localhost:8012/pedidos/<id do pedido da ana>`**

```bash
curl -s localhost:8012/pedidos/$(cut -s -d'"' -f4 /tmp/pedido-ana.json) -w '← HTTP %{http_code}\n'
```

🤔 O `status` veio **`CRIADO`**, mas você cancelou esse pedido na Etapa 5!
A projeção ainda não sabe tratar `PedidoCancelado`. É a próxima etapa.

## Clique em Verificar ✔
