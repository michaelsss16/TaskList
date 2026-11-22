# Feature Specification: Migração completa do template para TaskList

**Feature Branch**: `[001-tasklist-template-migration]`

**Created**: `2026-11-22`

**Status**: Draft
**Input**: Atualizar toda a documentação, nome de arquivos, comportamentos e descrições do plugin a partir do `__init__.py` do TaskList. O `__init__.py` é o único arquivo novo do projeto; os demais arquivos pertencem ao template inicial de histórico da área de transferência e não podem continuar representando o projeto.

## Clarifications

### Session 2026-11-22

- Q: Qual abordagem usar para o diretório técnico do plugin? → A: Renomear para TaskList
- Q: Qual versão deve receber o TaskList nesta migração? → A: 1.0.0

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reconhecer o plugin como TaskList (Priority: P1)

Como usuário do NVDA, eu quero que nome, resumo, descrição, janela, atalhos e documentação identificáveis
representem o TaskList, para que eu saiba que estou usando um gerenciador de tarefas e não o editor de
histórico da área de transferência usado anteriormente.

**Why this priority**: Identidade incorreta pode fazer o usuário instalar ou operar o complemento errado.

**Independent Test**: Instalar o artefato final em um ambiente de teste e comparar nome, resumo,
descrição, título da janela, categoria de comandos e documentação com a identidade TaskList.

**Acceptance Scenarios**:

1. **Given** o usuário visualiza os dados do complemento no NVDA, **When** abre o gerenciador de
   complementos, **Then** nome e descrição apresentados identificam o TaskList.
2. **Given** o usuário abre a janela principal, **When** a interface é exibida, **Then** títulos, rótulos
   e mensagens descrevem tarefas e listas.
3. **Given** o usuário consulta os comandos configuráveis do NVDA, **When** navega pela categoria do
   complemento, **Then** os comandos aparecem como funcionalidades do TaskList.

---

### User Story 2 - Separar o conteúdo novo dos resíduos do template (Priority: P1)

Como mantenedor do projeto, eu quero remover da distribuição e da documentação toda referência à
funcionalidade antiga de histórico da área de transferência, para que o repositório represente apenas o
TaskList.

**Why this priority**: Referências antigas podem impedir a publicação correta e induzir documentação
desalinhada.

**Independent Test**: Revisar o repositório e o pacote gerado procurando pelo nome antigo, pelos termos
de histórico da área de transferência e pelos nomes de arquivos derivados do template.

**Acceptance Scenarios**:

1. **Given** a documentação do projeto foi atualizada, **When** um usuário a lê, **Then** não encontra
   instruções ou descrições da funcionalidade antiga.
2. **Given** os arquivos distribuídos foram preparados, **When** são examinados, **Then** os nomes,
   resumos e caminhos correspondem ao TaskList.
3. **Given** o complemento é construído, **When** o pacote é criado, **Then** o pacote não contém texto,
   nome de arquivo ou caminho que o identifique como histórico da área de transferência.

---

### User Story 3 - Preservar o comportamento real do TaskList (Priority: P1)

Como usuário, eu quero que todas as alterações de identidade e documentação sejam coerentes com os
comportamentos já implementados no arquivo principal, para que os recursos documentados possam ser
executados.

**Why this priority**: A atualização não deve prometer funcionalidades diferentes das implementadas.

**Independent Test**: Executar os principais fluxos descritos pela documentação e compará-los com os
comandos e mensagens disponíveis no plugin.

**Acceptance Scenarios**:

1. **Given** uma tarefa foi criada, editada, concluída, excluída ou restaurada, **When** o usuário usa os
   atalhos correspondentes, **Then** a interface e os anúncios são consistentes com a documentação.
2. **Given** o usuário cria, renomeia, limpa, exclui, reordena, exporta ou importa listas e tarefas,
   **When** conclui cada ação, **Then** o comportamento descrito corresponde ao resultado observado.
3. **Given** os dados já existem em uma instalação anterior, **When** o plugin inicia, **Then** os dados
   e as listas conhecidas são carregados sem perda.

---

### User Story 4 - Centralizar os metadados do complemento (Priority: P2)

Como mantenedor, eu quero que os dados públicos do complemento sejam definidos em uma única origem
principal de metadados, para evitar divergências entre manifesto, documentação e pacote.

**Why this priority**: Metadados duplicados e inconsistentes dificultam manutenção e lançamento.

**Independent Test**: Alterar um dado público na origem principal e confirmar que todas as referências
derivadas usam o novo valor após a preparação da distribuição.

**Acceptance Scenarios**:

1. **Given** um metadado público precisa mudar, **When** o mantenedor o atualiza na configuração principal
   de build, **Then** as demais referências derivadas são atualizadas na distribuição.
