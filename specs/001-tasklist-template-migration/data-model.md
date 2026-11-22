# Modelo de dados: TaskList

Este modelo descreve os dados persistidos e os estados mantidos pela implementação existente; não
introduz novo formato. Os dados ficam em `taskListData.json` no diretório de configuração do NVDA.

## Complemento TaskList

| Campo | Descrição / regra |
|---|---|
| `name` | Nome público do complemento: `TaskList`. |
| `summary`, `description` | Identidade curta e descrição em pt-BR. |
| `version` | Versão de migração: `1.0.0`. |
| `author`, `url`, `sourceURL` | Dados públicos definidos prioritariamente em `buildVars.py`. |
| Compatibilidade NVDA | Versões mínima e testada declaradas consistentemente no manifesto e documentação. |

## Configuração persistida

| Campo | Tipo | Regra |
|---|---|---|
| `settings` | objeto | Mantém preferências do complemento. |
| `settings.soundEnabled` | booleano | Habilita feedback sonoro; padrão atual `true`. |
| `settings.recentReadCount` | inteiro | Quantidade de tarefas da lista Principal lidas pelo gesto global; padrão atual `3`. |
| `lists` | lista de Listas | Cada lista tem nome e coleção ordenada de tarefas. |

As listas padrão incluem `Principal`, `Acompanhamento`, `Tarefas pessoais` e `Concluídas`.
`Principal` e `Concluídas` são protegidas contra renomeação e exclusão; suas tarefas podem ser limpas.
Listas personalizadas podem ser renomeadas, movidas ou excluídas com suas tarefas.

## Lista

| Campo | Tipo | Regra |
|---|---|---|
| `name` | texto | Nome mostrado como aba; listas `Principal` e `Concluídas` são protegidas. |
| `tasks` | lista de Tarefas | Ordem estável por prioridade em ações que classificam tarefas; posição não é campo persistido. |

## Tarefa

| Campo | Tipo | Regra |
|---|---|---|
| `text` | texto | Descrição da tarefa. |
| `priority` | inteiro | `0` Normal, `1` Baixa, `2` Média, `3` Alta; a interface ordena prioridade maior primeiro. |
| `notes` | texto | Notas adicionais, padrão vazio. |
| `created_at` | texto de data/hora | Criada no formato `dd/mm/AAAA HH:MM` quando ausente. |
| `completed_at` | texto de data/hora ou nulo | Definido ao concluir; removido ao reabrir. |
| `origin_list` | texto ou nulo | Lista de origem para reabrir uma tarefa concluída. |

Uma tarefa pode ser criada, editada, priorizada, movida entre listas, concluída e reaberta. A exclusão
é reversível apenas durante a sessão do diálogo por meio da pilha de desfazer em memória.

## Formatos legados aceitos

- Objeto legado com `principal`, `acompanhamento` e `completas`: convertido às listas padrão
  correspondentes; a lista pessoal fica vazia.
- Lista de objetos `{name, tasks}`: convertida para listas nomeadas.
- Objeto com `settings` e `lists`: configurações são mescladas aos padrões e listas/tarefas normalizadas.
- Tarefas em formato texto são convertidas para tarefa com valores padrão; objetos de tarefa têm campos
  ausentes preenchidos.

Na migração de identidade, estes formatos e o nome do arquivo de dados devem continuar reconhecidos para
evitar perda de dados existentes.
