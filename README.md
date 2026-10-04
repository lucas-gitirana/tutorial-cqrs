# Tutorial interativo: padrão CQRS

Tutorial prático da disciplina de DevOps (UDESC) sobre o padrão **CQRS**
(*Command Query Responsibility Segregation*). Você separa a escrita e a leitura
de um microsserviço de pedidos: o lado de comando grava em um banco
normalizado e publica eventos, e o lado de consulta monta projeções otimizadas
para leitura.

**Duração estimada:** 35 minutos · 5 etapas com avaliação automática.

## Como começar

### Opção 1: GitHub Codespaces (recomendado)

1. Clique em **Code → Codespaces → Create codespace on main**.
2. Aguarde o ambiente abrir. Docker e Python já vêm instalados.
3. Instale a extensão **Tutoriais Interativos de Microsserviços** (veja abaixo).

### Opção 2: na sua máquina

Pré-requisitos: [VS Code](https://code.visualstudio.com/), Docker com Docker
Compose v2, Python 3.9+ e `bash` (Linux, macOS ou WSL no Windows).

```bash
git clone <url-deste-repositorio>
code tutorial-cqrs
```

### Instalando a extensão

Baixe o arquivo `.vsix` da extensão
[Tutoriais Interativos de Microsserviços](https://github.com/lucas-gitirana/tutoriais-interativos-microsservicos)
e instale em **Extensions → ⋯ → Install from VSIX...**. Ao abrir esta pasta, o
tutorial aparece na aba **Tutoriais Interativos** da barra lateral. Clique em
**Executar tutorial**.

## Estrutura

```text
index.json                 definição do tutorial (lida pela extensão)
docker-compose.yml         redis + pedidos-comando (8011) + pedidos-consulta (8012)
servicos/
  pedidos-comando/         lado de ESCRITA: comandos, SQLite, publica eventos
  pedidos-consulta/        lado de LEITURA: projeções em memória
tutorial/
  *.md                     texto de cada etapa
  verificar-etapa-NN.sh    avaliação automática de cada etapa
  verificacoes/            checagens em Python (só biblioteca padrão)
```

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| `Connection refused` nas verificações | `docker compose up -d --build --wait` e confira `docker compose ps` |
| Alterei o código e nada mudou | reinicie o serviço: `docker compose restart <servico>` |
| Quero recomeçar do zero | `docker compose down -v && docker compose up -d --build --wait` |

O código completo de referência fica na branch **`solucao`**.
