"""Peças da página pública (v3a-ag/.github/profile) — v3: técnica e operacional, com gráficos animados.

Narrativa: hero (promessa) → onde a automação entra (esteira de um job) → anatomia de uma automação
(entrada → processamento → saída → validação humana) → do pedido à produção (como é construída)
→ princípios → ferramentas → fechamento. Sem números de escala, sem nome de automação, cliente,
pessoa ou servidor.
"""
from pathlib import Path

from gerador import identidade as idt
from gerador import svg
from gerador import texto as tx
from gerador.icones import icone

COPY = {
    "hero": {"titulo": ["TEMPO INTELIGENTE É", "EXPERIÊNCIA", "DE MARCA"],
             "assinatura": ["EXPERIÊNCIA", "DE MARCA", "É V3A."]},
    "secoes": {
        "secao-01": ("01.", "ONDE A AUTOMAÇÃO ENTRA"),
        "secao-02": ("02.", "ANATOMIA DE UMA AUTOMAÇÃO"),
        "secao-03": ("03.", "DO PEDIDO À PRODUÇÃO"),
        "secao-04": ("04.", "PRINCÍPIOS"),
        "secao-05": ("05.", "COM O QUE A GENTE CONSTRÓI"),
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
    "fechamento": {"titulo": ["ROTINA RESOLVIDA É", "EXPERIÊNCIA", "DE MARCA"],
                   "assinatura": ["EXPERIÊNCIA", "DE MARCA", "É V3A."]},
}

ENTRADA = (
    "@keyframes sobe{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    ".logo{animation:fade .6s ease-out both}"
    ".l{animation:sobe .6s ease-out both}"
    ".l0{animation-delay:.2s}.l1{animation-delay:.38s}.l2{animation-delay:.52s}"
    ".ass{animation:fade .6s .9s ease-out both}"
    ".graf{animation:sobe .7s 1.1s cubic-bezier(.2,.7,.2,1) both}"
)


def _ic(nome, t, x, y, tam):
    if nome.startswith("s:"):
        return idt.simple_icon(nome[2:], t["texto"], x, y, tam)
    return icone(nome, t["texto"], t["destaque"], x, y, tam)


def _titulo(linhas, x, y0, passo, tam, cor, animado=True):
    pesos = [400, 800, 800]
    return "".join((f'<g class="l l{i}">' if animado else "<g>")
                   + svg.linha(t, x, y0 + i * passo, tam, cor, pesos[i], 0.005) + "</g>"
                   for i, t in enumerate(linhas))


def _assinatura(linhas, x, y0, passo, tam, cor, classe="ass"):
    cls = f' class="{classe}"' if classe else ""
    return (f"<g{cls}>" + "".join(
        svg.linha(t, x, y0 + i * passo, tam, cor, 800 if i == len(linhas) - 1 else 400, 0.005)
        for i, t in enumerate(linhas)) + "</g>")


def _passo_css(nome, eixo, passo, n, dur):
    """Keyframes que param em cada uma das n posições (eixo X ou Y), com fade no fim."""
    quadros, fatia = [], 100 / n
    for i in range(n):
        ini, fim = i * fatia, i * fatia + fatia * 0.8
        quadros.append(f"{ini + (3 if i == 0 else 0):.1f}%{{transform:translate{eixo}({i * passo:.0f}px);opacity:1}}")
        quadros.append(f"{fim:.1f}%{{transform:translate{eixo}({i * passo:.0f}px);opacity:1}}")
    corpo = "0%{transform:translate" + eixo + "(0);opacity:0}" + "".join(quadros) + \
            "100%{transform:translate" + eixo + f"({(n - 1) * passo:.0f}px);opacity:0}}"
    return f"@keyframes {nome}{{{corpo}}}.{nome}{{animation:{nome} {dur}s ease-in-out infinite}}"


# ---------- hero e fechamento ----------

def hero(tema):
    t = idt.TEMA[tema]
    L, A, x = 830, 226, 458
    c = COPY["hero"]
    corpo = (idt.fundo(L, A, tema) + idt.monograma(34, 24, 48, t["logo"], "logo")
             + _titulo(c["titulo"], x, 47, 33, 25.5, t["texto"])
             + _assinatura(c["assinatura"], x - 2, 165, 21, 16.4, t["texto"])
             + f'<g transform="translate(0 196)">{idt.grafismo(618, 0, 157, t["logo"], "graf")}</g>')
    return idt.svg_aberto(L, A, "Tempo inteligente é experiência de marca. Experiência de marca é V3A.", ENTRADA, corpo)


def hero_celular(tema):
    t = idt.TEMA[tema]
    L, A, x, lg = 360, 320, 24, 140
    c = COPY["hero"]
    corpo = (idt.fundo(L, A, tema) + idt.monograma(x, 24, 36, t["logo"], "logo")
             + _titulo(c["titulo"], x, 112, 38, 24, t["texto"])
             + _assinatura(c["assinatura"], x, 226, 19, 14.5, t["texto"])
             + f'<g transform="translate(0 {A - 28 - lg / idt.RAZAO_GRAFISMO:.1f})">'
               f'{idt.grafismo(L - 24 - lg, 0, lg, t["logo"], "graf")}</g>')
    return idt.svg_aberto(L, A, "Tempo inteligente é experiência de marca. Experiência de marca é V3A.", ENTRADA, corpo)


def fechamento(tema):
    t = idt.TEMA[tema]
    L, A, x = 830, 226, 34
    c = COPY["fechamento"]
    w_logo = idt.largura_monograma(40)
    corpo = (idt.fundo(L, A, tema) + idt.monograma(L - 34 - w_logo, 28, 40, t["logo"])
             + _titulo(c["titulo"], x, 70, 33, 25.5, t["texto"], animado=False)
             + _assinatura(c["assinatura"], 458, 165, 21, 16.4, t["texto"], classe="")
             + f'<g transform="translate(0 196)">{idt.grafismo(618, 0, 157, t["logo"])}</g>')
    return idt.svg_aberto(L, A, "Rotina resolvida é experiência de marca. Experiência de marca é V3A.", "", corpo)


def fechamento_celular(tema):
    t = idt.TEMA[tema]
    L, A, x, lg = 360, 300, 24, 140
    c = COPY["fechamento"]
    corpo = (idt.fundo(L, A, tema) + idt.monograma(x, 24, 34, t["logo"])
             + _titulo(c["titulo"], x, 108, 36, 22, t["texto"], animado=False)
             + _assinatura(c["assinatura"], x, 214, 19, 14.5, t["texto"], classe="")
             + f'<g transform="translate(0 {A - 28 - lg / idt.RAZAO_GRAFISMO:.1f})">'
               f'{idt.grafismo(L - 24 - lg, 0, lg, t["logo"])}</g>')
    return idt.svg_aberto(L, A, "Rotina resolvida é experiência de marca. Experiência de marca é V3A.", "", corpo)


# ---------- seções ----------

def secao(chave):
    num, titulo = COPY["secoes"][chave]

    def gerar(tema):
        t = idt.TEMA[tema]
        L, A, tam = 830, 60, 32
        w_num = tx.largura(num, tam, 900, 0)
        corpo = (svg.linha(num, 2, 44, tam, t["destaque"], 900, 0)
                 + svg.linha(titulo, w_num + 14, 44, tam, t["texto"], 800, 0.005))
        return idt.svg_aberto(L, A, f"{num} {titulo.capitalize()}", "", corpo)
    return gerar


# ---------- 01. esteira de um job ----------

def esteira(tema):
    t = idt.TEMA[tema]
    L, A, cy, r = 830, 268, 64, 38
    est = COPY["esteira"]
    passo = (L - 166) / (len(est) - 1)
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
    p.append(svg.linha(COPY["esteira_rodape"], L / 2, A - 14, 13.5, t["texto"], 800, 0.04, ancora="meio"))
    css = _passo_css("anel", "X", passo, len(est), 11)
    return idt.svg_aberto(L, A, "Onde a automação entra: briefing e abertura, planejamento, pré-produção, "
                                "produção e fechamento. O trabalho humano permanece no centro.", css, "".join(p))


def esteira_celular(tema):
    t = idt.TEMA[tema]
    est = COPY["esteira"]
    L, cx, r, passo, y0 = 360, 48, 30, 92, 44
    A = y0 + passo * (len(est) - 1) + 96
    p = [f'<rect x="{cx - 1.5}" y="{y0}" width="3" height="{passo * (len(est) - 1)}" fill="{t["linha"]}"/>']
    for i, (ic, rot, desc) in enumerate(est):
        cy = y0 + i * passo
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["pagina"]}" stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, cx - 16, cy - 16, 32))
        p.append(svg.linha(rot, 96, cy - 3, 16, t["texto"], 800, 0.01))
        p.append(svg.linha(desc, 96, cy + 19, 14, t["suave"], 400))
    p.append(f'<circle class="anel" cx="{cx}" cy="{y0}" r="{r + 2}" fill="none" stroke="{t["destaque"]}" stroke-width="4.5"/>')
    for j, l in enumerate(svg.quebrar(COPY["esteira_rodape"], 14, L - 48, 800, 0.03)):
        p.append(svg.linha(l, 24, A - 40 + j * 20, 14, t["texto"], 800, 0.03))
    css = _passo_css("anel", "Y", passo, len(est), 11)
    return idt.svg_aberto(L, A, "Onde a automação entra: briefing e abertura, planejamento, pré-produção, "
                                "produção e fechamento. O trabalho humano permanece no centro.", css, "".join(p))


