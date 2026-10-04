# Etapa 5 — Um novo modelo de leitura

**Objetivo:** criar uma consulta nova, **"produtos mais vendidos"**, sem
alterar nenhuma linha do lado de comando.

O time de marketing quer um ranking de produtos. Sem CQRS, isso seria uma
consulta pesada no banco transacional (`JOIN` + `GROUP BY` + `ORDER BY`),
competindo com as escritas. Com CQRS, basta uma nova projeção.

## O que implementar em `projetar_vendas_por_produto`

O arquivo `servicos/pedidos-consulta/projecoes.py` foi aberto na função.
Atualize o dicionário `modelo.vendas_por_produto` (`produto -> quantidade`):

- `PedidoCriado`: **some** a `quantidade` de cada item ao produto correspondente;
- `PedidoCancelado`: **subtraia** a `quantidade` de cada item;
- outros tipos de evento: ignore.

A rota `GET /produtos/mais-vendidos` já existe e ordena esse dicionário
(veja `ModeloDeLeitura.mais_vendidos`).

## Teste no serviço

```bash
docker compose restart pedidos-consulta && sleep 3
curl -s -w '\n' localhost:8012/produtos/mais-vendidos
```

O ranking já inclui os pedidos das etapas anteriores, **criados antes de esta
projeção existir**. Ao reiniciar, o serviço reprocessou o histórico de eventos
e montou o novo modelo do zero. Esse é um dos maiores benefícios de construir
consultas a partir de eventos.

Clique em **Verificar**.
