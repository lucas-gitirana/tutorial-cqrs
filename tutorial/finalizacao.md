## Você montou o mapa inteiro 🎉

![Mapa do CQRS](tutorial/img/mapa-geral.svg)

| Peça do mapa | O que você fez |
| --- | --- |
| **Comando** | `CancelarPedido`: validar → gravar → publicar |
| **Evento** | `PedidoCancelado`, com tudo o que a leitura precisa |
| **Projeção** | detalhes do pedido, a partir de `PedidoCriado` e `PedidoCancelado` |
| **Nova tela** | ranking de produtos, sem tocar no lado de escrita |
| **Consistência eventual** | viu a leitura "chegar depois" e como lidar com isso |

## Vale a pena usar CQRS?

| ✅ Ganha | ⚠️ Paga |
| --- | --- |
| consultas rápidas, no formato da tela | mais peças para operar (broker, dois serviços) |
| leitura e escrita escalam separadas | **consistência eventual** |
| telas novas sem mexer na escrita | mais código para escrever e testar |

Use CQRS quando ele resolve um problema real: leituras muito mais frequentes que
escritas, ou muitas "telas" diferentes dos mesmos dados. Em um CRUD simples, ele
só adiciona complexidade.

## Para pensar

1. Se o `pedidos-consulta` ficar 10 minutos fora do ar, o que acontece quando ele voltar?
2. O comando grava no SQLite e **depois** publica no Redis. E se o serviço cair
   entre as duas coisas? *(Pesquise: padrão Transactional Outbox.)*

## Limpando o ambiente

```bash
docker compose down -v
```

A solução completa está na branch `solucao` deste repositório.

## Formulários de pós-teste e SUS:
Após enviar o seu resultado ao professor, responda a esses dois formulários abaixo:
- [Formulário de Pós-teste][]
- [Formulário SUS][]

[Formulário de Pós-teste]: https://docs.google.com/forms/d/e/1FAIpQLSePetSPhG04Q4adG9hnTLeqpGcLQ2MIvFjHkeBsJqr3P4wnMg/viewform?usp=sharing&ouid=103537969988084746732
[Formulário SUS]: https://docs.google.com/forms/d/e/1FAIpQLSf_2BOW8VR3QeK4oJAORaNrIfw803TcrqspXP8xAwcXXbuuPQ/viewform?usp=sharing&ouid=103537969988084746732
