"""Peças da página pública (v3a-ag/.github/profile) — v4.

Técnica e operacional, com gráficos animados. Grade única (gerador/bloco.py): todas as peças com a
mesma largura e margem, título da seção dentro do bloco. Slogan do Igor, sem variação:
"Tempo inteligente é experiência de marca. Experiência de marca é V3A."
"""
from pathlib import Path

from gerador import bloco as blc
from gerador import identidade as idt
from gerador import motion
from gerador import svg
from gerador import texto as tx
from gerador.icones import icone

SLOGAN = {"titulo": ["TEMPO INTELIGENTE É", "EXPERIÊNCIA", "DE MARCA"],
          "assinatura": ["EXPERIÊNCIA", "DE MARCA", "É V3A."]}
SLOGAN_ALT = "Tempo inteligente é experiência de marca. Experiência de marca é V3A."
# Fechamento: versão aprovada pelo Igor em 25/11 (o hero usa o slogan; o fechamento, esta variação).
FECHAMENTO = {"titulo": ["ROTINA RESOLVIDA É", "EXPERIÊNCIA", "DE MARCA"], "assinatura": SLOGAN["assinatura"]}
FECHAMENTO_ALT = "Rotina resolvida é experiência de marca. Experiência de marca é V3A."

# O 'X' do hero gira entre benefícios que quem recebe a automação sente; a primeira é o slogan.
PALAVRAS = ["TEMPO INTELIGENTE", "ROTINA RESOLVIDA", "DADO CONFIÁVEL", "PROCESSO SEM ATRITO",
            "ENTREGA NO PRAZO", "FECHAMENTO SEM SUSTO", "CONTA QUE BATE", "EQUIPE LIVRE"]

COPY = {
    "hero": SLOGAN,
    "palavras": PALAVRAS,
    "fechamento": FECHAMENTO,
    "secoes": {
        "esteira": ("01.", "ONDE A AUTOMAÇÃO ENTRA",
                    "Cada job passa por cinco momentos, e em todos há rotina que pode sair da mão das pessoas."),
        "anatomia": ("02.", "ANATOMIA DE UMA AUTOMAÇÃO",
                     "Toda automação tem a mesma forma, e alguém sempre confere antes de seguir."),
        "arquitetura": ("03.", "DO PEDIDO À PRODUÇÃO",
                        "Nasce de um card, vira código e só entra em produção pela esteira, com aprovação."),
        "principios": ("04.", "PRINCÍPIOS", "O que orienta cada automação que a gente coloca no ar."),
        "stack": ("05.", "COM O QUE A GENTE CONSTRÓI", "As ferramentas por trás das automações."),
    },
    "esteira": [
        ("balao", "BRIEFING E ABERTURA", "Estruturar o job"),
        ("grafico", "PLANEJAMENTO", "Consolidar dados e cadastros"),
        ("contrato", "PRÉ-PRODUÇÃO", "Contratos e documentos"),
        ("camera", "PRODUÇÃO", "Documentar peças e entregas"),
        ("check", "FECHAMENTO", "Conferir despesas e gerar relatórios"),
    ],
    "esteira_rodape": "O TRABALHO HUMANO PERMANECE NO CENTRO.",
    "anatomia": {
        "etapas": ["ENTRADA", "PROCESSAMENTO", "SAÍDA", "VALIDAÇÃO HUMANA"],
        "exemplos": [
            [("grade", "PLANILHAS"), ("cruzamento", "CRUZAMENTO"), ("camadas", "BASE ORGANIZADA")],
            [("pdf", "NOTAS E DOCUMENTOS"), ("faisca", "EXTRAÇÃO COM IA"), ("grade", "PLANILHA FISCAL")],
            [("camera", "FOTOS DO EVENTO"), ("engrenagem", "ASSOCIAÇÃO"), ("slide", "RELATÓRIO EM SLIDES")],
        ],
        "validacao": ("aprova", "GENTE REVISA E APROVA"),
    },
    "arquitetura": [
        ("s:jira", "PEDIDO", "card na fila"),
        ("s:github", "CÓDIGO", "repositório e PR"),
        ("s:githubactions", "ESTEIRA", "ficha, testes, imagem"),
        ("servidor", "PRODUÇÃO", "apps e workflows"),
        ("camadas", "VERSÃO", "backup diário"),
    ],
    "arquitetura_rodape": "TUDO VERSIONADO. NADA PUBLICA SEM APROVAÇÃO.",
    "principios": [
        ("pessoa", ["GENTE NO", "CENTRO"]),
        ("grafico", ["DADO, NÃO", "ACHISMO"]),
        ("camadas", ["VERSÃO", "E BACKUP"]),
        ("passos", ["PASSOS", "CURTOS"]),
    ],
    "stack": [("n8n", "N8N"), ("python", "PYTHON"), ("supabase", "SUPABASE"),
              ("google", "GOOGLE WORKSPACE"), ("githubactions", "GITHUB ACTIONS"), ("claude", "CLAUDE")],
}

