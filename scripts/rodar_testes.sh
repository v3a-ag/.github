#!/usr/bin/env bash
# Roda os testes do projeto: cada testes/*.sh, em ordem alfabética, na raiz
# do repositório. Para no primeiro que falha (TA-02: sem imagem, sem deployment).
# Uso: rodar_testes.sh <raiz-do-repositorio>
set -uo pipefail
raiz="${1:?uso: rodar_testes.sh <raiz-do-repositorio>}"
cd "$raiz" || exit 1

shopt -s nullglob
testes=(testes/*.sh)
if [ "${#testes[@]}" -eq 0 ]; then
  echo "nenhum teste do projeto em testes/*.sh (só a verificação do bloco)"
  exit 0
fi

for t in "${testes[@]}"; do
  echo "::group::teste $t"
  bash "$t"
  codigo=$?
  echo "::endgroup::"
  if [ "$codigo" -ne 0 ]; then
    echo "::error title=testes do projeto::$t falhou (saída $codigo); a esteira para aqui, sem imagem e sem deployment"
    exit 1
  fi
done
echo "${#testes[@]} teste(s) passaram"
