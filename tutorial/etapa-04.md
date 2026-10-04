# Etapa 4 — Ponta a ponta e consistência eventual

**Objetivo:** ver o fluxo completo e entender o **atraso de replicação**
(*replication lag*), o principal efeito colateral do CQRS.

## 1. Crie um pedido e consulte imediatamente

O `pedidos-consulta` foi configurado com um atraso artificial de 2 segundos
para aplicar eventos (`ATRASO_PROJECAO_SEGUNDOS` no `docker-compose.yml`), como
uma réplica de leitura sobrecarregada.

```bash
PEDIDO=$(curl -s -w '\n' -X POST localhost:8011/pedidos -H 'Content-Type: application/json' \
  -d '{"cliente": "carla", "itens": [{"produto": "mochila", "quantidade": 1, "preco": 150.0}]}' \
  | python3 -c 'import sys, json; print(json.load(sys.stdin)["pedido_id"])')
echo "--- consulta imediata:"; curl -s -w '\n' localhost:8012/pedidos/$PEDIDO
sleep 3
echo "--- consulta 3s depois:"; curl -s -w '\n' localhost:8012/pedidos/$PEDIDO
```

A primeira consulta devolve 404: o comando **já foi gravado**, mas o modelo de
leitura **ainda não foi atualizado**. A segunda encontra o pedido. Isso é
**consistência eventual**: o lado de consulta sempre "chega lá", mas não no
mesmo instante.

## 2. Cancele e acompanhe

```bash
curl -s -w '\n' -X POST localhost:8011/pedidos/$PEDIDO/cancelar
sleep 3
curl -s -w '\n' localhost:8012/pedidos/$PEDIDO
curl -s -w '\n' localhost:8012/clientes/carla/resumo
```

## Como lidar com o atraso?

Bruce e Pereira (2019) descrevem três abordagens para o cliente:

| Abordagem | Como funciona |
| --- | --- |
| **Atualização otimista** | a interface já mostra o resultado esperado do comando e desfaz se ele falhar |
| **Polling** | após o comando, o cliente consulta periodicamente até ver a mudança |
| **Publish-subscribe** | o cliente é avisado por um evento quando a consulta já foi atualizada |

> A verificação desta etapa usa **polling**: cria um pedido, consulta o
> `pedidos-consulta` a cada 0,5 s até o pedido aparecer e depois cancela.

Clique em **Verificar**. Os dois serviços precisam estar rodando com o código
das Etapas 2 e 3.
