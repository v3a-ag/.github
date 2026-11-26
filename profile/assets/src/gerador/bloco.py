"""Grade única de blocos: toda peça tem a mesma largura total e a mesma margem interna.

Desktop: área de conteúdo 830 + margem 32 de cada lado (viewBox 894).
Celular: área de conteúdo 360 + margem 20 de cada lado (viewBox 400).
Assim hero, seções e botões começam o conteúdo na mesma borda.
"""
from . import identidade as idt
from . import svg
from . import texto as tx

GRADE = {"desk": {"conteudo": 830, "margem": 32}, "cel": {"conteudo": 360, "margem": 20}}


def largura_total(modo: str) -> int:
    g = GRADE[modo]
    return g["conteudo"] + 2 * g["margem"]


def cabecalho(num: str, titulo: str, subtitulo: str, t: dict, modo: str):
    """Título da seção no estilo do manual ("01." amarelo + título) e uma linha de apoio.

    Retorna (svg, altura) em coordenadas da área de conteúdo.
    """
    W = GRADE[modo]["conteudo"]
    if modo == "desk":
        tam, tam_sub, passo_sub = 30, 15.5, 21
    else:
        tam, tam_sub, passo_sub = 22, 14.5, 20
    w_num = tx.largura(num, tam, 900, 0)
    linhas_tit = svg.quebrar(titulo, tam, W - w_num - 12, 800, 0.005)
    partes = [svg.linha(num, 0, tam, tam, t["destaque"], 900, 0)]
    y = tam
    for i, l in enumerate(linhas_tit):
        partes.append(svg.linha(l, w_num + 12, y, tam, t["texto"], 800, 0.005))
        y += tam * 1.18 if i < len(linhas_tit) - 1 else 0
    if subtitulo:
        y += tam_sub + 14
        for i, l in enumerate(svg.quebrar(subtitulo, tam_sub, W, 400)):
            partes.append(svg.linha(l, 0, y + i * passo_sub, tam_sub, t["suave"], 400))
        y += (len(svg.quebrar(subtitulo, tam_sub, W, 400)) - 1) * passo_sub
    return "".join(partes), y


def bloco(tema: str, modo: str, alt: str, corpo: str, altura: int, css: str = "",
          cab: tuple = None, respiro: int = 28) -> str:
    """Peça completa: fundo próprio + margem da grade + (cabeçalho opcional) + corpo."""
    t = idt.TEMA[tema]
    g = GRADE[modo]
    conteudo = corpo
    h_cab = 0
    if cab:
        num, titulo, subtitulo = cab
        svg_cab, h = cabecalho(num, titulo, subtitulo, t, modo)
        h_cab = h + (respiro if corpo else 0)
        conteudo = svg_cab + (f'<g transform="translate(0 {h_cab:.1f})">{corpo}</g>' if corpo else "")
    return idt.svg_aberto(g["conteudo"], int(h_cab + altura), alt, css, conteudo, tema, g["margem"])
