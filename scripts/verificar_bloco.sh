#!/usr/bin/env bash
# Verificação própria de cada bloco, antes dos testes do projeto.
# Uso: verificar_bloco.sh <bloco> <raiz-do-repositorio>
set -uo pipefail
bloco="${1:?uso: verificar_bloco.sh <bloco> <raiz>}"
raiz="${2:?uso: verificar_bloco.sh <bloco> <raiz>}"

erro() { echo "::error title=bloco $bloco::$1"; exit 1; }

case "$bloco" in
  pagina_web_simples)
    [ -f "$raiz/index.html" ] || erro "a página precisa de index.html na raiz do repositório"
    [ -s "$raiz/index.html" ] || erro "index.html está vazio"
    grep -qiE '<(!doctype html|html|head|body|title)' "$raiz/index.html" \
      || erro "index.html não tem marcação HTML (doctype, html, head, body ou title)"
    [ ! -e "$raiz/cgi-bin" ] || erro "cgi-bin não é permitido: a página só serve arquivos estáticos"
    echo "bloco pagina_web_simples: index.html conferido"
    ;;
  *)
    erro "bloco desconhecido: $bloco"
    ;;
esac