2. **Given** o pacote foi preparado, **When** nome, versão, autor, URL e compatibilidade são consultados,
   **Then** não existem valores conflitantes.

---

### Edge Cases

- Uma referência antiga aparece em nome de arquivo, pasta, configuração ou documentação.
- A descrição antiga está incompleta ou não corresponde a uma funcionalidade implementada.
- Uma lista protegida ou dados sem uma lista concluída são encontrados na instalação.
- Dados legados têm formato diferente do formato atual.
- Falhas de leitura, gravação, exportação ou importação devem ser comunicadas sem indicar sucesso.
- Nomes de arquivos ou pacotes excedem ou usam caracteres incompatíveis com Windows.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O projeto DEVE apresentar o complemento com o nome TaskList em todas as referências públicas.
- **FR-002**: Toda documentação voltada ao usuário DEVE ser escrita em português do Brasil e DEVE
  explicar as tarefas, listas, prioridades, notas, conclusão, importação e exportação implementadas.
- **FR-003**: Os nomes de arquivos e caminhos do complemento criados para esta migração DEVEM refletir
  o TaskList e não o template antigo; o diretório técnico do plugin deve ser renomeado de
  `ClipBoardEditor` para `TaskList`, com referências de build e fontes atualizadas.
- **FR-004**: Os dados públicos do complemento DEVEM ser centralizados prioritariamente na configuração
  principal de build.
- **FR-005**: O pacote e os artefatos derivados DEVEM manter versão, autor, URL, nome, resumo,
  descrição e compatibilidade consistentes; nesta migração, a versão do complemento será `1.0.0`.
- **FR-006**: O sistema DEVE remover ou substituir todas as referências identificáveis à identidade,
  documentação e funcionalidade anteriores de histórico da área de transferência.
- **FR-007**: A documentação dos atalhos DEVE corresponder aos atalhos implementados no plugin.
- **FR-008**: Os comportamentos de tarefas, listas, prioridades, notas, busca, exportação, importação,
  conclusão e restauração já implementados DEVEM ser preservados.
- **FR-009**: Os dados locais existentes DEVEM continuar carregáveis pelo TaskList após a migração.
- **FR-010**: Mensagens de sucesso, falha e ajuda DEVEM ser em português do Brasil e não citar a
  funcionalidade anterior.
- **FR-011**: A documentação técnica DEVE explicar como preparar, validar e gerar o pacote do TaskList
  sem depender de instruções ou nomenclatura do template antigo.
- **FR-012**: O projeto DEVE validar que o artefato final não contém referências ao template antigo em
  seus metadados, nomes ou documentos distribuídos.

### Key Entities *(include if feature involves data)*

- **Complemento TaskList**: Identidade pública do produto, composta por nome, resumo, descrição,
  versão, autor, URLs, compatibilidade e documentação.
- **Tarefa**: Item com texto, prioridade, notas, data de conclusão, lista de origem e posição na lista.
- **Lista**: Coleção nomeada de tarefas, incluindo listas padrão e listas criadas pelo usuário.
- **Configuração do complemento**: Dados públicos e caminhos usados para preparar o pacote e os
  artefatos derivados.
- **Dados locais persistidos**: Conteúdo das tarefas e das listas armazenado no perfil local do usuário.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Em uma revisão completa, 100% das referências públicas visíveis identificam o produto como
  TaskList e 0 referências ao template antigo permanecem em arquivos distribuídos.
- **SC-002**: Pelo menos 100% dos atalhos documentados são verificáveis contra os comportamentos
  implementados no plugin.
- **SC-003**: Um usuário pode identificar o nome, o propósito e os principais usos do complemento pela
  documentação sem consultar arquivos do template antigo.
- **SC-004**: O processo de geração produz um único pacote reconhecível como TaskList, com metadados
  consistentes em todos os artefatos derivados.
- **SC-005**: Os principais fluxos de criar, editar, concluir, reabrir, excluir, restaurar, buscar,
  exportar e importar passam em revisão funcional antes da conclusão da migração.
- **SC-006**: A migração não perde dados locais válidos nem altera o formato das tarefas sem preservação
  compatível.

## Assumptions

- O arquivo principal `__init__.py` é a fonte funcional a ser usada para documentar comportamentos;
  na conclusão da migração, ele permanece em `addon/globalPlugins/TaskList/__init__.py`.
- Os arquivos fora desse arquivo são considerados infraestrutura ou artefatos do template a serem
  ajustados, renomeados ou removidos conforme necessário.
- Nomes técnicos em inglês podem permanecer quando forem exigidos por APIs, formatos ou ferramentas,
  mas o conteúdo voltado ao usuário deve usar português do Brasil.
- A lista não será alterada para incluir novos conceitos de produto além das tarefas e listas já
  implementadas.
- Os dados locais são pessoais e não devem ser enviados a serviços externos.
