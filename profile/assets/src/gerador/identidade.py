"""Identidade NÃO institucional da V3A: monograma de uma cor + grafismo na mesma cor.

Pares do Drive (pasta 1x): claro = monograma/grafismo amarelos sobre branco (sem moldura);
escuro = monograma/grafismo brancos sobre bloco cinza escuro.
"""
import re
from functools import lru_cache

from .marca import CORES, RECURSOS

TEMA = {
    "claro": {"bloco": CORES["branco"], "logo": CORES["amarelo"], "texto": CORES["preto"],
              "suave": CORES["cinza_escuro"], "destaque": CORES["amarelo"], "linha": CORES["cinza_claro"],
              "sobre_destaque": CORES["preto"], "pagina": "#FFFFFF"},
    "escuro": {"bloco": CORES["cinza_escuro"], "logo": CORES["branco"], "texto": CORES["branco"],
               "suave": CORES["nuvem"], "destaque": CORES["amarelo"], "linha": CORES["cinza_claro"],
               "sobre_destaque": CORES["preto"], "pagina": CORES["cinza_escuro"]},
}

# Grafismo: recortes dos traços do monograma (proporções de "Elementos Gráficos-01"),
# coordenadas normalizadas numa faixa de razão 11,2 : 1.
RAZAO_GRAFISMO = 11.2
GRAFISMO = [
    [(0.000, 0), (0.118, 0), (0.192, 1), (0.075, 1)],
    [(0.225, 0), (0.315, 0), (0.315, 1), (0.225, 1)],
    [(0.572, 0), (0.711, 0), (0.607, 1), (0.469, 1)],
    [(0.759, 0), (0.924, 0), (1.000, 1), (0.879, 1), (0.848, 0.54), (0.848, 1), (0.759, 1)],
]


def grafismo(x: float, y: float, largura: float, cor: str, classe: str = "", pecas: bool = False) -> str:
    """Faixa do grafismo com canto superior esquerdo em (x, y). Altura = largura / 11,2.

    `pecas=True` dá a cada recorte a classe gp0..gp3 (para subirem um de cada vez).
    """
    altura = largura / RAZAO_GRAFISMO
    cls = f' class="{classe}"' if classe else ""
    polis = "".join(
        (f'<polygon class="gp{i}" points="' if pecas else '<polygon points="')
        + " ".join(f"{x + px * largura:.1f},{y + py * altura:.1f}" for px, py in p) + '"/>'
        for i, p in enumerate(GRAFISMO))
    return f'<g{cls} fill="{cor}">{polis}</g>'


@lru_cache(maxsize=1)
def _monograma():
    bruto = (RECURSOS / "logo-monograma.svg").read_text(encoding="utf-8")
    return re.findall(r'<path d="([^"]+)" fill="var\(--fill-0, #626366\)"', bruto)


# caixa do monograma dentro do SVG oficial (x0, y0, largura, altura)
CAIXA_MONOGRAMA = (72.9999, 162.0, 278.0, 139.007)


def largura_monograma(altura: float) -> float:
    return CAIXA_MONOGRAMA[2] * altura / CAIXA_MONOGRAMA[3]


def monograma(x: float, y: float, altura: float, cor: str, classe: str = "") -> str:
    """Monograma V3A de uma cor; o posicionamento fica no <g> externo e a classe no interno."""
    x0, y0, _, h = CAIXA_MONOGRAMA
    esc = altura / h
    cls = f' class="{classe}"' if classe else ""
    paths = "".join(f'<path d="{d}"/>' for d in _monograma())
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({esc:.4f}) translate({-x0} {-y0})">'
            f'<g{cls} fill="{cor}">{paths}</g></g>')


def fundo(largura: int, altura: int, tema: str, raio: int = 12) -> str:
    """Toda peça traz o próprio fundo: claro = branco, escuro = cinza escuro #636466.

    O <picture> do GitHub escolhe a versão pelo tema do SISTEMA, não pelo do GitHub; sem fundo próprio,
    a versão escura cai em página branca (e vice-versa) e o texto some (bug de 25/11/2026).
    """
    return f'<rect width="{largura}" height="{altura}" rx="{raio}" fill="{TEMA[tema]["bloco"]}"/>'


def svg_aberto(largura: int, altura: int, titulo: str, css: str, corpo: str,
               tema: str = None, margem: int = 0) -> str:
    """Com `tema`, embrulha o corpo num bloco de fundo próprio com `margem` interna."""
    from html import escape
    from .svg import SEM_MOVIMENTO
    if tema:
        largura, altura = largura + 2 * margem, altura + 2 * margem
        corpo = fundo(largura, altura, tema) + f'<g transform="translate({margem} {margem})">{corpo}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" '
            f'width="{largura}" height="{altura}" role="img"><title>{escape(titulo)}</title>'
            f'<style>{css}{SEM_MOVIMENTO}</style>{corpo}</svg>')


def simple_icon(nome: str, cor: str, x: float, y: float, tam: float, classe: str = "") -> str:
    """Ícone de marca (Simple Icons, CC0) de uma cor, numa caixa tam×tam."""
    bruto = (RECURSOS / "icones" / f"{nome}.svg").read_text(encoding="utf-8")
    d = re.search(r'<path d="([^"]+)"', bruto).group(1)
    cls = f' class="{classe}"' if classe else ""
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({tam / 24:.4f})">'
            f'<path{cls} d="{d}" fill="{cor}"/></g>')
