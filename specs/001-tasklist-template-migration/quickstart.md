# Validação da migração do TaskList

## Inventário inicial da migração

Antes da migração, o repositório continha os seguintes resíduos técnicos do template:

- diretório `addon/globalPlugins/ClipBoardEditor/`;
- nome e metadados públicos `ClipBoardEditor`;
- documentação de editor da área de transferência;
- testes placeholders em `tests/unit/template/` e `tests/e2e/template/`;
- referências ao repositório antigo em manifesto, README e configuração Python.

## Pré-requisitos

- Windows com Python 3.13 disponível por meio do `uv`.
- Dependências de desenvolvimento restauradas (`uv sync`).
- Para validar o runtime completo, NVDA compatível com a versão mínima declarada e o complemento instalado.

## Testes automatizados e verificações estáticas

Na raiz do repositório, executar:

```powershell
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run prek run --all-files
```

Resultado esperado: comandos terminam sem falhas novas relacionadas à migração. Testes marcados como
`expectedFailure` pela estrutura existente continuam identificados como esperados.

## Construir e inspecionar o pacote

```powershell
uv run scons
```

Resultado esperado:

- Um único `.nvda-addon` é produzido na raiz com nome TaskList e versão `1.0.0`.
- O manifesto incluído tem nome, resumo, descrição, autor, URL, versão e compatibilidade coerentes com
  `buildVars.py`.
- O pacote inclui o plugin em `globalPlugins/TaskList/` e documentação pt-BR do TaskList.
- O pacote não contém arquivos, caminhos ou metadados que identifiquem o ClipBoardEditor ou a antiga
  funcionalidade de histórico da área de transferência.

## Conferência documental e de identidade

1. Conferir `readme.md` e `DocumentaçãoTecnica.md` contra
   [o contrato de interação](./contracts/user-interaction.md) e
   [o modelo de dados](./data-model.md).
2. Conferir a origem das fontes em `buildVars.py` contra os metadados do pacote construído.
3. Buscar referências ao nome e à funcionalidade do template antigo nas fontes de distribuição; ignorar
   referências explicativas necessárias em documentos da própria migração.
4. Confirmar que URLs, nome do projeto, pasta do plugin e referências de build usam TaskList.

## Verificação manual no NVDA

1. Instalar o `.nvda-addon` construído e confirmar a identidade TaskList no Gestor de Complementos e na
   categoria de comandos do NVDA.
2. Abrir a janela, navegar pelos controles usando teclado e validar anúncios de abas, totais, tarefas e
   mensagens de resultado.
3. Exercitar os fluxos de tarefa e lista descritos no contrato, incluindo bloqueios das listas protegidas.
4. Abrir dados existentes no formato atual e nos formatos legados suportados; confirmar que tarefas e
   listas continuam disponíveis.
5. Testar importação e exportação, incluindo caminhos inválidos ou falhas de arquivo, verificando que
   mensagens de erro não anunciam sucesso.
