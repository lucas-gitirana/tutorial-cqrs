![Mapa: lado de leitura](tutorial/img/mapa-consulta.svg)

📍 **Você está aqui:** o evento atravessou o Redis e chegou ao lado de **leitura**.

## 1. Tente ler no lado errado

**`GET http://localhost:8011/pedidos`** (porta do **comando**)

```bash
curl -s localhost:8011/pedidos -w '← HTTP %{http_code}\n'
```

**405 Method Not Allowed**: o lado de comando **não responde consultas**.
Cada lado tem uma única responsabilidade.

## 2. Leia no lado certo

**`GET http://localhost:8012/clientes/ana/resumo`** (porta da **consulta**)

```bash
curl -s localhost:8012/clientes/ana/resumo -w '← HTTP %{http_code}\n'
```

Resposta esperada:

```json
{ "cliente": "ana", "pedidos_ativos": 1, "total_gasto": 109.9 }
```

Repare: o `total_gasto` **já vem calculado**. Ninguém somou nada na hora da
consulta. Quem preparou esse resumo foi uma **projeção** (você vai entender
isso na Etapa 6).

> Veio 404? Espere 2 segundos e rode de novo. Na Etapa 8 você descobre por quê.

## 3. Espie o evento no Redis

```bash
docker compose exec redis redis-cli XRANGE pedidos.eventos - +
```

Esse é o **stream** `pedidos.eventos`: a lista de tudo o que já aconteceu, em
ordem. Você deve ver o seu `PedidoCriado` com os dados da `ana`.

✅ Você já percorreu o mapa inteiro: **comando → evento → consulta**. Agora
vamos construir cada pedaço. Clique em **Avançar**.
