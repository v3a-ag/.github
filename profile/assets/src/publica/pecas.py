"""Peças SVG da página pública (v3a-ag/.github/profile). Sem números, sem automação específica."""
from pathlib import Path

from gerador import marca, svg
from gerador.icones import icone

COPY = {
    "banner": {
        "titulo": "Automação & IA",
        "linhas": ["Tirar o repetitivo do caminho.", "Devolver tempo para criar experiência."],
    },
    "cards": {
        "card-horas": ("relogio", "De horas para minutos",
                       "O que tomava a tarde inteira agora roda sozinho, enquanto o time cuida do que importa."),
        "card-planilha": ("grade", "Planilha que se preenche",
                          "O dado chega onde precisa, sem copiar e colar e sem retrabalho."),
        "card-painel": ("grafico", "Dado espalhado vira painel",
                        "Informação de várias fontes num lugar só, sempre atualizada."),
        "card-relatorio": ("slide", "Relatório pronto, no padrão",
                           "Slides e PDFs gerados no formato da casa, prontos para enviar."),
        "card-ia": ("faisca", "IA com gente no controle",
                    "A IA sugere; a pessoa revisa e aprova antes de qualquer coisa sair."),
        "card-durar": ("escudo", "Feito para durar",
                       "Versionado, com backup e padrão. Nada de script solto num canto."),
    },
    "trabalho": {
        "titulo": "Como a gente trabalha",
        "itens": [
            ("alvo", "Começa pelo problema", "Primeiro entender a rotina da área. A ferramenta vem depois."),
            ("passos", "Passos curtos", "Entrega pequena, usada cedo e melhorada com quem usa."),
            ("pessoa", "Gente decide", "O que importa passa por aprovação humana."),
            ("camadas", "Padrão em tudo", "Versão, backup e documentação desde o começo."),
        ],
    },
    "fechamento": {"frase": "Experiência de marca é V3A.", "assinatura": "It's We."},
}

TRACK = -0.02  # manual: títulos com -2%


def banner(tema: str) -> str:
    t = marca.TEMAS[tema]
    L, A = 1600, 440
    logo, (lw, lh) = marca.logo_paths("institucional", tema)
    esc = 230 / lh
    x_txt = 96 + lw * esc + 96
    c = COPY["banner"]
    tam = svg.caber(c["titulo"], 104, L - x_txt - 96, 900, TRACK)
    corpo = (
        f'<g transform="translate(96 {(A - lh * esc) / 2:.1f}) scale({esc:.4f})"><g class="logo">{logo}</g></g>'
        f'<rect x="{x_txt - 48}" y="96" width="4" height="248" rx="2" fill="{t["borda"]}" opacity=".6"/>'
        + svg.linha(c["titulo"], x_txt, 214, tam, t["texto"], 900, TRACK, "titulo")
        + f'<rect class="barra" x="{x_txt}" y="244" width="180" height="10" rx="5" fill="{t["acento"]}"/>'
        + svg.paragrafo(c["linhas"], x_txt, 308, 36, t["texto_suave"], 400, 1.3, classe="sub")
    )
    css = (
        "@keyframes entra{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
        "@keyframes barra{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".logo{animation:entra .6s ease-out both}"
        ".titulo{animation:entra .7s .15s ease-out both}"
        ".sub{animation:entra .7s .35s ease-out both}"
        f".barra{{transform-origin:{x_txt}px 249px;animation:barra .8s .6s cubic-bezier(.2,.7,.2,1) both}}"
    )
    return svg.peca(L, A, corpo, tema, css, "V3A · Automação & IA")


RESPIRA = ("@keyframes respira{0%,100%{opacity:.35}50%{opacity:1}}"
           ".respira{animation:respira 3.2s ease-in-out infinite}")


def card(nome: str):
    ic, titulo, texto = COPY["cards"][nome]

    def gerar(tema: str) -> str:
        t = marca.TEMAS[tema]
        L, A, m = 780, 300, 56
        tam = svg.caber(titulo, 44, L - 2 * m, 800, TRACK)
        linhas = svg.quebrar(texto, 27, L - 2 * m)
        corpo = (
            icone(ic, t["texto"], t["acento"], m, 44, 64)
            + f'<rect class="respira" x="{m + 84}" y="74" width="64" height="6" rx="3" fill="{t["acento"]}"/>'
            + svg.linha(titulo, m, 172, tam, t["texto"], 800, TRACK)
            + svg.paragrafo(linhas, m, 218, 27, t["texto_suave"], 400, 1.35)
        )
        return svg.peca(L, A, corpo, tema, RESPIRA, titulo)

    return gerar


def icone_item(nome: str):
    """Ícone pequeno, sem fundo, para a lista "Como a gente trabalha" (texto fica no README)."""
    def gerar(tema: str) -> str:
        t = marca.TEMAS[tema]
        return svg.peca(96, 96, icone(nome, t["texto"], t["acento"], 8, 8, 80), tema, "", nome, fundo=False)
    return gerar


def fechamento(tema: str) -> str:
    t = marca.TEMAS[tema]
    L, A = 1600, 360
    from gerador import texto as tx
    a, b, c_ = "Experiência de marca é V", "3", "A."
    tam = 84
    wa, wb, wc = (tx.largura(s, tam, 900, TRACK) for s in (a, b, c_))
    tr = TRACK * tam
    total = wa + tr + wb + tr + wc
    x0 = (L - total) / 2
    corpo = (
        svg.linha(a, x0, 190, tam, t["texto"], 900, TRACK)
        + svg.linha(b, x0 + wa + tr, 190, tam, t["acento"], 900, TRACK)
        + svg.linha(c_, x0 + wa + tr + wb + tr, 190, tam, t["texto"], 900, TRACK)
        + f'<rect class="respira" x="{L / 2 - 60}" y="226" width="120" height="8" rx="4" fill="{t["acento"]}"/>'
        + svg.linha(COPY["fechamento"]["assinatura"], L / 2, 300, 40, t["texto_suave"], 400, 0, ancora="meio")
    )
    return svg.peca(L, A, corpo, tema, RESPIRA, COPY["fechamento"]["frase"])


def gerar_todas(pasta: Path) -> list:
    saida = svg.salvar("banner", banner, pasta)
    for nome in COPY["cards"]:
        saida += svg.salvar(nome, card(nome), pasta)
    for ic, _, _ in COPY["trabalho"]["itens"]:
        saida += svg.salvar(f"ic-{ic}", icone_item(ic), pasta)
    saida += svg.salvar("fechamento", fechamento, pasta)
    return saida


if __name__ == "__main__":
    import sys
    for p in gerar_todas(Path(sys.argv[1] if len(sys.argv) > 1 else "saida")):
        print(p)