# ---------- 02. anatomia ----------

CICLO = ("@keyframes ciclo{0%{opacity:0}4%{opacity:1}30%{opacity:1}34%{opacity:0}100%{opacity:0}}"
         ".ex{animation:ciclo 12s infinite both}.ex1{animation-delay:4s;opacity:0}.ex2{animation-delay:8s;opacity:0}"
         "@keyframes flui{to{stroke-dashoffset:-20}}.flui{animation:flui 1s linear infinite}")


def _exemplos_coluna(col, t, cx, y_ic, y_txt, tam_ic, tam_txt, larg_txt, ancora="meio"):
    out = []
    for k, ex in enumerate(COPY["anatomia"]["exemplos"]):
        ic, rot = ex[col]
        partes = _ic(ic, t, cx - tam_ic / 2 if ancora == "meio" else cx, y_ic, tam_ic)
        for j, l in enumerate(svg.quebrar(rot, tam_txt, larg_txt, 700, 0.01)):
            partes += svg.linha(l, cx if ancora == "meio" else cx + tam_ic + 16, y_txt + j * (tam_txt + 5),
                                tam_txt, t["texto"], 700, 0.01, ancora=ancora if ancora == "meio" else "inicio")
        out.append(f'<g class="ex ex{k}">{partes}</g>')
    return "".join(out)


