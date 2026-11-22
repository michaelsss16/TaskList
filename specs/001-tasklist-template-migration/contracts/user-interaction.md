# Contrato de interação do TaskList

Este contrato é uma referência verificável para documentação e teste manual. A documentação final deve
ser conferida contra os scripts e eventos do plugin, não usada para alterar silenciosamente o
comportamento existente.

## Gestos globais do NVDA

| Gesto padrão | Resultado |
|---|---|
| `NVDA+ç` | Abre ou eleva a janela principal do TaskList. |
| `NVDA+Shift+ç` | Anuncia as tarefas recentes da lista Principal, na ordem de prioridade e até o limite configurado. |
| `NVDA+Alt+ç` | Solicita uma nova tarefa para Principal e salva a alteração. |

O NVDA permite ao usuário reconfigurar os gestos na categoria `TaskList`.

## Teclas na janela

| Tecla | Condição | Resultado |
|---|---|---|
| `Ctrl+N` | Lista de tarefas em foco | Cria uma tarefa na lista atual. |
| `Enter` | Tarefa selecionada | Edita o texto da tarefa. |
| `Shift+Enter` | Tarefa selecionada | Edita as notas. |
| `Ctrl+P` | Tarefa selecionada | Cicla Normal → Baixa → Média → Alta → Normal. |
| `Espaço` | Tarefa selecionada | Conclui a tarefa ou reabre a partir de Concluídas. |
| `Delete` | Tarefa selecionada | Exclui a tarefa durante a sessão do diálogo. |
| `Ctrl+Z` | Janela aberta | Desfaz a exclusão mais recente desta sessão. |
| `Ctrl+C` | Tarefa selecionada | Copia texto, prioridade e notas da tarefa para a área de transferência. |
| `Ctrl+Shift+C` | Janela aberta | Copia a lista atual como Markdown; não copia lista vazia. |
| `Ctrl+Seta para cima/baixo` | Tarefa selecionada | Move a tarefa na lista atual. |
| `Ctrl+Seta para esquerda/direita` | Tarefa selecionada | Move a tarefa para a lista adjacente. |
| `Ctrl+F` | Lista de tarefas em foco | Busca texto da tarefa ou notas na lista atual. |
| `Ctrl+1` a `Ctrl+9` | Janela aberta | Seleciona a aba na posição indicada, se existir. |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | Janela aberta | Navega entre abas pela navegação padrão do notebook. |
| `Ctrl+Shift+N` | Janela aberta | Cria nova lista à direita da atual. |
| `F2` | Janela aberta | Renomeia lista personalizada; listas protegidas não podem ser renomeadas. |
| `Ctrl+Shift+Delete` | Janela aberta | Limpa tarefas de listas protegidas ou solicita exclusão de lista personalizada. |
| `Ctrl+Alt+Seta para esquerda/direita` | Janela aberta | Move a aba/lista atual. |
| `Ctrl+E` | Janela aberta | Exporta tarefas para `.txt` ou `.md`. |
| `Ctrl+I` | Janela aberta | Importa linhas de um arquivo `.txt` na lista atual. |
| `F1` | Janela aberta | Exibe ajuda de atalhos. |
| `Esc` | Janela aberta | Fecha a janela; os dados são salvos no fechamento. |

## Arquivos e persistência

- Dados do usuário são armazenados localmente em `taskListData.json`, no caminho de configuração do NVDA.
- Uma gravação bem-sucedida substitui o arquivo principal por gravação temporária; o arquivo existente
  é copiado para `taskListData.json.bak` antes da gravação.
- A exportação contém seções por lista e tarefas legíveis; notas são exportadas em linhas subsequentes.
- A importação lê linhas não vazias de `.txt` como tarefas e remove marcadores simples de lista/número.
- Falhas de importação/exportação devem ser anunciadas sem mensagem de sucesso.

## Critérios de conformidade

1. Cada gesto e atalho documentado deve corresponder a um handler implementado.
2. Nomes, estados e ações devem permanecer acessíveis por teclado e anunciados pelo NVDA.
3. Dados permanecem locais, e formatos legados suportados continuam carregáveis.
4. Documentação não deve prometer restauração após encerramento do NVDA, importação estruturada de notas
   ou formatos além dos aceitos pelos diálogos.
