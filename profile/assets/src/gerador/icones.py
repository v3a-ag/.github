"""Ícones próprios em traço, numa caixa 64x64. `cor` = traço, `acento` = detalhe amarelo."""


def _g(conteudo: str, cor: str, x: float, y: float, escala: float) -> str:
    return (f'<g transform="translate({x} {y}) scale({escala})" fill="none" stroke="{cor}" '
            f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{conteudo}</g>')


ICONES = {
    "relogio": lambda c, a: f'<circle cx="32" cy="34" r="24"/><path d="M32 20v14l10 6"/><path d="M26 4h12" stroke="{a}"/>',
    "grade": lambda c, a: '<rect x="8" y="10" width="48" height="44" rx="4"/><path d="M8 25h48M8 40h48M24 10v44M40 10v44"/>'
                          f'<rect x="26" y="27" width="12" height="11" fill="{a}" stroke="none"/>',
    "grafico": lambda c, a: f'<path d="M8 56h48"/><path d="M16 46V32M30 46V20M44 46V28"/><path d="M14 18l14-8 14 8 10-6" stroke="{a}"/>',
    "slide": lambda c, a: f'<rect x="6" y="10" width="52" height="36" rx="4"/><path d="M32 46v10M22 56h20"/><path d="M14 22h22M14 32h14" stroke="{a}"/>',
    "faisca": lambda c, a: f'<path d="M28 6c2 12 6 16 18 18-12 2-16 6-18 18-2-12-6-16-18-18 12-2 16-6 18-18z"/><circle cx="50" cy="50" r="6" fill="{a}" stroke="none"/>',
    "escudo": lambda c, a: f'<path d="M32 6l22 8v16c0 14-10 24-22 28C20 54 10 44 10 30V14z"/><path d="M22 32l7 7 14-14" stroke="{a}"/>',
    "alvo": lambda c, a: f'<circle cx="32" cy="32" r="24"/><circle cx="32" cy="32" r="13"/><circle cx="32" cy="32" r="4" fill="{a}" stroke="none"/>',
    "passos": lambda c, a: f'<path d="M8 52h14V40h14V28h14V14"/><circle cx="50" cy="12" r="5" fill="{a}" stroke="none"/>',
    "pessoa": lambda c, a: f'<circle cx="32" cy="20" r="10"/><path d="M12 56c2-12 10-18 20-18s18 6 20 18"/><path d="M44 8l6-4" stroke="{a}"/>',
    "camadas": lambda c, a: f'<path d="M32 8l24 12-24 12L8 20z"/><path d="M8 32l24 12 24-12"/><path d="M8 44l24 12 24-12" stroke="{a}"/>',
    "balao": lambda c, a: f'<path d="M10 12h44v30H30l-12 10V42h-8z"/><path d="M20 24h24M20 32h14" stroke="{a}"/>',
    "lapis": lambda c, a: f'<path d="M12 52l4-14 30-30 10 10-30 30z"/><path d="M40 14l10 10" stroke="{a}"/>',
    "foguete": lambda c, a: f'<path d="M32 6c10 8 14 20 10 34H22C18 26 22 14 32 6z"/><circle cx="32" cy="24" r="5"/><path d="M26 46l-4 10M38 46l4 10" stroke="{a}"/>',
    "time": lambda c, a: f'<circle cx="22" cy="22" r="8"/><circle cx="44" cy="22" r="8"/><path d="M6 54c2-10 8-14 16-14s14 4 16 14"/><path d="M34 44c3-3 6-4 10-4 8 0 14 4 16 14" stroke="{a}"/>',
    "seta": lambda c, a: '<path d="M14 32h36M38 20l12 12-12 12"/>',
    "pdf": lambda c, a: f'<path d="M14 6h26l12 12v40H14z"/><path d="M40 6v12h12"/><path d="M22 36h20M22 46h14" stroke="{a}"/>',
    "aranha": lambda c, a: f'<circle cx="32" cy="32" r="24"/><path d="M8 32h48M32 8c-8 8-8 40 0 48M32 8c8 8 8 40 0 48"/><circle cx="48" cy="48" r="6" fill="{a}" stroke="none"/>',
}


def icone(nome: str, cor: str, acento: str, x: float = 0, y: float = 0, tamanho: float = 64) -> str:
    return _g(ICONES[nome](cor, acento), cor, x, y, tamanho / 64)
