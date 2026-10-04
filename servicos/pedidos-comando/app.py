"""Serviço pedidos-comando: a API de ESCRITA dos pedidos (porta 8011).

Rotas:
  POST /pedidos                 -> comando CriarPedido
  POST /pedidos/<id>/cancelar   -> comando CancelarPedido
  GET  /saude                   -> estado do serviço

Repare: não há consultas aqui (GET /pedidos responde 405). Consultas ficam
no pedidos-consulta.
"""
import logging
import os

from flask import Flask, jsonify, request

from barramento import Barramento
from comandos import ErroDeComando, cancelar_pedido, criar_pedido
from repositorio import RepositorioSQLite

app = Flask(__name__)
app.json.ensure_ascii = False


class _OcultarHealthcheck(logging.Filter):
    """Esconde dos logs as chamadas do healthcheck do Docker a /saude."""

    def filter(self, registro: logging.LogRecord) -> bool:
        return "/saude" not in registro.getMessage()


logging.getLogger("werkzeug").addFilter(_OcultarHealthcheck())

repositorio = RepositorioSQLite(os.environ.get("BANCO_PATH", "pedidos.db"))
barramento = Barramento(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))


def publicar(evento: dict) -> None:
    id_evento = barramento.publicar(evento)
    print(f"[comando] evento publicado: {evento['tipo']} (pedido {evento['dados'].get('pedido_id')}, id {id_evento})")


@app.errorhandler(ErroDeComando)
def tratar_erro_de_comando(erro: ErroDeComando):
    return jsonify(erro=erro.mensagem), erro.status


@app.post("/pedidos")
def rota_criar_pedido():
    pedido_id = criar_pedido(repositorio, publicar, request.get_json(silent=True) or {})
    # 201 Created: devolvemos só o id. Para ver o pedido, consulte o pedidos-consulta.
    return jsonify(pedido_id=pedido_id), 201


@app.post("/pedidos/<pedido_id>/cancelar")
def rota_cancelar_pedido(pedido_id: str):
    cancelar_pedido(repositorio, publicar, pedido_id)
    return jsonify(pedido_id=pedido_id, status="CANCELADO"), 200


@app.get("/pedidos")
@app.get("/pedidos/<pedido_id>")
def consultas_nao_ficam_aqui(pedido_id: str | None = None):
    return jsonify(erro="O lado de comando não responde consultas. Use o pedidos-consulta (porta 8012)."), 405


@app.get("/saude")
def saude():
    return jsonify(servico="pedidos-comando", status="ok", pedidos_gravados=repositorio.contar_pedidos())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
