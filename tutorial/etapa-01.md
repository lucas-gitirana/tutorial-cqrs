# Etapa 1 — Conhecendo o ambiente

**Objetivo:** ver os dois lados do CQRS rodando e criar o primeiro pedido.

## 1. Confira os containers

```bash
docker compose ps
```

Você deve ver três serviços com estado `running`: `redis`, `pedidos-comando`
e `pedidos-consulta`.

## 2. Envie um comando: criar um pedido

O lado de **comando** (porta 8011) só recebe intenções de mudança:

```bash
curl -s -w '\n' -X POST localhost:8011/pedidos \
  -H 'Content-Type: application/json' \
  -d '{"cliente": "ana", "itens": [{"produto": "caneca", "quantidade": 2, "preco": 25.0}, {"produto": "camiseta", "quantidade": 1, "preco": 59.9}]}' \
  | tee /tmp/primeiro-pedido.json
```

A resposta traz **apenas o id** do pedido. Comandos não devolvem dados para
exibição. O id também foi salvo em `/tmp/primeiro-pedido.json` para usarmos
depois.

## 3. Tente consultar no lado de comando

```bash
curl -s -w '\n' localhost:8011/pedidos
```

O lado de comando recusa a consulta com HTTP 405 e indica o serviço certo.

## 4. Consulte no lado de consulta

O `pedidos-consulta` (porta 8012) já tem uma projeção pronta: o **resumo por
cliente**. Veja como ela foi feita em `servicos/pedidos-consulta/projecoes.py`
(função `projetar_resumo_por_cliente`).

```bash
curl -s -w '\n' localhost:8012/clientes/ana/resumo
```

> Recebeu 404? Espere 2 segundos e tente de novo. Na Etapa 4 você vai entender por quê.

Agora tente ver os detalhes do pedido que você acabou de criar:

```bash
PRIMEIRO_PEDIDO=$(python3 -c 'import json; print(json.load(open("/tmp/primeiro-pedido.json"))["pedido_id"])')
curl -s -w '\n' localhost:8012/pedidos/$PRIMEIRO_PEDIDO
```

Ele ainda **não existe** no modelo de leitura (HTTP 404), porque a projeção dos
detalhes do pedido é a sua tarefa da Etapa 3.

## 5. Espie os eventos

Os eventos ficam guardados em um *stream* do Redis, um log que só cresce:

```bash
docker compose exec redis redis-cli XRANGE pedidos.eventos - +
```

Clique em **Verificar** para concluir a etapa.