ENTRADA = motion.entrada_hero()  # usado também pelo hero de membros


def _ic(nome, t, x, y, tam):
    if nome.startswith("s:"):
        return idt.simple_icon(nome[2:], t["texto"], x, y, tam)
    return icone(nome, t["texto"], t["destaque"], x, y, tam)


def _titulo(linhas, x, y0, passo, tam, cor, animado=True):
    pesos = [400, 800, 800]
    return "".join((f'<g class="l l{i}">' if animado else "<g>")
                   + svg.linha(s, x, y0 + i * passo, tam, cor, pesos[i], 0.005) + "</g>"
                   for i, s in enumerate(linhas))


def _assinatura(linhas, x, y0, passo, tam, cor, animado=True):
    cls = ' class="ass"' if animado else ""
    return (f"<g{cls}>" + "".join(
        svg.linha(s, x, y0 + i * passo, tam, cor, 800 if i == len(linhas) - 1 else 400, 0.005)
        for i, s in enumerate(linhas)) + "</g>")


def _linha_x(x, y, tam):
    """Linha 1 do hero: o 'X' (palavras empilhadas, uma visível por vez) e o 'É' que desliza junto."""
    def w(txt):
        return tx.largura(txt + " ", tam, 400, 0.005)
    palavras = "".join(f'<g class="pal pal{k}">' + svg.linha(p, x, y, tam, "{cor}", 400, 0.005) + "</g>"
                       for k, p in enumerate(PALAVRAS))
    e = '<g class="e">' + svg.linha("É", x + w(PALAVRAS[0]), y, tam, "{cor}", 400, 0.005) + "</g>"
    desloc = [w(p) - w(PALAVRAS[0]) for p in PALAVRAS]
    return palavras + e, motion.palavras(len(PALAVRAS), desloc)


def hero(tema):
    t = idt.TEMA[tema]
    W, x = 830, 440
    linha1, css = _linha_x(x, 23, 25.5)
    corpo = (idt.monograma(0, 0, 48, t["logo"], "logo")
             + linha1.replace("{cor}", t["texto"])
             + _titulo(SLOGAN["titulo"], x, 23, 33, 25.5, t["texto"]).split("</g>", 1)[1]
             + _assinatura(SLOGAN["assinatura"], x, 141, 21, 16.4, t["texto"])
             + f'<g transform="translate(0 172)">{idt.grafismo(W - 157, 0, 157, t["logo"], pecas=True)}</g>')
    return blc.bloco(tema, "desk", SLOGAN_ALT, corpo, 186, ENTRADA + css)


def hero_celular(tema):
    t = idt.TEMA[tema]
    W, lg = 360, 140
    linha1, css = _linha_x(0, 88, 24)
    corpo = (idt.monograma(0, 0, 36, t["logo"], "logo")
             + linha1.replace("{cor}", t["texto"])
             + _titulo(SLOGAN["titulo"], 0, 88, 38, 24, t["texto"]).split("</g>", 1)[1]
             + _assinatura(SLOGAN["assinatura"], 0, 200, 19, 14.5, t["texto"])
             + f'<g transform="translate(0 252)">{idt.grafismo(W - lg, 0, lg, t["logo"], pecas=True)}</g>')
    return blc.bloco(tema, "cel", SLOGAN_ALT, corpo, 266, ENTRADA + css)


def fechamento(tema):
    t = idt.TEMA[tema]
    W = 830
    w_logo = idt.largura_monograma(40)
    corpo = (idt.monograma(W - w_logo, 0, 40, t["logo"])
             + _titulo(FECHAMENTO["titulo"], 0, 23, 33, 25.5, t["texto"], animado=False)
             + _assinatura(FECHAMENTO["assinatura"], 440, 141, 21, 16.4, t["texto"], animado=False)
             + f'<g transform="translate(0 172)">{idt.grafismo(W - 157, 0, 157, t["logo"])}</g>')
    return blc.bloco(tema, "desk", FECHAMENTO_ALT, corpo, 186)


