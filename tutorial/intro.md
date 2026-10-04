# Padrão CQRS na prática

**Tempo estimado:** 35 minutos · **Linguagem:** Python (Flask) · **Infra:** Docker Compose + Redis

## O problema

Em um serviço "tradicional", o mesmo modelo de dados atende escrita e leitura.
Só que escrever e ler têm necessidades diferentes:

- a **escrita** precisa garantir regras de negócio e integridade (tabelas
  normalizadas, transações);
- a **leitura** quer respostas rápidas e no formato da tela (dados
  desnormalizados, totais já calculados, sem JOINs).

## A ideia do CQRS

**CQRS** (*Command Query Responsibility Segregation*) divide as operações em
dois grupos:

- **comandos**: mudam dados (criar pedido, cancelar pedido);
- **consultas** (*queries*): só leem dados.

Cada grupo tem o **seu próprio modelo**, e eles podem viver em serviços, bancos
e até tecnologias diferentes (Newman, 2021). O lado de comando publica
**eventos** ("PedidoCriado", "PedidoCancelado"). O lado de consulta escuta esses
eventos e mantém **projeções**, que são visões já prontas para leitura.

```text
                    POST /pedidos                          GET /pedidos/<id>
                    POST /pedidos/<id>/cancelar            GET /clientes/<c>/resumo
                          │                                        ▲
                          ▼                                        │
                ┌───────────────────┐                    ┌───────────────────┐
  cliente ───▶  │  pedidos-comando  │                    │  pedidos-consulta │  ◀─── cliente
                │   (porta 8011)    │                    │   (porta 8012)    │
                └─────────┬─────────┘                    └─────────▲─────────┘
                          │ grava                                  │ projeções
                          ▼                                        │ (memória)
                ┌───────────────────┐   publica    ┌───────────────┴───┐
                │  SQLite           │   eventos    │  Redis Stream     │
                │  (normalizado)    │ ───────────▶ │  pedidos.eventos  │
                └───────────────────┘              └───────────────────┘
```

## O que você vai fazer

1. Conhecer o ambiente e criar o primeiro pedido.
2. Implementar o comando **CancelarPedido**.
3. Implementar a **projeção** que monta os detalhes do pedido para leitura.
4. Testar o fluxo de ponta a ponta e observar a **consistência eventual**.
5. Criar um **novo modelo de leitura** sem tocar no lado de comando.

## Como funciona este tutorial

- Blocos de comando têm um botão **▶ Executar**, que roda o comando no terminal integrado.
- Etapas com avaliação têm o botão **Verificar**. Ele roda um script que confere
  o seu código e/ou os serviços em execução. Leia a saída quando algo falhar:
  ela diz o que está faltando.
- Os arquivos que você vai editar abrem sozinhos, já na linha certa. Procure os
  comentários `TODO`.

## Preparando o ambiente

Ao abrir esta introdução, o terminal já começou a subir os containers
(`docker compose up -d --build --wait`). A primeira execução baixa as imagens e pode
levar 1–2 minutos. Se precisar rodar de novo:

```bash
docker compose up -d --build --wait
```

> Pré-requisitos: Docker com Docker Compose e Python 3 (o Python é usado
> pelas verificações). No GitHub Codespaces, tudo já vem instalado.
