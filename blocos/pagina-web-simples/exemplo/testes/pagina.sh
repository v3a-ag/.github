#!/usr/bin/env bash
# Teste de exemplo: roda na raiz do repositório; saída diferente de 0 para a esteira.
set -euo pipefail
grep -q '<title>' index.html
