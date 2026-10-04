# Parabéns, você aplicou CQRS! 🎉

## O que você construiu

- Um lado de **comando** que valida, grava em um banco normalizado e publica eventos.
- Um lado de **consulta** com três projeções independentes, reconstruídas a
  partir do log de eventos.
- Uma consulta nova (ranking de produtos) criada **sem tocar** no lado de escrita.

## Benefícios e custos

| Benefícios | Custos |
| --- | --- |
| Consultas rápidas e no formato da tela | Mais peças para operar (broker, dois serviços) |
| Leitura e escrita escalam de forma independente | **Atraso de replicação**: consistência eventual |
| Novas consultas sem mexer na escrita | Mais código e mais cenários para testar |
| Melhor separação de responsabilidades | Complexidade arquitetural |

Use CQRS **quando ele resolve um problema real** (leituras muito diferentes
ou muito mais frequentes que as escritas, várias visões dos mesmos dados).
Em um CRUD simples, ele só adiciona complexidade (Nadareishvili *et al.*, 2016).

## Para refletir

1. O que aconteceria com o modelo de leitura se o `pedidos-consulta` ficasse
   fora do ar por 10 minutos e depois voltasse?
2. Neste tutorial, o comando grava no SQLite e **depois** publica no Redis. O
   que acontece se o serviço cair entre essas duas operações? *(Pesquise o
   padrão Transactional Outbox.)*
3. Em produção, quais tecnologias você usaria para o modelo de leitura?
   (ex.: Elasticsearch, MongoDB, Redis.)

## Limpando o ambiente

```bash
docker compose down -v
```

O código completo de referência está na branch `solucao` deste repositório.