def anatomia(tema):
    t = idt.TEMA[tema]
    L, A, gap, y_card, h_card = 830, 236, 34, 46, 168
    larg = (L - 3 * gap - 4) / 4  # 2 px de folga em cada borda para o traço não ser cortado
    etapas = COPY["anatomia"]["etapas"]
    p = []
    for i, etapa in enumerate(etapas):
        x = 2 + i * (larg + gap)
        cx = x + larg / 2
        p.append(svg.linha(f"0{i + 1}", x, 28, 14, t["destaque"], 900, 0))
        p.append(svg.linha(etapa, x + 30, 28, svg.caber(etapa, 14, larg - 30, 800, 0.01), t["texto"], 800, 0.01))
        p.append(f'<rect x="{x}" y="{y_card}" width="{larg}" height="{h_card}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["destaque"] if i == 3 else t["linha"]}" stroke-width="{3 if i == 3 else 2}"/>')
        if i < 3:
            p.append(_exemplos_coluna(i, t, cx, y_card + 34, y_card + 124, 56, 13.5, larg - 24))
            x1, x2 = x + larg + 4, x + larg + gap - 4
            yc = y_card + h_card / 2
            p.append(f'<path class="flui" d="M{x1} {yc}H{x2}" stroke="{t["destaque"]}" stroke-width="3" '
                     f'stroke-dasharray="6 4" fill="none"/>')
        else:
            ic, rot = COPY["anatomia"]["validacao"]
            p.append(_ic(ic, t, cx - 28, y_card + 34, 56))
            for j, l in enumerate(svg.quebrar(rot, 13.5, larg - 24, 700, 0.01)):
                p.append(svg.linha(l, cx, y_card + 124 + j * 18.5, 13.5, t["texto"], 700, 0.01, ancora="meio"))
    return idt.svg_aberto(L, A, "Anatomia de uma automação: entrada, processamento, saída e validação humana.",
                          CICLO, "".join(p))


