# Pesquisa de planejamento: Migração completa do template para TaskList

Este planejamento não encontrou decisões técnicas pendentes. As escolhas abaixo foram verificadas
contra a configuração e o código atuais do repositório, e não exigem comparação com serviços externos.

## Metadados e empacotamento

- **Decisão**: `buildVars.py` é a origem prioritária de nome, resumo, descrição, versão, autor, URLs e
  compatibilidade; o pacote `.nvda-addon` e o manifesto são gerados pelo SCons.
- **Motivo**: `sconstruct` injeta `buildVars.addon_info` no ambiente NVDA e usa os valores para compor o
  manifesto e o nome do pacote.
- **Alternativas consideradas**: Editar diretamente `addon/manifest.ini` ou manter os dados em
  documentação duplicada. Rejeitadas porque o manifesto é derivado e a duplicação permite divergência.

## Nome do plugin e versão

- **Decisão**: Usar `TaskList` no diretório do plugin, nos metadados do projeto e no nome do complemento;
  usar a versão `1.0.0` nesta migração.
- **Motivo**: A especificação esclarece explicitamente o rename do diretório técnico e a versão, e a
  configuração atual de fontes inclui `addon/globalPlugins/ClipBoardEditor/*.py`.
- **Alternativas consideradas**: Manter o diretório `ClipBoardEditor` ou lançar com nova versão.
  Rejeitadas pelas clarificações registradas na especificação.

## Dados e compatibilidade

- **Decisão**: Manter o JSON `taskListData.json` no diretório de configuração do NVDA, bem como o backup,
  a gravação temporária e os formatos legados atualmente aceitos.
- **Motivo**: O plugin já carrega estruturas legadas em dicionário e listas, normaliza tarefas simples e
  mantém leitura e gravação locais.
- **Alternativas consideradas**: Migrar o formato ou usar armazenamento remoto. Rejeitadas por não serem
  necessárias para a atualização de identidade e por arriscarem incompatibilidade ou privacidade.

## Documentação e validação

- **Decisão**: Tratar `readme.md` como fonte de documentação do usuário, `DocumentaçãoTecnica.md` como
  guia de manutenção e usar o fluxo de validação existente do projeto (`unittest`, Ruff, Pyright, `prek`,
  SCons).
- **Motivo**: A build copia o readme para os documentos do complemento e os workflows do repositório já
  usam SCons, unittest e prek.
- **Alternativas consideradas**: Manter instruções do template ou introduzir um runner e processo de
  build novos. Rejeitadas por perpetuarem instruções incorretas ou ampliarem desnecessariamente o escopo.

## Interface pública observável

- **Decisão**: Documentar os gestos globais, atalhos da janela, ações de lista/tarefa, persistência,
  exportação e importação em um contrato de interação, validando a documentação contra os scripts e
  handlers atuais.
- **Motivo**: Embora o complemento não exponha uma API HTTP ou biblioteca pública, os gestos globais,
  a interface por teclado e os formatos de arquivo são contratos usados diretamente por usuários.
- **Alternativas consideradas**: Omitir contratos por não haver API de rede. Rejeitada porque isso
  deixaria critérios de aceitação centrais sem uma representação verificável.
