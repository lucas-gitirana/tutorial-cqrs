![Mapa: lado de escrita](tutorial/img/mapa-comando.svg)

📍 **Você está aqui:** dentro do `pedidos-comando`. Você vai escrever o comando
**CancelarPedido**, em duas etapas curtas.

Todo comando segue a mesma receita. Veja `criar_pedido`, no arquivo aberto ao lado:

| Passo | O que faz | Etapa |
| --- | --- | --- |
| 1. **Validar** | recusa o comando se ele quebra uma regra | **esta** |
| 2. **Gravar** | salva a mudança no modelo de escrita | 5 |
| 3. **Publicar** | avisa o mundo com um evento | 5 |

## 🐍 Python rápido: `raise`

`raise` **interrompe** a função na hora e lança um erro. Nada abaixo dele roda.

```python
if pedido is None:
    raise ErroDeComando("Pedido não encontrado.", status=404)
# se entrou no if, esta linha nunca é executada
```

O `app.py` captura o `ErroDeComando` e responde ao cliente com o `status` dele.

## Quais códigos HTTP usar?

| Situação | Código | Por quê |
| --- | --- | --- |
| o pedido não existe | **404** Not Found | o recurso pedido não foi encontrado |
| o pedido já está cancelado | **409** Conflict | a requisição é válida, mas **conflita com o estado atual** do pedido |

> Não é 400 (Bad Request), porque a requisição está bem formada. E não é 500,
> porque o servidor não falhou: foi uma regra de negócio que barrou.

## ✏️ Faça

Em `cancelar_pedido`, logo abaixo do marcador **PASSO 1 · VALIDAR**, cole o bloco de código abaixo e complete o primeiro `___` com `"CANCELADO"` e o segundo `___` com `409`:

```python
    if pedido is None:
        raise ErroDeComando("Pedido não encontrado.", status=404)

    if pedido["status"] == ___:
        raise ErroDeComando("Pedido já está cancelado.", status=___)
```

> Atenção à **indentação**: 4 espaços, alinhado com `pedido = ...`.

**Salve** o arquivo (`Ctrl+S`). O serviço recarrega sozinho.

## 🧪 Teste

Tente cancelar um pedido que não existe:

**`POST http://localhost:8011/pedidos/nao-existe/cancelar`**

```bash
curl -s -X POST localhost:8011/pedidos/nao-existe/cancelar -w '← HTTP %{http_code}\n'
```

Esperado: `{"erro": "Pedido não encontrado."}` e `← HTTP 404`.

## Clique em Verificar ✔