def anatomia_celular(tema):
    t = idt.TEMA[tema]
    etapas = COPY["anatomia"]["etapas"]
    L, h, gap, x = 360, 100, 30, 0
    A = len(etapas) * h + (len(etapas) - 1) * gap + 4
    p = []
    for i, etapa in enumerate(etapas):
        y = 2 + i * (h + gap)
        p.append(f'<rect x="1" y="{y}" width="{L - 2}" height="{h}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["destaque"] if i == 3 else t["linha"]}" stroke-width="{3 if i == 3 else 2}"/>')
        p.append(svg.linha(f"0{i + 1}", 20, y + 30, 14, t["destaque"], 900, 0))
        p.append(svg.linha(etapa, 50, y + 30, 14, t["texto"], 800, 0.01))
        if i < 3:
            p.append(_exemplos_coluna(i, t, 20, y + 46, y + 74, 40, 15, 260, ancora="inicio"))
            p.append(f'<path class="flui" d="M{L / 2} {y + h + 4}V{y + h + gap - 4}" stroke="{t["destaque"]}" '
                     f'stroke-width="3" stroke-dasharray="6 4" fill="none"/>')
        else:
            ic, rot = COPY["anatomia"]["validacao"]
            p.append(_ic(ic, t, 20, y + 46, 40))
            p.append(svg.linha(rot, 76, y + 74, 15, t["texto"], 700, 0.01))
    return idt.svg_aberto(L, A, "Anatomia de uma automação: entrada, processamento, saída e validação humana.",
                          CICLO, "".join(p))


# ---------- 03. do pedido à produção ----------

