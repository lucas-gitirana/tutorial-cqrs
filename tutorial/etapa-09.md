![Mapa: projeções](tutorial/img/mapa-projecao.svg)

📍 **Você está aqui:** de volta às projeções. Você vai criar uma **tela nova**
sem tocar em **nenhuma linha** do lado de escrita.

## O pedido do marketing

> "Queremos um ranking dos **produtos mais vendidos**."

Sem CQRS, seria uma consulta pesada no banco de escrita (`JOIN` + `GROUP BY` +
`ORDER BY`), disputando espaço com as gravações. Com CQRS, é só **mais uma
projeção** sobre os mesmos eventos.

## O que deve acontecer

`modelo.vendas_por_produto` é um dicionário `produto → quantidade vendida`:

| Evento | Efeito |
| --- | --- |
| `PedidoCriado` com 2 canecas | `{"caneca": 2}` |
| `PedidoCriado` com 3 canecas | `{"caneca": 5}` |
| `PedidoCancelado` do 1º pedido | `{"caneca": 3}` |

## 🐍 Python rápido

| Código | Significa |
| --- | --- |
| `for item in dados["itens"]:` | repete o bloco abaixo para cada item do pedido |
| `dicionario.get(produto, 0)` | valor da chave, ou `0` se ela ainda não existe |

## ✏️ Faça

Abaixo do marcador **Etapa 9**, cole o código abaixo e complete o `___` com `modelo.vendas_por_produto.get(produto, 0) - item["quantidade"]`, que faz a mesma coisa que o `if` de cima, mas **subtraindo**:

```python
    if evento["tipo"] == "PedidoCriado":
        for item in dados["itens"]:
            produto = item["produto"]
            modelo.vendas_por_produto[produto] = modelo.vendas_por_produto.get(produto, 0) + item["quantidade"]

    if evento["tipo"] == "PedidoCancelado":
        for item in dados["itens"]:
            produto = item["produto"]
            modelo.vendas_por_produto[produto] = ___
```

**Salve** (`Ctrl+S`).

## 🧪 Teste

**`GET http://localhost:8012/produtos/mais-vendidos`**

```bash
curl -s localhost:8012/produtos/mais-vendidos -w '← HTTP %{http_code}\n'
```

O ranking **já inclui os pedidos das etapas anteriores**, criados antes desta
projeção existir. Ao reiniciar, o serviço reprojetou o histórico inteiro e montou
a tela nova do zero.

## Clique em Verificar ✔
