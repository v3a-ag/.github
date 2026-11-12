# Ficha do projeto: `v3a-projeto.yml` (versão 1) [proposta]

Arquivo na raiz de cada repositório de app. Diz **o que o app precisa**; o modelo do bloco decide **como** isso vira container no servidor. O esquema está em [`esquema/v3a-projeto.schema.json`](../esquema/v3a-projeto.schema.json) e o validador em [`scripts/validar_ficha.py`](../scripts/validar_ficha.py), rodado pela esteira em todo PR e todo push na `main`.

## Campos

| Campo | Obrigatório | Valores | Padrão |
| --- | --- | --- | --- |
| `versao` | sim | `1` | — |
| `chave` | sim | CHAVE do projeto, `^[A-Z][A-Z0-9]{1,4}-[a-z0-9]+(-[a-z0-9]+)*$`, até 40 caracteres, **igual ao nome do repositório** | — |
| `bloco` | sim | `pagina_web_simples` (outros blocos entram quando forem testados) | — |
| `healthcheck` | não | caminho que começa com `/` | `/` |
| `exposicao` | não | `interface_humana` (pessoas, pelo login); `maquina` fica bloqueado até a decisão do gateway de máquinas | `interface_humana` |
| `dependencias_privadas` | não | lista de `postgres`, `supabase` | `[]` |
| `servicos_compartilhados` | não | lista de `stirling-pdf`, `crawl4ai`, `searxng` | `[]` |
| `conversa_com_n8n` | não | `true` ou `false` | `false` |
| `apis_externas` | não | lista de `openai`, `anthropic`, `gemini`, `cnpja` | `[]` |
| `dados.classificacao` | não | `publico`, `interno`, `sensivel` | `interno` |
| `dados.persistencia` | não | `nenhuma`, `volume` | `nenhuma` |
| `recursos.memoria` | não | `32m` a `1024m` | `128m` |
| `recursos.cpu` | não | `0.05` a `2` | `0.25` |

Campo fora desta lista é recusado ("campo desconhecido").

## O que a ficha nunca aceita

Rede, sub-rede, alias, porta, mount, volume, label, privilégio, nome de container, hostname, IP, DNS e afins, **em qualquer nível** da ficha, com qualquer grafia (`porta`, `ports`, `sub-rede`, `subnet`, `labels`...). Também é recusado qualquer valor que cite `docker.sock`. Essas coisas são do modelo do bloco e do servidor; a ficha que as pede é recusada pelo Actions, e nenhum deployment é registrado.

**A porta sai da ficha.** Cada bloco fixa a porta interna do container (Página web simples: 8080). O desenvolvedor não escolhe porta.

## Exemplo

```yaml
versao: 1
chave: N1-exemplo-pagina
bloco: pagina_web_simples
healthcheck: /
exposicao: interface_humana
dependencias_privadas: []
servicos_compartilhados: []
conversa_com_n8n: false
apis_externas: []
dados: {classificacao: interno, persistencia: nenhuma}
recursos: {memoria: 64m, cpu: 0.25}
```

## Rodar o validador

```bash
yq -o=json '.' v3a-projeto.yml > /tmp/ficha.json
python3 scripts/validar_ficha.py --repositorio <nome-do-repositorio> /tmp/ficha.json
```

Saída `0`: ficha válida. Saída `1`: ficha recusada, com um `::error` por problema.
