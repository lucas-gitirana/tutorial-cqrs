![Mapa: visão geral](tutorial/img/mapa-geral.svg)

📍 **Você está aqui:** conhecendo as peças do mapa.

## 1. Veja os containers

```bash
docker compose ps
```

Devem aparecer **3 serviços** com estado `running (healthy)`:

| Serviço | No mapa |
| --- | --- |
| `pedidos-comando` | lado de **escrita** (porta 8011) |
| `redis` | o **barramento de eventos** no meio |
| `pedidos-consulta` | lado de **leitura** (porta 8012) |

O `docker-compose.yml`, aberto ao lado, descreve esses três serviços.

> Algum serviço não está `healthy`? Rode `docker compose up -d --build --wait` de novo.

## 2. Clique em Verificar ✔

A verificação confere se os dois serviços estão respondendo.
