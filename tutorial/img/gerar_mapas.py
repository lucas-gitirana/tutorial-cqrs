"""Gera os diagramas "você está aqui" (mapa-*.svg) usados no texto das etapas.

Cada mapa é o mesmo desenho da arquitetura com uma parte destacada.
Para regenerar depois de mudar algo:  python3 tutorial/img/gerar_mapas.py
"""
from pathlib import Path

ESCRITA, EVENTOS, LEITURA, APAGADO = "#d9480f", "#c2255c", "#1971c2", "#adb5bd"

# nome: (x, y, largura, altura, linha 1, linha 2, cor quando destacado)
CAIXAS = {
    "voce_esq": (15, 83, 90, 54, "Você", "(curl)", "#495057"),
    "comando": (185, 75, 160, 70, "pedidos-comando", "porta 8011", ESCRITA),
    "sqlite": (185, 205, 160, 60, "SQLite", "modelo de escrita", ESCRITA),
    "redis": (435, 75, 160, 70, "Redis Stream", "pedidos.eventos", EVENTOS),
    "consulta": (685, 75, 160, 70, "pedidos-consulta", "porta 8012", LEITURA),
    "leitura": (685, 205, 160, 60, "projeções", "modelo de leitura", LEITURA),
    "voce_dir": (925, 83, 90, 54, "Você", "(curl)", "#495057"),
}

# nome: (x1, y1, x2, y2, rótulo, cor quando destacada)
SETAS = {
    "post": (107, 110, 182, 110, "POST", ESCRITA),
    "grava": (265, 147, 265, 202, "grava", ESCRITA),
    "publica": (347, 110, 432, 110, "evento", EVENTOS),
    "entrega": (597, 110, 682, 110, "evento", EVENTOS),
    "projeta": (765, 147, 765, 202, "projeta", LEITURA),
    "get": (923, 110, 848, 110, "GET", LEITURA),
}

TUDO = set(CAIXAS) | set(SETAS)
MAPAS = {
    "mapa-geral": TUDO,
    "mapa-comando": {"voce_esq", "comando", "sqlite", "redis", "post", "grava", "publica"},
    "mapa-consulta": {"redis", "consulta", "leitura", "voce_dir", "entrega", "projeta", "get"},
    "mapa-projecao": {"redis", "consulta", "leitura", "entrega", "projeta"},
}


def svg(destaque: set[str]) -> str:
    partes = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1030 285" width="100%" '
        'font-family="Segoe UI, Helvetica, Arial, sans-serif">',
        '<defs>',
    ]
    for nome, cor in (("on-e", ESCRITA), ("on-v", EVENTOS), ("on-l", LEITURA), ("off", APAGADO)):
        partes.append(
            f'<marker id="{nome}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{cor}"/></marker>'
        )
    partes.append('</defs>')
    partes.append('<rect x="1" y="1" width="1028" height="283" rx="10" fill="#ffffff" stroke="#dee2e6"/>')
    partes.append(f'<text x="265" y="42" text-anchor="middle" font-size="15" font-weight="700" fill="{ESCRITA}">'
                  'ESCRITA · Command</text>')
    partes.append(f'<text x="765" y="42" text-anchor="middle" font-size="15" font-weight="700" fill="{LEITURA}">'
                  'LEITURA · Query</text>')
    partes.append('<line x1="515" y1="20" x2="515" y2="62" stroke="#dee2e6" stroke-dasharray="4 4"/>')

    marcador = {ESCRITA: "on-e", EVENTOS: "on-v", LEITURA: "on-l"}
    for nome, (x1, y1, x2, y2, rotulo, cor) in SETAS.items():
        ligado = nome in destaque
        c = cor if ligado else APAGADO
        partes.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{3 if ligado else 2}" '
            f'marker-end="url(#{marcador[cor] if ligado else "off"})"/>'
        )
        vertical = x1 == x2
        tx, ty = (x1 + 10, (y1 + y2) / 2 + 4) if vertical else ((x1 + x2) / 2, y1 - 10)
        ancora = "start" if vertical else "middle"
        partes.append(f'<text x="{tx}" y="{ty}" text-anchor="{ancora}" font-size="12" fill="{c}" '
                      f'font-weight="{600 if ligado else 400}">{rotulo}</text>')

    for nome, (x, y, w, h, l1, l2, cor) in CAIXAS.items():
        ligado = nome in destaque
        c = cor if ligado else APAGADO
        fundo = "#ffffff" if not ligado else {ESCRITA: "#fff4e6", EVENTOS: "#fff0f6", LEITURA: "#e7f5ff"}.get(cor, "#f1f3f5")
        partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fundo}" stroke="{c}" '
                      f'stroke-width="{2.5 if ligado else 1.5}"/>')
        cx = x + w / 2
        partes.append(f'<text x="{cx}" y="{y + h / 2 - 3}" text-anchor="middle" font-size="14" font-weight="700" '
                      f'fill="{c if ligado else APAGADO}">{l1}</text>')
        partes.append(f'<text x="{cx}" y="{y + h / 2 + 15}" text-anchor="middle" font-size="12" '
                      f'fill="{"#495057" if ligado else APAGADO}">{l2}</text>')

    partes.append('</svg>')
    return "\n".join(partes) + "\n"


if __name__ == "__main__":
    pasta = Path(__file__).parent
    for nome, destaque in MAPAS.items():
        (pasta / f"{nome}.svg").write_text(svg(destaque), encoding="utf-8")
        print(f"gerado {nome}.svg")
