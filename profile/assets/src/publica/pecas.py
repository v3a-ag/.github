"""Peças da página pública (v3a-ag/.github/profile) — identidade não institucional, v2.

Narrativa para talento/candidato: hero (promessa) → o que você faria aqui → como a gente trabalha
→ no que a gente acredita → com o que a gente constrói → chamada. Sem números de escala e sem
nome de automação.
"""
from pathlib import Path

from gerador import identidade as idt
from gerador import svg
from gerador import texto as tx

COPY = {
    "hero": {"titulo": ["TEMPO INTELIGENTE É", "EXPERIÊNCIA", "DE MARCA"],
             "assinatura": ["EXPERIÊNCIA", "DE MARCA", "É V3A."]},
    "secoes": {
        "secao-01": ("01.", "O QUE VOCÊ FARIA AQUI"),
        "secao-02": ("02.", "COMO A GENTE TRABALHA"),
        "secao-03": ("03.", "NO QUE A GENTE ACREDITA"),
        "secao-04": ("04.", "COM O QUE A GENTE CONSTRÓI"),
    },
    "metodo": ["ESCUTA", "DESENHO", "AUTOMAÇÃO", "EVOLUÇÃO"],
    "fechamento": {"titulo": ["QUER CONSTRUIR", "ISSO COM", "A GENTE?"],
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


def _titulo(linhas, x, y0, passo, tam, cor):
    pesos = [400, 800, 800]
    return "".join(f'<g class="l l{i}">' + svg.linha(t, x, y0 + i * passo, tam, cor, pesos[i], 0.005) + "</g>"
                   for i, t in enumerate(linhas))


def _assinatura(linhas, x, y0, passo, tam, cor, classe="ass"):
    cls = f' class="{classe}"' if classe else ""
    return (f"<g{cls}>" + "".join(
        svg.linha(t, x, y0 + i * passo, tam, cor, 800 if i == len(linhas) - 1 else 400, 0.005)
        for i, t in enumerate(linhas)) + "</g>")


def hero(tema: str) -> str:
    """830×226 — mock do Igor: esquerda livre (vídeo/GIF em loop no futuro), texto à direita."""
    t = idt.TEMA[tema]
    L, A, x = 830, 226, 458
    c = COPY["hero"]
    corpo = (idt.fundo(L, A, tema)
             + idt.monograma(34, 24, 48, t["logo"], "logo")
             + _titulo(c["titulo"], x, 47, 33, 25.5, t["texto"])
             + _assinatura(c["assinatura"], x - 2, 165, 21, 16.4, t["texto"])
             + f'<g transform="translate(0 196)">{idt.grafismo(618, 0, 157, t["logo"], "graf")}</g>')
    return idt.svg_aberto(L, A, "Tempo inteligente é experiência de marca. Experiência de marca é V3A.",
                          ENTRADA, corpo)


def hero_celular(tema: str) -> str:
    """360×320 — mesma composição empilhada, letra maior para tela estreita."""
    t = idt.TEMA[tema]
    L, A, x = 360, 320, 24
    c = COPY["hero"]
    lg = 140
    corpo = (idt.fundo(L, A, tema)
             + idt.monograma(x, 24, 36, t["logo"], "logo")
             + _titulo(c["titulo"], x, 112, 38, 24, t["texto"])
             + _assinatura(c["assinatura"], x, 226, 19, 14.5, t["texto"])
             + f'<g transform="translate(0 {A - 28 - lg / idt.RAZAO_GRAFISMO:.1f})">'
               f'{idt.grafismo(L - 24 - lg, 0, lg, t["logo"], "graf")}</g>')
    return idt.svg_aberto(L, A, "Tempo inteligente é experiência de marca. Experiência de marca é V3A.",
                          ENTRADA, corpo)


def secao(chave: str):
    num, titulo = COPY["secoes"][chave]

    def gerar(tema: str) -> str:
        t = idt.TEMA[tema]
        L, A, tam = 830, 60, 32
        w_num = tx.largura(num, tam, 900, 0)
        corpo = (svg.linha(num, 2, 44, tam, t["destaque"], 900, 0)
                 + svg.linha(titulo, w_num + 14, 44, tam, t["texto"], 800, 0.005))
        return idt.svg_aberto(L, A, f"{num} {titulo.capitalize()}", "", corpo)
    return gerar


def metodo(tema: str) -> str:
    """Quatro passos com o único loop lento da página (um ponto amarelo percorre a linha)."""
    t = idt.TEMA[tema]
    L, A, m, y = 830, 132, 80, 34
    passos = COPY["metodo"]
    xs = [m + i * (L - 2 * m) / (len(passos) - 1) for i in range(len(passos))]
    partes = [f'<rect x="{xs[0]}" y="{y - 1.5}" width="{xs[-1] - xs[0]}" height="3" rx="1.5" fill="{t["linha"]}"/>',
              f'<circle class="anda" cx="{xs[0]}" cy="{y}" r="8" fill="{t["destaque"]}"/>']
    for i, (x, rot) in enumerate(zip(xs, passos)):
        partes.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{t["destaque"]}"/>')
        partes.append(svg.linha(f"0{i + 1}", x, y + 7, 19, t["sobre_destaque"], 800, 0, ancora="meio"))
        partes.append(svg.linha(rot, x, y + 72, 25, t["texto"], 800, 0.01, ancora="meio"))
    dist = xs[-1] - xs[0]
    css = (f"@keyframes anda{{0%{{transform:translateX(0);opacity:0}}8%{{opacity:1}}"
           f"88%{{opacity:1}}100%{{transform:translateX({dist:.0f}px);opacity:0}}}}"
           ".anda{animation:anda 6s ease-in-out infinite}")
    return idt.svg_aberto(L, A, "Escuta, desenho, automação e evolução", css, "".join(partes))


def fechamento(tema: str) -> str:
    """Espelho do hero: chamada à esquerda, monograma no topo à direita, assinatura + grafismo."""
    t = idt.TEMA[tema]
    L, A, x = 830, 226, 34
    c = COPY["fechamento"]
    w_logo = idt.largura_monograma(40)
    corpo = (idt.fundo(L, A, tema)
             + idt.monograma(L - 34 - w_logo, 28, 40, t["logo"])
             + "".join(svg.linha(s, x, 70 + i * 33, 25.5, t["texto"], 400 if i == 0 else 800, 0.005)
                       for i, s in enumerate(c["titulo"]))
             + _assinatura(c["assinatura"], 458, 165, 21, 16.4, t["texto"], classe="")
             + f'<g transform="translate(0 196)">{idt.grafismo(618, 0, 157, t["logo"])}</g>')
    return idt.svg_aberto(L, A, "Quer construir isso com a gente? Experiência de marca é V3A.", "", corpo)


def gerar_todas(pasta: Path) -> list:
    saida = svg.salvar("hero", hero, pasta)
    saida += svg.salvar("hero-celular", hero_celular, pasta)
    for chave in COPY["secoes"]:
        saida += svg.salvar(chave, secao(chave), pasta)
    saida += svg.salvar("metodo", metodo, pasta)
    saida += svg.salvar("fechamento", fechamento, pasta)
    return saida


if __name__ == "__main__":
    import sys
    for p in gerar_todas(Path(sys.argv[1] if len(sys.argv) > 1 else "saida")):
        print(p)