def fechamento_celular(tema):
    t = idt.TEMA[tema]
    W, lg = 360, 140
    corpo = (idt.monograma(0, 0, 34, t["logo"])
             + _titulo(FECHAMENTO["titulo"], 0, 84, 36, 22, t["texto"], animado=False)
             + _assinatura(FECHAMENTO["assinatura"], 0, 192, 19, 14.5, t["texto"], animado=False)
             + f'<g transform="translate(0 252)">{idt.grafismo(W - lg, 0, lg, t["logo"])}</g>')
    return blc.bloco(tema, "cel", FECHAMENTO_ALT, corpo, 266)


# ---------- corpos dos diagramas (coordenadas da área de conteúdo) ----------

def _esteira_desk(t):
    W, cy, r = 830, 40, 38
    est = COPY["esteira"]
    passo = (W - 166) / (len(est) - 1)
    xs = [83 + i * passo for i in range(len(est))]
    p = [f'<rect x="{xs[0]}" y="{cy - 1.5}" width="{xs[-1] - xs[0]}" height="3" fill="{t["linha"]}"/>']
    for x, (ic, rot, desc) in zip(xs, est):
        p.append(f'<circle cx="{x}" cy="{cy}" r="{r}" fill="{t["pagina"]}" stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, x - 20, cy - 20, 40))
        for j, l in enumerate(svg.quebrar(rot, 14.5, 150, 800, 0.01)):
            p.append(svg.linha(l, x, cy + r + 30 + j * 19, 14.5, t["texto"], 800, 0.01, ancora="meio"))
        for j, l in enumerate(svg.quebrar(desc, 13.5, 140, 400)):
            p.append(svg.linha(l, x, cy + r + 74 + j * 18, 13.5, t["suave"], 400, 0, ancora="meio"))
    p.append(f'<circle class="anel" cx="{xs[0]}" cy="{cy}" r="{r + 2}" fill="none" stroke="{t["destaque"]}" stroke-width="5"/>')
    A = 236
    p.append(svg.linha(COPY["esteira_rodape"], 0, A, 13.5, t["texto"], 800, 0.04))
    return "".join(p), A + 4, motion.passos("anel", "X", passo, len(est))


def _esteira_cel(t):
    est = COPY["esteira"]
    cx, r, passo, y0 = 30, 30, 92, 32
    p = [f'<rect x="{cx - 1.5}" y="{y0}" width="3" height="{passo * (len(est) - 1)}" fill="{t["linha"]}"/>']
    for i, (ic, rot, desc) in enumerate(est):
        cy = y0 + i * passo
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["pagina"]}" stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, cx - 16, cy - 16, 32))
        p.append(svg.linha(rot, 78, cy - 3, 16, t["texto"], 800, 0.01))
        p.append(svg.linha(desc, 78, cy + 19, 14, t["suave"], 400))
    p.append(f'<circle class="anel" cx="{cx}" cy="{y0}" r="{r + 2}" fill="none" stroke="{t["destaque"]}" stroke-width="4.5"/>')
    y = y0 + passo * (len(est) - 1) + r + 34
    linhas = svg.quebrar(COPY["esteira_rodape"], 14, 360, 800, 0.03)
    for j, l in enumerate(linhas):
        p.append(svg.linha(l, 0, y + j * 20, 14, t["texto"], 800, 0.03))
    return "".join(p), y + (len(linhas) - 1) * 20 + 4, motion.passos("anel", "Y", passo, len(est))


CICLO = motion.ciclo(3) + motion.fluxo()


def _exemplos(col, t, cx, y_ic, y_txt, tam_ic, tam_txt, larg_txt, meio=True):
    out = []
    for k, ex in enumerate(COPY["anatomia"]["exemplos"]):
        ic, rot = ex[col]
        partes = _ic(ic, t, cx - tam_ic / 2 if meio else cx, y_ic, tam_ic)
        for j, l in enumerate(svg.quebrar(rot, tam_txt, larg_txt, 700, 0.01)):
            partes += svg.linha(l, cx if meio else cx + tam_ic + 16, y_txt + j * (tam_txt + 5),
                                tam_txt, t["texto"], 700, 0.01, ancora="meio" if meio else "inicio")
        out.append(f'<g class="ex ex{k}">{partes}</g>')
    return "".join(out)


