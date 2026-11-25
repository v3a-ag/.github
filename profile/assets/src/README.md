# Fontes das imagens desta página

As imagens em `profile/assets/` são geradas por estes scripts. Para mudar um texto, edite
`publica/pecas.py` e gere de novo:

```bash
cd profile/assets/src
python3 -m venv .venv && .venv/bin/pip install fonttools pillow brotli
.venv/bin/python -m publica.pecas ..
```

- `gerador/` converte texto em Geologica para contorno SVG, monta as versões clara e escura e
  guarda os ícones e o logo oficial (manual de marca V3A).
- `gerador/recursos/Geologica.ttf` está sob a SIL Open Font License (`OFL.txt`).
- Testes: `.venv/bin/python -m unittest discover -p 'test_*.py'`
