<!--
Sync Impact Report
- Version change: 1.1.0 -> 1.1.1
- Modified principles: II. Dados locais e privacidade; IV. Desenvolvimento orientado a testes;
  VI. Idioma e nomenclatura em pt-BR
- Added sections: none
- Removed sections: none
- Follow-up TODOs: Ratification date is unknown and requires confirmation
-->

# Constituição do TaskList

## Core Principles

### I. Acessibilidade em primeiro lugar com NVDA

Toda funcionalidade DEVE ser utilizável por teclado e DEVE expor nomes, funções, estados e anúncios
claros por meio das APIs do NVDA. A implementação DEVE usar os padrões de plugin global, gestos,
interface e síntese de voz já estabelecidos pelo projeto. Esta regra é inegociável porque o complemento
precisa melhorar o acesso e não pode criar telas inacessíveis ou atalhos que prendam o usuário.

### II. Dados locais e privacidade

Os dados das tarefas DEVEM permanecer locais ao ambiente do NVDA, exceto quando o usuário iniciar
explicitamente uma operação externa. O complemento NÃO DEVE enviar conteúdo de usuário pela rede,
adicionar telemetria que capture dados pessoais ou persistir informações temporárias além do necessário.
Os mecanismos de persistência DEVEM preservar os dados existentes em caso de falha e minimizar
informações pessoais armazenadas.

### III. Integração nativa com NVDA

O código de produção DEVE seguir o modelo de complemento do NVDA, as convenções Python, os metadados
do manifesto, a localização e a estrutura de empacotamento deste repositório. O comportamento público
DEVE permanecer compatível com a versão mínima do NVDA e com o Python 3.13 configurados. Alterações
em gestos, rótulos de interface, manifestos ou metadados DEVEM ser deliberadas e documentadas.

### IV. Desenvolvimento orientado a testes e regressões

Alterações de comportamento DEVEM possuir cobertura automatizada focada antes da integração. Os
testes DEVEM cobrir resultados observáveis, como operações com tarefas, interface, teclado, migração
de dados, persistência e recuperação de erros. Testes unitários são obrigatórios para lógica isolada;
testes de ponta a ponta ou de integração com NVDA são obrigatórios quando o comportamento atravessar
plugin, interface ou APIs do NVDA.

### V. Legibilidade, confiabilidade e escopo pequeno

A implementação DEVE preferir funções claras e testáveis e os utilitários existentes a abstrações
desnecessárias. Falhas DEVEM ser registradas com contexto útil e NÃO DEVEM corromper dados nem
apresentar anúncios de sucesso enganosos. Cada alteração DEVE manter escopo restrito, documentar
comportamentos descobríveis e fornecer plano de compatibilidade ou reversão quando afetar dados
persistidos ou comportamento público.

### VI. Idioma e nomenclatura em pt-BR

Toda especificação, documentação técnica, orientação de uso e texto de governança DEVE ser escrita em
português do Brasil. Os nomes de funções, classes, variáveis e outros símbolos criados no código DEVEM
usar nomes descritivos em pt-BR, salvo termos técnicos amplamente adotados ou exigências das APIs do
NVDA. O código existente ou importado pode preservar nomes de terceiros até que uma alteração planejada
o normalize. Esta regra elimina ambiguidade para contribuidores e usuários brasileiros e não exige
tradução artificial de APIs externas.

O projeto se chama TaskList. Os metadados provisórios derivados do template padrão DEVEM ser ajustados
para a identidade, a documentação e os nomes do TaskList antes de publicar uma nova versão.

## Development Constraints

- O complemento DEVE ser destinado ao Windows e ao Python 3.13 e DEVE seguir a estrutura de fontes
  dos complementos do NVDA.
- O intervalo de versões suportadas do NVDA DEVE ser declarado no manifesto e mantido consistente
  com a documentação e as variáveis de compilação.
- Todas as strings visíveis ao usuário DEVEM usar pt-BR e suporte à localização pelas convenções
  existentes de gettext e do NVDA.
- Os dados públicos do plugin, como nome, resumo, descrição, versão, autor, URL e compatibilidade,
  DEVEM ser definidos prioritariamente em `buildVars.py`, conforme o padrão de compilação adotado.
  Manifestos e arquivos derivados DEVEM ser gerados a partir dessas definições.
- Operações sobre dados DEVEM preservar o conteúdo do usuário e evitar alterações não solicitadas até
  uma ação explícita de salvar ou concluir.
- A lógica de validação e formatação DEVE validar a entrada e informar erros precisos e acionáveis.
- O código DEVE passar pelas verificações de formatação e validação estática configuradas antes do
  lançamento.
- Os pacotes gerados DEVEM conter o manifesto, a documentação e os recursos localizados esperados.

## Development Workflow

- Toda funcionalidade DEVE começar por um caso de uso claro, com critérios de aceitação cobrindo acesso
  por teclado, anúncios do NVDA, entradas inválidas e recuperação de falhas.
- As implementações DEVEM usar a menor alteração que satisfaça os critérios e reutilizar os padrões
  existentes do repositório.
- Revisões locais ou pull requests DEVEM verificar acessibilidade, privacidade, compatibilidade,
  cobertura de testes, localização, documentação e empacotamento.
- O changelog e a documentação do usuário DEVEM ser atualizados para alterações públicas, gestos,
  compatibilidade ou formatos de dados.
- Releases DEVEM construir o pacote `.nvda-addon`, verificar o manifesto e executar a suíte de
  validação configurada antes da distribuição.

## Governance

Esta constituição substitui práticas informais do repositório para planejamento e implementação.
Todos os contribuidores DEVEM verificar alterações substantivas contra estes princípios durante a
revisão. A constituição DEVE ser alterada quando um princípio for adicionado, removido ou redefinido
substancialmente, ou quando restrições globais de desenvolvimento forem modificadas.

Alterações exigem justificativa documentada, nova versão, plano de migração ou compatibilidade quando
necessário e sincronização da documentação do projeto. Aplica-se versionamento semântico: MAJOR para
mudanças incompatíveis de governança ou princípios, MINOR para novos princípios ou expansão material
de seções, e PATCH para esclarecimentos ou ajustes não semânticos.

As revisões de conformidade DEVEM cobrir acessibilidade, privacidade, compatibilidade com NVDA, testes,
localização, documentação e empacotamento. Exceções DEVEM ser explícitas nas notas de revisão e
DEVEM incluir justificativa, escopo afetado e plano de remediação.

**Version**: 1.1.1 | **Ratified**: TODO(RATIFICATION_DATE): confirmar a data original de adoção | **Last Amended**: 2026-11-22
