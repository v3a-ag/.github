#!/usr/bin/env python3
"""Valida a ficha v3a-projeto.yml contra o esquema da esteira.

Uso (no workflow, depois de `yq -o=json . v3a-projeto.yml > ficha.json`):

    python3 validar_ficha.py --repositorio <nome-do-repo> ficha.json

Saída 0: ficha válida. Saída 1: ficha recusada (cada problema sai como
anotação `::error` do Actions). Só biblioteca padrão.

Regras, nesta ordem:
1. nenhum campo de infraestrutura em lugar nenhum da ficha (rede, sub-rede,
   alias, porta, mount, label, privilégio...) e nenhum valor com docker.sock;
2. o esquema esquema/v3a-projeto.schema.json (campos conhecidos, tipos, limites);
3. política: chave igual ao nome do repositório; exposição de máquina
   bloqueada até a P-18.
"""

import argparse
import json
import os
import re
import sys

ESQUEMA_PADRAO = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "esquema",
    "v3a-projeto.schema.json",
)

# Comparados em minúsculas, com "-" trocado por "_".
CAMPOS_DE_INFRA = {
    "porta", "portas", "port", "ports", "expose",
    "rede", "redes", "network", "networks", "network_mode",
    "sub_rede", "sub_redes", "subrede", "subredes", "subnet", "subnets",
    "alias", "aliases",
    "mount", "mounts", "volume", "volumes", "bind", "binds", "tmpfs",
    "label", "labels", "rotulo", "rotulos",
    "privileged", "privilegiado", "cap_add", "devices", "security_opt",
    "container_name", "hostname", "ipv4_address", "ipv6_address",
    "extra_hosts", "dns", "pid", "ipc", "userns_mode", "user",
}

TIPOS = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
}


def caminho_de(base, chave):
    return chave if not base else f"{base}.{chave}"


def campo_de_infra(nome):
    return str(nome).lower().replace("-", "_") in CAMPOS_DE_INFRA


def procurar_infra(valor, base, erros):
    """Percorre a ficha inteira atrás de campos e valores proibidos."""
    if isinstance(valor, dict):
        for k, v in valor.items():
            p = caminho_de(base, k)
            if campo_de_infra(k):
                erros.append(
                    f"{p}: campo de infraestrutura proibido na ficha "
                    f"(rede, sub-rede, alias, porta, mount e label são do modelo do bloco)"
                )
            procurar_infra(v, p, erros)
    elif isinstance(valor, list):
        for i, v in enumerate(valor):
            procurar_infra(v, f"{base}[{i}]", erros)
    elif isinstance(valor, str) and "docker.sock" in valor:
        erros.append(f"{base or '(raiz)'}: valor com docker.sock é proibido")


def tipo_confere(valor, tipo):
    if tipo == "integer":
        return isinstance(valor, int) and not isinstance(valor, bool)
    if tipo == "number":
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    return isinstance(valor, TIPOS[tipo])


def validar_esquema(valor, esq, base, erros):
    """Subconjunto do JSON Schema usado pelo esquema da ficha."""
    nome = base or "(raiz)"
    if "const" in esq and valor != esq["const"]:
        erros.append(f"{nome}: precisa ser {json.dumps(esq['const'])}")
        return
    if "enum" in esq and valor not in esq["enum"]:
        aceitos = ", ".join(str(x) for x in esq["enum"])
        erros.append(f"{nome}: valor {json.dumps(valor, ensure_ascii=False)} fora da lista ({aceitos})")
        return
    tipo = esq.get("type")
    if tipo and not tipo_confere(valor, tipo):
        erros.append(f"{nome}: precisa ser do tipo {tipo}")
        return
    if isinstance(valor, str):
        if "maxLength" in esq and len(valor) > esq["maxLength"]:
            erros.append(f"{nome}: passa de {esq['maxLength']} caracteres")
        if "pattern" in esq and not re.search(esq["pattern"], valor):
            erros.append(f"{nome}: formato inválido ({valor!r})")
    if tipo in ("number", "integer"):
        if "minimum" in esq and valor < esq["minimum"]:
            erros.append(f"{nome}: menor que {esq['minimum']}")
        if "maximum" in esq and valor > esq["maximum"]:
            erros.append(f"{nome}: maior que {esq['maximum']}")
    if isinstance(valor, list):
        if esq.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in valor}) != len(valor):
            erros.append(f"{nome}: itens repetidos")
        if "items" in esq:
            for i, item in enumerate(valor):
                validar_esquema(item, esq["items"], f"{base}[{i}]", erros)
    if isinstance(valor, dict):
        props = esq.get("properties", {})
        for obrigatorio in esq.get("required", []):
            if obrigatorio not in valor:
                erros.append(f"{caminho_de(base, obrigatorio)}: campo obrigatório ausente")
        for k, v in valor.items():
            p = caminho_de(base, k)
            if k in props:
                validar_esquema(v, props[k], p, erros)
            elif esq.get("additionalProperties") is False and not campo_de_infra(k):
                erros.append(f"{p}: campo desconhecido")


def validar_politica(ficha, repositorio, erros):
    chave = ficha.get("chave")
    if isinstance(chave, str) and chave != repositorio:
        erros.append(
            f"chave: {chave!r} precisa ser igual ao nome do repositório ({repositorio!r})"
        )
    if ficha.get("exposicao") == "maquina":
        erros.append(
            "exposicao: 'maquina' fica bloqueada até a decisão do gateway de máquinas (P-18)"
        )


def validar(ficha, esquema, repositorio):
    erros = []
    if not isinstance(ficha, dict):
        return ["(raiz): a ficha precisa ser um mapa de campos (chave: valor)"]
    procurar_infra(ficha, "", erros)
    validar_esquema(ficha, esquema, "", erros)
    validar_politica(ficha, repositorio, erros)
    return erros


def anotar(msg):
    print(f"::error title=ficha v3a-projeto.yml::{msg}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ficha", help="ficha convertida para JSON")
    ap.add_argument("--repositorio", required=True, help="nome do repositório (sem a organização)")
    ap.add_argument("--esquema", default=ESQUEMA_PADRAO)
    args = ap.parse_args(argv)

    with open(args.esquema, encoding="utf-8") as f:
        esquema = json.load(f)

    if not os.path.isfile(args.ficha):
        anotar("ficha não encontrada: o repositório precisa de v3a-projeto.yml na raiz")
        print("ficha recusada")
        return 1
    try:
        with open(args.ficha, encoding="utf-8") as f:
            ficha = json.load(f)
    except (ValueError, UnicodeDecodeError) as e:
        anotar(f"ficha ilegível: {e}")
        print("ficha recusada")
        return 1

    erros = validar(ficha, esquema, args.repositorio)
    if erros:
        for e in erros:
            anotar(e)
        print(f"ficha recusada: {len(erros)} problema(s)")
        return 1
    print(f"ficha válida: chave={ficha['chave']} bloco={ficha['bloco']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
