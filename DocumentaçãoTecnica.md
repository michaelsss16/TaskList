# Documentação Técnica do TaskList

## Construção

Restaurar dependências e criar o pacote:

```powershell
uv sync
uv run scons
```

Os metadados públicos são definidos em `buildVars.py`. O SCons gera `addon/manifest.ini`,
o HTML da documentação e o arquivo `TaskList-1.0.0.nvda-addon`.

## Validação

```powershell
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run prek run --all-files
```

## Estrutura relevante

- `addon/globalPlugins/TaskList/__init__.py`: implementação do plugin.
- `addon/doc/pt_BR/readme.md`: documentação distribuída.
- `buildVars.py`: metadados públicos e fontes Python.
- `specs/001-tasklist-template-migration/quickstart.md`: roteiro de validação da migração.
