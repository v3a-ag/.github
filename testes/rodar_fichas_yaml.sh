#!/usr/bin/env bash
# Converte cada ficha YAML de testes/fichas/ com o yq (como a esteira faz)
# e confere o resultado: valida-* precisa passar, recusa-* precisa ser recusada.
set -uo pipefail
cd "$(dirname "$0")/.."
falhas=0
for f in testes/fichas/*.yml; do
  nome="$(basename "$f")"
  json="$(mktemp)"
  yq -o=json '.' "$f" > "$json" 2>/dev/null
  python3 scripts/validar_ficha.py --repositorio N1-exemplo-pagina "$json" > /dev/null
  codigo=$?
  rm -f "$json"
  case "$nome" in
    valida-*) esperado=0 ;;
    *) esperado=1 ;;
  esac
  if [ "$codigo" -eq "$esperado" ]; then
    echo "ok   $nome (saída $codigo)"
  else
    echo "::error::$nome: esperado $esperado, veio $codigo"
    falhas=$((falhas + 1))
  fi
done
exit "$falhas"
