![Mapa: lado de escrita](tutorial/img/mapa-comando.svg)

📍 **Você está aqui:** lado de **escrita**. Você vai mandar o seu primeiro **comando**.

## 1. A requisição

Um comando é um **pedido de mudança**. Este cria um pedido para a cliente `ana`:

**`POST http://localhost:8011/pedidos`**

```json
{
  "cliente": "ana",
  "itens": [
    { "produto": "caneca",   "quantidade": 2, "preco": 25.0 },
    { "produto": "camiseta", "quantidade": 1, "preco": 59.9 }
  ]
}
```

## 2. Envie

```bash
curl -s -X POST localhost:8011/pedidos \
  -H 'Content-Type: application/json' \
  -d '{"cliente": "ana", "itens": [{"produto": "caneca", "quantidade": 2, "preco": 25.0}, {"produto": "camiseta", "quantidade": 1, "preco": 59.9}]}' \
  -w '← HTTP %{http_code}\n' | tee /tmp/pedido-ana.json
```

> O `curl` envia o JSON acima. O `tee` guarda a resposta em `/tmp/pedido-ana.json`
> para reaproveitarmos o id depois.

## 3. Olhe a resposta

```text
{"pedido_id": "a1b2c3d4"}
← HTTP 201
```

- **201 Created**: o pedido foi criado.
- Só veio o **id**. Comando **não devolve dados para exibição**: quem quer ler
  pedidos vai ao outro lado do mapa.

Por trás, o `pedidos-comando` fez três coisas: **validou** os dados, **gravou**
no SQLite e **publicou** o evento `PedidoCriado` no Redis.

## 4. Clique em Verificar ✔