def _anatomia_desk(t):
    W, gap, y_card, h_card = 830, 34, 30, 168
    larg = (W - 3 * gap - 4) / 4
    etapas = COPY["anatomia"]["etapas"]
    p = []
    for i, etapa in enumerate(etapas):
        x = 2 + i * (larg + gap)
        cx = x + larg / 2
        p.append(svg.linha(f"0{i + 1}", x, 14, 14, t["destaque"], 900, 0))
        p.append(svg.linha(etapa, x + 30, 14, svg.caber(etapa, 14, larg - 30, 800, 0.01), t["texto"], 800, 0.01))
        p.append(f'<rect x="{x}" y="{y_card}" width="{larg}" height="{h_card}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["destaque"] if i == 3 else t["linha"]}" stroke-width="{3 if i == 3 else 2}"/>')
        if i < 3:
            p.append(_exemplos(i, t, cx, y_card + 34, y_card + 124, 56, 13.5, larg - 24))
            yc = y_card + h_card / 2
            p.append(f'<path class="flui" d="M{x + larg + 4} {yc}H{x + larg + gap - 4}" stroke="{t["destaque"]}" '
                     f'stroke-width="3" stroke-dasharray="6 4" fill="none"/>')
        else:
            ic, rot = COPY["anatomia"]["validacao"]
            p.append(_ic(ic, t, cx - 28, y_card + 34, 56))
            for j, l in enumerate(svg.quebrar(rot, 13.5, larg - 24, 700, 0.01)):
                p.append(svg.linha(l, cx, y_card + 124 + j * 18.5, 13.5, t["texto"], 700, 0.01, ancora="meio"))
    return "".join(p), y_card + h_card + 2, CICLO


def _anatomia_cel(t):
    etapas = COPY["anatomia"]["etapas"]
    W, h, gap = 360, 100, 30
    p = []
    for i, etapa in enumerate(etapas):
        y = 2 + i * (h + gap)
        p.append(f'<rect x="1" y="{y}" width="{W - 2}" height="{h}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["destaque"] if i == 3 else t["linha"]}" stroke-width="{3 if i == 3 else 2}"/>')
        p.append(svg.linha(f"0{i + 1}", 18, y + 30, 14, t["destaque"], 900, 0))
        p.append(svg.linha(etapa, 48, y + 30, 14, t["texto"], 800, 0.01))
        if i < 3:
            p.append(_exemplos(i, t, 18, y + 46, y + 74, 40, 15, 260, meio=False))
            p.append(f'<path class="flui" d="M{W / 2} {y + h + 4}V{y + h + gap - 4}" stroke="{t["destaque"]}" '
                     f'stroke-width="3" stroke-dasharray="6 4" fill="none"/>')
        else:
            ic, rot = COPY["anatomia"]["validacao"]
            p.append(_ic(ic, t, 18, y + 46, 40))
            p.append(svg.linha(rot, 74, y + 74, 15, t["texto"], 700, 0.01))
    return "".join(p), len(etapas) * h + (len(etapas) - 1) * gap + 4, CICLO


