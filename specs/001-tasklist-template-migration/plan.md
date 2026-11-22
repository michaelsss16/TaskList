# Plano de Implementação: Migração completa do template para TaskList

**Branch**: `001-tasklist-template-migration` | **Data**: 2026-11-22 | **Spec**: [spec.md](./spec.md)

**Entrada**: Especificação da feature em `specs/001-tasklist-template-migration/spec.md`

## Resumo

Alinhar a identidade e os documentos de distribuição com os comportamentos existentes do TaskList,
removendo metadados, nomenclatura, documentação e estrutura remanescentes do template ClipBoardEditor.
Os dados públicos serão definidos em `buildVars.py`; o diretório do plugin será
`addon/globalPlugins/TaskList/`; o pacote e os metadados do projeto usarão a versão `1.0.0`.
Os dados de tarefas permanecerão no JSON local existente, preservando os formatos legados suportados.

## Contexto técnico

**Linguagem/Versão**: Python 3.13

**Dependências principais**: NVDA, wxPython fornecido pelo NVDA, SCons e ferramentas de build configuradas
em `pyproject.toml`.

**Armazenamento**: JSON em `globalVars.appArgs.configPath/taskListData.json`, com backup `.bak` e gravação
temporária `.tmp`.

**Testes**: `unittest` (`uv run python -m unittest discover -s tests -v`), Ruff, Pyright e `prek`.

**Plataforma alvo**: Windows com NVDA 2026.3 ou superior, conforme metadados atuais de compatibilidade.

**Tipo de projeto**: Complemento acessível do NVDA com interface wxPython e plugin global.

**Metas de desempenho**: Não há metas numéricas especificadas; manter as operações locais e os fluxos
interativos existentes.

**Restrições**: Dados locais e privados; navegação por teclado e anúncios NVDA; strings e documentação
visíveis ao usuário em pt-BR; metadados centralizados; versão do complemento `1.0.0`; manter compatibilidade
com o formato legado dos dados.

**Escala/escopo**: Um perfil local do NVDA, listas e tarefas do usuário; uma migração de identidade e
documentação, sem introduzir novos conceitos de produto.

## Verificação da Constituição

| Princípio / restrição | Estado | Aplicação ao plano |
|---|---|---|
| Acessibilidade NVDA | Conforme | Preservar os gestos, comandos de teclado, rótulos nomeados e anúncios implementados; documentá-los com exatidão. |
| Dados locais e privacidade | Conforme | Preservar armazenamento no perfil e não introduzir rede ou telemetria. |
| Integração nativa com NVDA | Conforme | Manter a estrutura e o empacotamento SCons do complemento e declarar compatibilidade consistente. |
| Testes e regressões | Conforme | Executar testes automatizados, verificações estáticas e validação de pacote; cobrir regressões de persistência e identidade. |
| Legibilidade e escopo pequeno | Conforme | Alterar somente os arquivos derivados do template e as referências necessárias ao rename e à identidade. |
| pt-BR e nomenclatura | Conforme | Atualizar documentação do usuário e strings públicas em pt-BR; usar TaskList em referências técnicas próprias. |
| Manifesto, docs e pacote | Conforme | Gerar os dados derivados da origem de metadados e confirmar os arquivos incluídos no `.nvda-addon`. |

**Resultado do gate inicial**: PASS. A feature não propõe nova coleta, dependência funcional ou mudança
do formato de persistência.

## Estrutura do repositório

```text
addon/
├── globalPlugins/
│   └── TaskList/
│       └── __init__.py
├── doc/
│   ├── style.css
│   └── pt_BR/
│       └── readme.md
└── manifest.ini                 # gerado pelo build
buildVars.py                     # origem dos metadados do complemento
readme.md                        # documentação-fonte do usuário
DocumentaçãoTecnica.md           # documentação de manutenção e build
pyproject.toml                   # identidade do projeto Python
uv.lock                          # dependências de desenvolvimento travadas
tests/
├── unit/
└── e2e/
specs/001-tasklist-template-migration/
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   └── user-interaction.md
└── quickstart.md
```

**Decisão de estrutura**: Projeto de complemento único. O pacote de fonte do plugin será renomeado de
`ClipBoardEditor` para `TaskList`; configuração de build, metadados do projeto e documentação que apontam
para nomes antigos devem acompanhar a mudança. Artefatos de build não são fontes de metadados.

## Gate após o design

**Resultado**: PASS. O design preserva a integração NVDA, os dados locais e a acessibilidade, descreve os
contratos observáveis sem ampliar o produto e define verificações reproduzíveis. Nenhuma exceção à
Constituição é necessária.
