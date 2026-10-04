"""Modelo de ESCRITA: banco relacional normalizado (SQLite).

O modelo de escrita é otimizado para garantir as regras de negócio e a
integridade dos dados (chaves, normalização, transações) — não para
consultas. Repare que os itens ficam em uma tabela separada: montar um
pedido completo exige um JOIN.
"""
from __future__ import annotations

import sqlite3
import threading


class RepositorioSQLite:
    def __init__(self, caminho: str) -> None:
        self._conexao = sqlite3.connect(caminho, check_same_thread=False)
        self._conexao.row_factory = sqlite3.Row
        self._trava = threading.Lock()
        with self._trava, self._conexao:
            self._conexao.executescript(
                """
                CREATE TABLE IF NOT EXISTS pedidos (
                    id        TEXT PRIMARY KEY,
                    cliente   TEXT NOT NULL,
                    status    TEXT NOT NULL,
                    criado_em TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS itens_pedido (
                    pedido_id      TEXT NOT NULL REFERENCES pedidos(id),
                    produto        TEXT NOT NULL,
                    quantidade     INTEGER NOT NULL,
                    preco_unitario REAL NOT NULL
                );
                """
            )

    def inserir_pedido(self, pedido_id: str, cliente: str, itens: list, criado_em: str) -> None:
        with self._trava, self._conexao:  # uma transação
            self._conexao.execute(
                "INSERT INTO pedidos (id, cliente, status, criado_em) VALUES (?, ?, 'CRIADO', ?)",
                (pedido_id, cliente, criado_em),
            )
            self._conexao.executemany(
                "INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                [(pedido_id, i["produto"], i["quantidade"], i["preco"]) for i in itens],
            )

    def obter_pedido(self, pedido_id: str) -> dict | None:
        """Devolve {id, cliente, status, itens, total} ou None se não existir."""
        with self._trava:
            linha = self._conexao.execute(
                "SELECT id, cliente, status FROM pedidos WHERE id = ?", (pedido_id,)
            ).fetchone()
            if linha is None:
                return None
            itens = [
                {"produto": i["produto"], "quantidade": i["quantidade"], "preco": i["preco_unitario"]}
                for i in self._conexao.execute(
                    "SELECT produto, quantidade, preco_unitario FROM itens_pedido WHERE pedido_id = ?",
                    (pedido_id,),
                )
            ]
        total = round(sum(i["quantidade"] * i["preco"] for i in itens), 2)
        return {"id": linha["id"], "cliente": linha["cliente"], "status": linha["status"],
                "itens": itens, "total": total}

    def atualizar_status(self, pedido_id: str, status: str) -> None:
        with self._trava, self._conexao:
            self._conexao.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))

    def contar_pedidos(self) -> int:
        with self._trava:
            return self._conexao.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