def _arquitetura_desk(t):
    nos = COPY["arquitetura"]
    W, cy, s = 830, 40, 76
    passo = (W - 166) / (len(nos) - 1)
    xs = [83 + i * passo for i in range(len(nos))]
    p = [f'<rect x="{xs[0]}" y="{cy - 1.5}" width="{xs[-1] - xs[0]}" height="3" fill="{t["linha"]}"/>',
         f'<rect class="pacote" x="{xs[0] - 9}" y="{cy - 6}" width="18" height="12" rx="4" fill="{t["destaque"]}"/>']
    for x, (ic, rot, desc) in zip(xs, nos):
        p.append(f'<rect x="{x - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="18" fill="{t["pagina"]}" '
                 f'stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, x - 18, cy - 18, 36))
        p.append(svg.linha(rot, x, cy + s / 2 + 30, 15, t["texto"], 800, 0.01, ancora="meio"))
        p.append(svg.linha(desc, x, cy + s / 2 + 52, 13.5, t["suave"], 400, 0, ancora="meio"))
    A = 186
    p.append(svg.linha(COPY["arquitetura_rodape"], 0, A, 13.5, t["texto"], 800, 0.04))
    return "".join(p), A + 4, motion.passos("pacote", "X", passo, len(nos))


def _arquitetura_cel(t):
    nos = COPY["arquitetura"]
    cx, s, passo, y0 = 30, 60, 90, 32
    p = [f'<rect x="{cx - 1.5}" y="{y0}" width="3" height="{passo * (len(nos) - 1)}" fill="{t["linha"]}"/>',
         f'<rect class="pacote" x="{cx - 6}" y="{y0 - 9}" width="12" height="18" rx="4" fill="{t["destaque"]}"/>']
    for i, (ic, rot, desc) in enumerate(nos):
        cy = y0 + i * passo
        p.append(f'<rect x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, cx - 15, cy - 15, 30))
        p.append(svg.linha(rot, 78, cy - 3, 16, t["texto"], 800, 0.01))
        p.append(svg.linha(desc, 78, cy + 19, 14, t["suave"], 400))
    y = y0 + passo * (len(nos) - 1) + s / 2 + 34
    linhas = svg.quebrar(COPY["arquitetura_rodape"], 14, 360, 800, 0.03)
    for j, l in enumerate(linhas):
        p.append(svg.linha(l, 0, y + j * 20, 14, t["texto"], 800, 0.03))
    return "".join(p), y + (len(linhas) - 1) * 20 + 4, motion.passos("pacote", "Y", passo, len(nos))


def _grade(itens, colunas, larg_cel, alt_cel, desenha, t, tam_ic, tam_txt):
    return "".join(desenha(it, t, (i % colunas) * larg_cel + larg_cel / 2, (i // colunas) * alt_cel, tam_ic, tam_txt)
                   for i, it in enumerate(itens))


def _principio(it, t, cx, y, tam_ic, tam_txt):
    ic, linhas = it
    out = _ic(ic, t, cx - tam_ic / 2, y, tam_ic)
    for j, l in enumerate(linhas):
        out += svg.linha(l, cx, y + tam_ic + 32 + j * (tam_txt + 5), tam_txt, t["texto"], 800, 0.01, ancora="meio")
    return out


def _ferramenta(it, t, cx, y, tam_ic, tam_txt):
    nome, rot = it
    out = idt.simple_icon(nome, t["texto"], cx - tam_ic / 2, y, tam_ic)
    for j, l in enumerate(svg.quebrar(rot, tam_txt, 120, 700, 0.03)):
        out += svg.linha(l, cx, y + tam_ic + 26 + j * (tam_txt + 4), tam_txt, t["suave"], 700, 0.03, ancora="meio")
    return out


def _principios_desk(t):
    return _grade(COPY["principios"], 4, 830 / 4, 0, _principio, t, 52, 17), 128, ""


def _principios_cel(t):
    return _grade(COPY["principios"], 2, 180, 140, _principio, t, 46, 17), 260, ""


def _stack_desk(t):
    return _grade(COPY["stack"], 6, 830 / 6, 0, _ferramenta, t, 36, 12), 92, ""


def _stack_cel(t):
    return _grade(COPY["stack"], 3, 120, 96, _ferramenta, t, 34, 12), 186, ""


ALT = {
    "esteira": "Onde a automação entra: briefing e abertura, planejamento, pré-produção, produção e fechamento. "
               "O trabalho humano permanece no centro.",
    "anatomia": "Anatomia de uma automação: entrada, processamento, saída e validação humana.",
    "arquitetura": "Do pedido à produção: pedido, código, esteira, produção e versão. "
                   "Tudo versionado; nada publica sem aprovação.",
    "principios": "Princípios: gente no centro, dado não achismo, versão e backup, passos curtos.",
    "stack": "Ferramentas: n8n, Python, Supabase, Google Workspace, GitHub Actions e Claude.",
}
CORPOS = {"esteira": (_esteira_desk, _esteira_cel), "anatomia": (_anatomia_desk, _anatomia_cel),
          "arquitetura": (_arquitetura_desk, _arquitetura_cel), "principios": (_principios_desk, _principios_cel),
          "stack": (_stack_desk, _stack_cel)}


def secao(chave, modo):
    def gerar(tema):
        t = idt.TEMA[tema]
        fn = CORPOS[chave][0 if modo == "desk" else 1]
        corpo, A, css = fn(t)
        num, titulo, sub = COPY["secoes"][chave]
        return blc.bloco(tema, modo, f"{num} {titulo.capitalize()}. {ALT[chave]}", corpo, A, css,
                         cab=(num, titulo, sub))
    return gerar


PECAS = {"hero": hero, "hero-celular": hero_celular,
         "fechamento": fechamento, "fechamento-celular": fechamento_celular}
for _c in CORPOS:
    PECAS[_c] = secao(_c, "desk")
    PECAS[f"{_c}-celular"] = secao(_c, "cel")


def gerar_todas(pasta: Path) -> list:
    saida = []
    for nome, fn in PECAS.items():
        saida += svg.salvar(nome, fn, pasta)
    return saida


if __name__ == "__main__":
    import sys
    for p in gerar_todas(Path(sys.argv[1] if len(sys.argv) > 1 else "saida")):
        print(p)
