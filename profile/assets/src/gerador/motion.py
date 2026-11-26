"""Linguagem de movimento única para todas as peças.

Princípios: entrar com ease-out longo (sensação de "assentar"), deslocar com ease-in-out (sem tranco),
toda troca com fade cruzado, pausas longas o bastante para ler. Nada linear, exceto o fluxo tracejado.
Tudo respeita prefers-reduced-motion (o estado de repouso é sempre o legível).
"""

EASE_OUT = "cubic-bezier(.22,1,.36,1)"      # easeOutQuint: entra rápido e assenta devagar
EASE_IN_OUT = "cubic-bezier(.65,0,.35,1)"   # easeInOutCubic: desloca sem tranco
EASE_IN = "cubic-bezier(.55,0,1,.45)"       # easeInCubic: sai acelerando

DY = 14  # deslocamento vertical das entradas/saídas (px do viewBox)


def entrada_hero(atraso: float = 0.1) -> str:
    """Logo assenta, título sobe linha a linha, assinatura aparece, grafismo sobe peça por peça."""
    a = atraso
    return (
        f"@keyframes entra{{from{{opacity:0;transform:translateY({DY}px)}}to{{opacity:1;transform:none}}}}"
        "@keyframes assenta{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}"
        "@keyframes aparece{from{opacity:0}to{opacity:1}}"
        "@keyframes ergue{from{opacity:0;transform:translateY(100%)}to{opacity:1;transform:none}}"
        f".logo{{transform-box:fill-box;transform-origin:center;animation:assenta 1s {a:.2f}s {EASE_OUT} both}}"
        f".l{{animation:entra .9s {EASE_OUT} both}}"
        f".l0{{animation-delay:{a + .15:.2f}s}}.l1{{animation-delay:{a + .27:.2f}s}}.l2{{animation-delay:{a + .39:.2f}s}}"
        f".ass{{animation:aparece .9s {a + .75:.2f}s {EASE_OUT} both}}"
        + "".join(f".gp{i}{{transform-box:fill-box;animation:ergue .8s {a + .95 + i * .08:.2f}s {EASE_OUT} both}}"
                  for i in range(4))
    )


def palavras(n: int, larguras: list, inicio: float = 2.8, slot: float = 2.8, sai: float = .35,
             entra_ini: float = .3, entra_fim: float = .85, atraso_entrada: float = .25) -> str:
    """Troca do 'X' em sequência (texto não pode cruzar: vira borrão): a palavra que sai sobe e some
    em `sai` s; a nova sobe e aparece entre `entra_ini` e `entra_fim`; o 'É' desliza no meio da troca.

    A palavra 0 entra com o hero, fica até `inicio` e o ciclo segue a ordem 1..n-1, 0.
    `larguras[k]` = deslocamento do 'É' para a palavra k (relativo à palavra 0).
    """
    P = n * slot

    def pc(seg):
        return f"{seg / P * 100:.3f}%"

    kf = (f"@keyframes palavra{{"
          f"0%,{pc(entra_ini)}{{opacity:0;transform:translateY({DY}px);animation-timing-function:{EASE_OUT}}}"
          f"{pc(entra_fim)}{{opacity:1;transform:none}}"
          f"{pc(slot)}{{opacity:1;transform:none;animation-timing-function:{EASE_IN}}}"
          f"{pc(slot + sai)},100%{{opacity:0;transform:translateY(-{DY * .7:.0f}px)}}}}"
          f"@keyframes sai{{from{{opacity:1;transform:none}}to{{opacity:0;transform:translateY(-{DY * .7:.0f}px)}}}}")
    regras = [".pal{opacity:0}.pal0{opacity:1}",
              f".pal0{{animation:entra .9s {atraso_entrada:.2f}s {EASE_OUT} both,"
              f"sai {sai:.2f}s {inicio:.2f}s {EASE_IN} forwards,"
              f"palavra {P:.2f}s {inicio + (n - 1) * slot:.2f}s infinite}}"]
    for k in range(1, n):
        regras.append(f".pal{k}{{animation:palavra {P:.2f}s {inicio + (k - 1) * slot:.2f}s infinite}}")
    # 'É' desliza no meio da troca: posição da palavra visível em cada slot (ordem 1..n-1, 0)
    ordem = list(range(1, n)) + [0]
    quadros = ["0%{transform:translateX(0)}"]
    anterior = 0.0
    for j, k in enumerate(ordem):
        base = j * slot
        quadros.append(f"{pc(base + .15)}{{transform:translateX({anterior:.1f}px);animation-timing-function:{EASE_IN_OUT}}}")
        quadros.append(f"{pc(base + .75)}{{transform:translateX({larguras[k]:.1f}px)}}")
        anterior = larguras[k]
    quadros.append("100%{transform:translateX(0)}")
    regras.append("@keyframes desliza{" + "".join(quadros) + "}")
    regras.append(f".e{{animation:entra .9s {atraso_entrada:.2f}s {EASE_OUT} both,"
                  f"desliza {P:.2f}s {inicio:.2f}s infinite}}")
    return kf + "".join(regras)


