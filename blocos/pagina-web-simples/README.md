# Bloco Página web simples

Site estático (HTML, CSS, JS, imagens) servido por um servidor web mínimo, sem root e só leitura, atrás do login da organização.

## O que o repositório precisa

| Arquivo | Para quê |
| --- | --- |
| `index.html` na raiz | a página; a esteira recusa se faltar, estiver vazio ou sem marcação HTML |
| `v3a-projeto.yml` na raiz | a ficha, com `bloco: pagina_web_simples` ([docs/ficha.md](../../docs/ficha.md)) |
| `.github/workflows/esteira.yml` | chamador da esteira ([exemplo](exemplo/.github/workflows/esteira.yml)) |
| `.github/workflows/voltar-versao.yml` | chamador do voltar versão ([exemplo](exemplo/.github/workflows/voltar-versao.yml)) |
| `testes/*.sh` (opcional) | testes do projeto; cada um roda na raiz do repositório e saída diferente de 0 para a esteira |
| `LICENSE` e `README.md` | licença proprietária e README técnico |

Os únicos arquivos de deploy são os dois chamadores e a ficha. **O repositório não tem Dockerfile**: a esteira usa sempre o [Dockerfile padrão do bloco](Dockerfile); um Dockerfile no repositório é ignorado.

## O que vai para a imagem

Todos os arquivos do repositório, menos: arquivos e pastas ocultos (`.git`, `.github`, `.env`...), links simbólicos, `testes/`, `docs/`, `README*`, `LICENSE*`, `Dockerfile` e a própria ficha na pasta do site. A ficha vai separada para `/v3a/v3a-projeto.yml`, fora do que é servido. Pasta `cgi-bin` é recusada.

## A imagem

- Base `busybox` fixada por digest; `httpd` na porta interna 8080, usuário 65534 (sem root).
- Arquivos do site em `/www`, só leitura para o processo.
- `HEALTHCHECK` no caminho `healthcheck` da ficha.
- Marcada com o commit (`:<commit>`) e identificada pelo digest; cache do build no cache do Actions.

## Começar um repositório

Copie a pasta [`exemplo/`](exemplo/) para a raiz do repositório novo, troque `N1-exemplo-pagina` pela CHAVE (o nome do repositório) e `<SHA>` nos dois chamadores pela versão da esteira em uso.
