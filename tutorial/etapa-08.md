![Mapa: visão geral](tutorial/img/mapa-geral.svg)

📍 **Você está aqui:** o mapa inteiro, de ponta a ponta. Repare no **tempo** que
um evento leva para atravessá-lo.

O `pedidos-consulta` foi configurado para aplicar cada evento **2 segundos
depois** (`ATRASO_PROJECAO_SEGUNDOS`, no `docker-compose.yml` aberto ao lado),
como uma réplica de leitura sobrecarregada.

## 🧪 Crie um pedido e consulte imediatamente

**`POST http://localhost:8011/pedidos`** e logo depois **`GET http://localhost:8012/pedidos/<id>`**

```json
{ "cliente": "carla", "itens": [{ "produto": "mochila", "quantidade": 1, "preco": 150.0 }] }
```

```bash
curl -s -X POST localhost:8011/pedidos -H 'Content-Type: application/json' \
  -d '{"cliente": "carla", "itens": [{"produto": "mochila", "quantidade": 1, "preco": 150.0}]}' \
  | tee /tmp/pedido-carla.json
ID=$(cut -s -d'"' -f4 /tmp/pedido-carla.json)
echo "--- consulta IMEDIATA:";  curl -s localhost:8012/pedidos/$ID -w '← HTTP %{http_code}\n'
sleep 3
echo "--- consulta 3s DEPOIS:"; curl -s localhost:8012/pedidos/$ID -w '← HTTP %{http_code}\n'
```

## O que aconteceu

```text
 t = 0s   POST  → gravado no SQLite ✔   evento no Redis ✔
 t = 0s   GET   → 404   a projeção ainda não aplicou o evento
 t = 2s           a projeção aplica o PedidoCriado
 t = 3s   GET   → 200 ✔
```

Isso é **consistência eventual**: o lado de leitura sempre "chega lá", mas **não
no mesmo instante**. É o principal preço do CQRS.

## Como o cliente lida com o atraso?

| Abordagem | Como funciona |
| --- | --- |
| **Atualização otimista** | a tela já mostra o resultado esperado e desfaz se o comando falhar |
| **Polling** | depois do comando, consulta de tempos em tempos até ver a mudança |
| **Publish-subscribe** | o cliente é avisado quando a leitura foi atualizada |

## Clique em Verificar ✔

A verificação usa **polling**: cria um pedido, consulta a cada 0,5 s até ele
aparecer, cancela e espera o cancelamento chegar ao lado de leitura.
