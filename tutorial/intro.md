## O problema

Uma loja online **grava** um pedido de vez em quando, mas **lê** pedidos o tempo
todo: tela do cliente, painel do vendedor, relatórios...

Usar o mesmo modelo de dados para as duas coisas gera atrito:

| | Escrita | Leitura |
| --- | --- | --- |
| Quer... | regras de negócio e integridade | respostas rápidas, no formato da tela |
| Melhor formato | tabelas normalizadas, transações | dados prontos, totais já calculados |

## A ideia do CQRS

**CQRS** (*Command Query Responsibility Segregation*) separa o sistema em **dois
lados**, cada um com o **seu próprio modelo de dados**:

- **Comando** (*Command*): muda dados. Ex.: criar pedido, cancelar pedido.
- **Consulta** (*Query*): só lê dados. Ex.: ver um pedido, ver o resumo do cliente.

O lado de comando avisa o que aconteceu publicando **eventos**. O lado de
consulta escuta esses eventos e monta **projeções**: visões dos dados já
prontas para leitura.

Este é o mapa do sistema que você vai usar. Ele aparece em toda etapa,
destacando a parte em que você está:

![Mapa do CQRS](tutorial/img/mapa-geral.svg)

## As ferramentas

| Peça | O que é | Papel aqui |
| --- | --- | --- |
| **Docker Compose** | sobe vários containers com um único comando, a partir do `docker-compose.yml` | liga os 3 serviços do mapa |
| **Flask** | microframework web em Python | faz as APIs HTTP dos dois serviços |
| **SQLite** | banco relacional que vive em um único arquivo | modelo de **escrita** do `pedidos-comando` |
| **Redis** | banco em memória, muito rápido. Tem os *Streams*: listas de mensagens que só crescem, sempre em ordem | **barramento de eventos**: o comando publica, a consulta lê |
| **curl** | faz requisições HTTP pelo terminal | é o "cliente" que você vai usar |

## Como funciona este tutorial

- **▶ Executar**, embaixo de um bloco de comando, roda o comando no terminal.
- **Verificar** confere o seu código e diz o que falta quando algo dá errado.
- O arquivo a editar abre sozinho, ao lado. Procure o marcador **✏️**.
- Os serviços recarregam sozinhos quando você **salva** um arquivo (`Ctrl+S`).

## Preparando o ambiente

Ao abrir esta tela, o terminal já começou a rodar a partir do comando `docker compose up -d --build --wait`:

- `up`: cria e liga os containers descritos no `docker-compose.yml`;
- `-d`: roda em segundo plano e devolve o terminal para você;
- `--build`: constrói a imagem dos serviços Python antes de subir;
- `--wait`: só termina quando todos os serviços estiverem **saudáveis**
  (respondendo). Assim você não começa com o ambiente pela metade.

Na primeira vez demora 1 ou 2 minutos, porque as imagens são baixadas. Quando o
terminal voltar ao prompt, clique em **Começar**.

> Pré-requisitos: Docker com Docker Compose e Python 3 (usado pelas
> verificações). No GitHub Codespaces já vem tudo instalado.