def passos(nome: str, eixo: str, passo: float, n: int, slot: float = 2.2, viagem: float = .75,
           pop: bool = True) -> str:
    """Um marcador que viaja de parada em parada (ease-in-out), com um leve 'pop' ao chegar
    e fade no recomeço (nunca volta deslizando para o início)."""
    P = n * slot
    q = []

    def tr(i, s=1):
        sc = f" scale({s})" if pop else ""
        return f"translate{eixo}({i * passo:.1f}px){sc}"

    q.append(f"0%{{opacity:0;transform:{tr(0, .8)};animation-timing-function:{EASE_OUT}}}")
    q.append(f"{.5 / P * 100:.3f}%{{opacity:1;transform:{tr(0)}}}")
    for i in range(n):
        chega = (i * slot + (viagem if i else .5)) / P * 100
        if i:
            parte = (i * slot) / P * 100
            q.append(f"{parte:.3f}%{{opacity:1;transform:{tr(i - 1)};animation-timing-function:{EASE_IN_OUT}}}")
            q.append(f"{chega:.3f}%{{opacity:1;transform:{tr(i, 1.12 if pop else 1)};animation-timing-function:{EASE_OUT}}}")
            q.append(f"{chega + .35 / P * 100:.3f}%{{opacity:1;transform:{tr(i)}}}")
    q.append(f"{(P - .45) / P * 100:.3f}%{{opacity:1;transform:{tr(n - 1)};animation-timing-function:{EASE_IN}}}")
    q.append(f"100%{{opacity:0;transform:{tr(n - 1, .9)}}}")
    return (f"@keyframes {nome}{{{''.join(q)}}}"
            f".{nome}{{transform-box:fill-box;transform-origin:center;animation:{nome} {P:.2f}s infinite}}")


def ciclo(n: int, slot: float = 3.2, sai: float = .35, entra_ini: float = .3, entra_fim: float = .85,
          classe: str = "ex") -> str:
    """Troca em sequência entre n variações empilhadas (mesma lógica das palavras do hero: sai, depois
    entra; nunca cruza). A 0 já começa visível no carregamento (atraso negativo)."""
    P = n * slot

    def pc(seg):
        return f"{seg / P * 100:.3f}%"

    kf = (f"@keyframes ciclo{{0%,{pc(entra_ini)}{{opacity:0;transform:translateY(10px);animation-timing-function:{EASE_OUT}}}"
          f"{pc(entra_fim)}{{opacity:1;transform:none}}"
          f"{pc(slot)}{{opacity:1;transform:none;animation-timing-function:{EASE_IN}}}"
          f"{pc(slot + sai)},100%{{opacity:0;transform:translateY(-8px)}}}}")
    regras = [f".{classe}{{animation:ciclo {P:.2f}s infinite}}"]
    for k in range(n):
        regras.append(f".{classe}{k}{{animation-delay:{k * slot - entra_fim:.2f}s;{'opacity:0' if k else ''}}}")
    return kf + "".join(regras)


def fluxo(duracao: float = 1.8) -> str:
    return f"@keyframes flui{{to{{stroke-dashoffset:-20}}}}.flui{{animation:flui {duracao}s linear infinite}}"


def barras(n: int, enche: float = 1.1, pausa: float = .5, segura: float = 1.6, some: float = .6) -> str:
    """Pedaços enchem um de cada vez (ease-out), seguram cheios e somem juntos em fade."""
    P = n * (enche + pausa) + segura + some
    regras = []
    for i in range(n):
        ini = i * (enche + pausa) / P * 100
        fim = (i * (enche + pausa) + enche) / P * 100
        sai = (P - some) / P * 100
        regras.append(
            f"@keyframes enche{i}{{0%,{ini:.3f}%{{opacity:1;transform:scaleX(0);animation-timing-function:{EASE_OUT}}}"
            f"{fim:.3f}%,{sai:.3f}%{{opacity:1;transform:scaleX(1);animation-timing-function:{EASE_IN_OUT}}}"
            f"100%{{opacity:0;transform:scaleX(1)}}}}"
            f".enche{i}{{animation:enche{i} {P:.2f}s infinite}}")
    return "".join(regras)
