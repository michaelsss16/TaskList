# TaskList

TaskList é um complemento do NVDA para criar, organizar e concluir tarefas em listas locais.
Os dados são preservados no perfil do NVDA e não são enviados pela internet.

## Instalação

1. Baixe o arquivo `TaskList-1.0.0.nvda-addon` da seção Releases ou gere o pacote com `uv run scons`.
2. Abra o arquivo no NVDA e confirme a instalação no Gestor de Complementos.
3. Reinicie o NVDA, se solicitado.

## Operações principais

- Crie tarefas em qualquer lista e edite seu texto e notas.
- Priorize tarefas entre Normal, Baixa, Média e Alta.
- Mova tarefas entre listas adjacentes ou altere a posição dentro da lista.
- Conclua tarefas na lista Concluídas e reabra-as em sua lista de origem.
- Renomeie ou exclua listas personalizadas.
- Pesquise texto e notas na lista atual.
- Exporte tarefas em texto ou Markdown e importe linhas de arquivos `.txt`.

As listas Principal e Concluídas são protegidas contra renomeação e exclusão.

## Gestos globais

| Gesto | Ação |
|---|---|
| NVDA+ç | Abre ou eleva a janela do TaskList |
| NVDA+Shift+ç | Anuncia até três tarefas recentes da lista Principal |
| NVDA+Alt+ç | Solicita uma nova tarefa para a lista Principal |

Os gestos podem ser reconfigurados em NVDA > Preferências > Definir comandos, na categoria TaskList.

## Atalhos da janela

| Atalho | Ação |
|---|---|
| Ctrl+N | Nova tarefa na lista atual |
| Enter | Editar texto da tarefa selecionada |
| Shift+Enter | Editar notas da tarefa selecionada |
| Ctrl+P | Alternar prioridade |
| Espaço | Concluir ou reabrir tarefa |
| Delete | Excluir tarefa desta sessão |
| Ctrl+Z | Desfazer a última exclusão da sessão |
| Ctrl+C | Copiar tarefa, prioridade e notas |
| Ctrl+Shift+C | Copiar a lista atual como Markdown |
| Ctrl+Seta acima/abaixo | Mover tarefa na lista |
| Ctrl+Seta esquerda/direita | Mover tarefa para a lista adjacente |
| Ctrl+F | Buscar na lista atual |
| Ctrl+1 a Ctrl+9 | Selecionar uma aba existente |
| Ctrl+Tab / Ctrl+Shift+Tab | Navegar entre abas |
| Ctrl+Shift+N | Criar lista |
| F2 | Renomear lista personalizada |
| Ctrl+Shift+Delete | Limpar lista protegida ou excluir lista personalizada |
| Ctrl+Alt+Seta esquerda/direita | Mover a aba atual |
| Ctrl+E | Exportar para `.txt` ou `.md` |
| Ctrl+I | Importar linhas de um arquivo `.txt` |
| F1 | Exibir ajuda |
| Esc | Fechar e salvar |

## Dados e recuperação

Os dados são gravados em `taskListData.json`, no diretório de configuração do NVDA.
Antes de uma gravação, o arquivo existente é preservado como `taskListData.json.bak`.
Uma exclusão pode ser desfeita enquanto a janela permanecer aberta. O encerramento do NVDA não
preserva a pilha de desfazer.

## Construção e validação

```powershell
uv sync
uv run scons
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run prek run --all-files
```

## Compatibilidade

- Versão: 1.0.0
- NVDA mínimo: 2026.3
- NVDA testado: 2026.3
- Plataforma: Windows

## Autor e licença

Michael da Silva Soares dos Santos

- E-mail: michaelsss16@gmail.com
- Repositório: https://github.com/michaelsss16/TaskList

Distribuído sob a GNU General Public License, versão 2. Consulte `COPYING.txt`.
