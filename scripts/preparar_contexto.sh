#!/usr/bin/env bash
# Monta o contexto de build da imagem a partir do modelo do bloco.
# O Dockerfile é sempre o padrão do bloco; o do repositório, se houver, é ignorado.
#   <destino>/Dockerfile        modelo do bloco (blocos/<bloco>/Dockerfile)
#   <destino>/v3a-projeto.yml   ficha (vai para /v3a/ dentro da imagem)
#   <destino>/site/             arquivos da página, sem os de repositório
# Uso: preparar_contexto.sh <bloco> <raiz-do-repositorio> <destino>
set -euo pipefail
bloco="${1:?uso: preparar_contexto.sh <bloco> <raiz> <destino>}"
raiz="${2:?}"
destino="${3:?}"
aqui="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$bloco" in
  pagina_web_simples) modelo="$aqui/../blocos/pagina-web-simples" ;;
  *) echo "::error title=bloco $bloco::bloco sem modelo de imagem"; exit 1 ;;
esac

rm -rf "$destino"
mkdir -p "$destino/site"
cp "$modelo/Dockerfile" "$destino/Dockerfile"
cp "$raiz/v3a-projeto.yml" "$destino/v3a-projeto.yml"
# Sem links simbólicos e sem arquivos ocultos (.env, .git...) em lugar nenhum.
rsync -rt --no-links \
  --exclude='.*' \
  --exclude='/testes' --exclude='/docs' \
  --exclude='/README*' --exclude='/LICENSE*' \
  --exclude='/v3a-projeto.yml' --exclude='/Dockerfile' \
  "$raiz"/ "$destino/site/"
echo "contexto do bloco $bloco montado em $destino ($(find "$destino/site" -type f | wc -l | tr -d ' ') arquivo(s) da página)"
