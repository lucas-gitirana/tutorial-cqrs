"""Serviço pedidos-consulta: a API de LEITURA dos pedidos (porta 8012).

Ao iniciar, lê o stream de eventos desde o início e reconstrói o modelo de
leitura em memória; depois continua escutando novos eventos.

Rotas:
  GET /pedidos/<id>              -> detalhes de um pedido
  GET /clientes/<cliente>/resumo -> pedidos ativos e total gasto do cliente
  GET /produtos/mais-vendidos    -> ranking de produtos (Etapa 9)
  GET /saude                     -> estado do serviço e da projeção
"""
import logging
import os
import threading
import time

from flask import Flask, jsonify, request

from barramento import Barramento
from projecoes import ModeloDeLeitura, aplicar_evento

app = Flask(__name__)
app.json.ensure_ascii = False


class _OcultarHealthcheck(logging.Filter):
    """Esconde dos logs as chamadas do healthcheck do Docker a /saude."""

    def filter(self, registro: logging.LogRecord) -> bool:
        return "/saude" not in registro.getMessage()


logging.getLogger("werkzeug").addFilter(_OcultarHealthcheck())

# Atraso artificial para deixar visível a consistência eventual (Etapa 8).
ATRASO_SEGUNDOS = float(os.environ.get("ATRASO_PROJECAO_SEGUNDOS", "0"))

modelo = ModeloDeLeitura()
trava = threading.Lock()
progresso = {"eventos_processados": 0, "ultimo_evento": None, "erro": None}
barramento = Barramento(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))


def ao_receber(evento: dict, id_evento: str) -> None:
    # O id do Redis começa com o instante de publicação (ms). Eventos antigos
    # (reprocessados no início) são aplicados na hora; eventos novos esperam
    # ATRASO_SEGUNDOS para simular uma réplica de leitura atrasada.
    publicado_em = int(id_evento.split("-")[0]) / 1000
    espera = publicado_em + ATRASO_SEGUNDOS - time.time()
    if espera > 0:
        time.sleep(espera)

    try:
        with trava:
            aplicar_evento(modelo, evento)
    except Exception as erro:  # não derruba o consumidor por causa de uma projeção com defeito
        progresso["erro"] = f"{type(erro).__name__}: {erro}"
        print(f"[projeção] ERRO ao aplicar {evento['tipo']} ({id_evento}): {progresso['erro']}")
        return

    progresso["eventos_processados"] += 1
    progresso["ultimo_evento"] = id_evento
    print(f"[projeção] {evento['tipo']} aplicado (pedido {evento['dados'].get('pedido_id')})")


@app.get("/pedidos/<pedido_id>")
def obter_pedido(pedido_id: str):
    with trava:
        pedido = modelo.pedidos.get(pedido_id)
    if pedido is None:
        return jsonify(erro=f"Pedido '{pedido_id}' não está no modelo de leitura (ainda?)."), 404
    return jsonify(pedido)


@app.get("/clientes/<cliente>/resumo")
def resumo_do_cliente(cliente: str):
    with trava:
        resumo = modelo.resumo_por_cliente.get(cliente)
    if resumo is None:
        return jsonify(erro=f"Nenhum pedido do cliente '{cliente}' no modelo de leitura."), 404
    return jsonify(resumo)


@app.get("/produtos/mais-vendidos")
def mais_vendidos():
    with trava:
        return jsonify(modelo.mais_vendidos(limite=request.args.get("limite", 5, type=int)))


@app.get("/saude")
def saude():
    return jsonify(servico="pedidos-consulta", status="ok", atraso_projecao_segundos=ATRASO_SEGUNDOS, **progresso)


if __name__ == "__main__":
    # use_reloader: ao salvar um .py, o serviço reinicia sozinho e reconstrói o
    # modelo de leitura do zero. O consumidor só roda no processo filho (o que
    # atende as requisições), não no processo que vigia os arquivos.
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=barramento.consumir_desde_o_inicio, args=(ao_receber,), daemon=True).start()
    app.run(host="0.0.0.0", port=8000, threaded=True, use_reloader=True)