def arquitetura(tema):
    t = idt.TEMA[tema]
    nos = COPY["arquitetura"]
    L, A, cy, s = 830, 236, 60, 76
    passo = (L - 166) / (len(nos) - 1)
    xs = [83 + i * passo for i in range(len(nos))]
    p = [f'<rect x="{xs[0]}" y="{cy - 1.5}" width="{xs[-1] - xs[0]}" height="3" fill="{t["linha"]}"/>',
         f'<rect class="pacote" x="{xs[0] - 9}" y="{cy - 6}" width="18" height="12" rx="4" fill="{t["destaque"]}"/>']
    for x, (ic, rot, desc) in zip(xs, nos):
        p.append(f'<rect x="{x - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="18" fill="{t["pagina"]}" '
                 f'stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, x - 18, cy - 18, 36))
        p.append(svg.linha(rot, x, cy + s / 2 + 30, 15, t["texto"], 800, 0.01, ancora="meio"))
        p.append(svg.linha(desc, x, cy + s / 2 + 52, 13.5, t["suave"], 400, 0, ancora="meio"))
    p.append(svg.linha(COPY["arquitetura_rodape"], L / 2, A - 14, 13.5, t["texto"], 800, 0.04, ancora="meio"))
    dist = xs[-1] - xs[0]
    css = (f"@keyframes pacote{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}"
           f"90%{{opacity:1}}100%{{transform:translateX({dist:.0f}px);opacity:0}}}}"
           ".pacote{animation:pacote 5s cubic-bezier(.45,0,.55,1) infinite}")
    return idt.svg_aberto(L, A, "Do pedido à produção: pedido, código, esteira, produção e versão. "
                                "Tudo versionado; nada publica sem aprovação.", css, "".join(p))


def arquitetura_celular(tema):
    t = idt.TEMA[tema]
    nos = COPY["arquitetura"]
    L, cx, s, passo, y0 = 360, 48, 60, 90, 40
    A = y0 + passo * (len(nos) - 1) + 96
    p = [f'<rect x="{cx - 1.5}" y="{y0}" width="3" height="{passo * (len(nos) - 1)}" fill="{t["linha"]}"/>',
         f'<rect class="pacote" x="{cx - 6}" y="{y0 - 9}" width="12" height="18" rx="4" fill="{t["destaque"]}"/>']
    for i, (ic, rot, desc) in enumerate(nos):
        cy = y0 + i * passo
        p.append(f'<rect x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="14" fill="{t["pagina"]}" '
                 f'stroke="{t["linha"]}" stroke-width="2.5"/>')
        p.append(_ic(ic, t, cx - 15, cy - 15, 30))
        p.append(svg.linha(rot, 96, cy - 3, 16, t["texto"], 800, 0.01))
        p.append(svg.linha(desc, 96, cy + 19, 14, t["suave"], 400))
    for j, l in enumerate(svg.quebrar(COPY["arquitetura_rodape"], 14, L - 48, 800, 0.03)):
        p.append(svg.linha(l, 24, A - 40 + j * 20, 14, t["texto"], 800, 0.03))
    dist = passo * (len(nos) - 1)
    css = (f"@keyframes pacote{{0%{{transform:translateY(0);opacity:0}}6%{{opacity:1}}"
           f"90%{{opacity:1}}100%{{transform:translateY({dist:.0f}px);opacity:0}}}}"
           ".pacote{animation:pacote 5s cubic-bezier(.45,0,.55,1) infinite}")
    return idt.svg_aberto(L, A, "Do pedido à produção: pedido, código, esteira, produção e versão. "
                                "Tudo versionado; nada publica sem aprovação.", css, "".join(p))


# ---------- 04. princípios e 05. ferramentas ----------

def _blocos(itens, t, L, colunas, larg_cel, alt_cel, tam_ic, tam_txt, desenha):
    p = []
    for i, it in enumerate(itens):
        col, lin = i % colunas, i // colunas
        cx = col * larg_cel + larg_cel / 2
        y = lin * alt_cel
        p.append(desenha(it, t, cx, y, tam_ic, tam_txt))
    return "".join(p)


def _principio(it, t, cx, y, tam_ic, tam_txt):
    ic, linhas = it
    out = _ic(ic, t, cx - tam_ic / 2, y + 8, tam_ic)
    for j, l in enumerate(linhas):
        out += svg.linha(l, cx, y + tam_ic + 40 + j * (tam_txt + 5), tam_txt, t["texto"], 800, 0.01, ancora="meio")
    return out


def principios(tema):
    t = idt.TEMA[tema]
    itens = COPY["principios"]
    corpo = _blocos(itens, t, 830, 4, 830 / 4, 0, 52, 17, _principio)
    return idt.svg_aberto(830, 148, "Princípios: gente no centro, dado não achismo, versão e backup, passos curtos.",
                          "", corpo)


def principios_celular(tema):
    t = idt.TEMA[tema]
    corpo = _blocos(COPY["principios"], t, 360, 2, 180, 150, 46, 17, _principio)
    return idt.svg_aberto(360, 290, "Princípios: gente no centro, dado não achismo, versão e backup, passos curtos.",
                          "", corpo)


def _ferramenta(it, t, cx, y, tam_ic, tam_txt):
    nome, rot = it
    out = idt.simple_icon(nome, t["texto"], cx - tam_ic / 2, y + 6, tam_ic)
    linhas = svg.quebrar(rot, tam_txt, 120, 700, 0.03)
    for j, l in enumerate(linhas):
        out += svg.linha(l, cx, y + tam_ic + 30 + j * (tam_txt + 4), tam_txt, t["suave"], 700, 0.03, ancora="meio")
    return out


def stack(tema):
    t = idt.TEMA[tema]
    corpo = _blocos(COPY["stack"], t, 830, 6, 830 / 6, 0, 36, 12, _ferramenta)
    return idt.svg_aberto(830, 104, "Ferramentas: n8n, Python, Supabase, Google Workspace, GitHub Actions e Claude.",
                          "", corpo)


def stack_celular(tema):
    t = idt.TEMA[tema]
    corpo = _blocos(COPY["stack"], t, 360, 3, 120, 100, 34, 12, _ferramenta)
    return idt.svg_aberto(360, 196, "Ferramentas: n8n, Python, Supabase, Google Workspace, GitHub Actions e Claude.",
                          "", corpo)


PECAS = {
    "hero": hero, "hero-celular": hero_celular,
    "esteira": esteira, "esteira-celular": esteira_celular,
    "anatomia": anatomia, "anatomia-celular": anatomia_celular,
    "arquitetura": arquitetura, "arquitetura-celular": arquitetura_celular,
    "principios": principios, "principios-celular": principios_celular,
    "stack": stack, "stack-celular": stack_celular,
    "fechamento": fechamento, "fechamento-celular": fechamento_celular,
}


def gerar_todas(pasta: Path) -> list:
    saida = []
    for nome, fn in PECAS.items():
        saida += svg.salvar(nome, fn, pasta)
    for chave in COPY["secoes"]:
        saida += svg.salvar(chave, secao(chave), pasta)
    return saida


if __name__ == "__main__":
    import sys
    for p in gerar_todas(Path(sys.argv[1] if len(sys.argv) > 1 else "saida")):
        print(p)
