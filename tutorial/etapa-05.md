![Mapa: lado de escrita](tutorial/img/mapa-comando.svg)

📍 **Você está aqui:** terminando o **CancelarPedido**: gravar no SQLite e
publicar o evento no Redis (as setas **grava** e **evento** do mapa).

## ✏️ Faça: PASSO 2 · GRAVAR

Abaixo do marcador **PASSO 2**, escreva uma linha:

```python
    repositorio.atualizar_status(pedido_id, "CANCELADO")
```

## ✏️ Faça: PASSO 3 · PUBLICAR

Um **evento** conta algo que **já aconteceu**, por isso o nome fica no passado:
`PedidoCancelado`. Abaixo do marcador **PASSO 3**, escreva (é quase igual ao
`publicar` de `criar_pedido`, logo acima):

```python
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
```

> **Por que mandar cliente, itens e total no evento?** O lado de consulta só
> conhece o mundo pelos eventos. Se o evento já traz tudo, ele nunca precisa
> perguntar nada ao lado de comando. Os dois lados ficam **independentes**.

**Salve** o arquivo (`Ctrl+S`).

## 🧪 Teste: cancele o pedido da `ana`

**`POST http://localhost:8011/pedidos/<id do pedido da ana>/cancelar`**

```bash
curl -s -X POST localhost:8011/pedidos/$(cut -s -d'"' -f4 /tmp/pedido-ana.json)/cancelar -w '← HTTP %{http_code}\n'
```

> `$(cut ...)` lê o id que o `tee` guardou na Etapa 2.

Esperado: `"status": "CANCELADO"` e `← HTTP 200`. Agora **rode o mesmo comando
de novo**: deve vir `← HTTP 409`, a validação da Etapa 4 funcionando.

## Clique em Verificar ✔

> Deu erro de conexão? Pode ser um erro de digitação no Python. Veja com
> `docker compose logs pedidos-comando --tail 20`.
