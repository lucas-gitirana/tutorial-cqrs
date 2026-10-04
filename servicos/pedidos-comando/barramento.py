"""Barramento de eventos sobre Redis Streams.

Um *stream* do Redis é um log ordenado e persistente de mensagens: quem publica
acrescenta um evento ao final; quem consome pode ler a partir de qualquer
posição — inclusive do início, o que permite reconstruir um modelo de leitura
inteiro "reassistindo" todos os eventos já publicados.

Este arquivo é infraestrutura: você não precisa alterá-lo no tutorial.
"""
from __future__ import annotations

import json
import time
from typing import Callable

import redis

STREAM_PEDIDOS = "pedidos.eventos"


class Barramento:
    def __init__(self, url: str, stream: str = STREAM_PEDIDOS) -> None:
        self.stream = stream
        self.redis = redis.Redis.from_url(url, decode_responses=True)

    def publicar(self, evento: dict) -> str:
        """Acrescenta o evento ao final do stream e devolve o id gerado."""
        return self.redis.xadd(
            self.stream,
            {"tipo": evento["tipo"], "dados": json.dumps(evento["dados"], ensure_ascii=False)},
        )

    def consumir_desde_o_inicio(self, ao_receber: Callable[[dict, str], None]) -> None:
        """Lê TODOS os eventos do stream (do primeiro ao último) e depois fica
        aguardando novos eventos para sempre. Chama ``ao_receber(evento, id)``
        para cada um, na ordem em que foram publicados."""
        ultimo_id = "0"
        while True:
            try:
                respostas = self.redis.xread({self.stream: ultimo_id}, block=5000, count=100)
            except redis.ConnectionError:
                print("[barramento] Redis indisponível, tentando de novo em 2s...")
                time.sleep(2)
                continue
            for _stream, mensagens in respostas or []:
                for id_mensagem, campos in mensagens:
                    evento = {"tipo": campos["tipo"], "dados": json.loads(campos["dados"])}
                    ao_receber(evento, id_mensagem)
                    ultimo_id = id_mensagem
