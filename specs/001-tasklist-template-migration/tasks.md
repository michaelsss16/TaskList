# Tasks: Migração completa do template para TaskList

**Input**: Design documents from `/specs/001-tasklist-template-migration/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Acceptance scenarios in the specification require regression coverage. Unit and integration tests are included where they verify observable behavior.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the migration workspace and establish repeatable validation commands.

- [X] T001 Create the migration baseline and record the old-template file inventory in `specs/001-tasklist-template-migration/quickstart.md`
- [X] T002 [P] Define the TaskList unit-test modules under `tests/unit/` and replace template placeholders under `tests/unit/template/`
- [X] T003 [P] Define the TaskList package-validation fixtures under `tests/e2e/` and replace template placeholders under `tests/e2e/template/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Apply the technical rename and package-source configuration required by every user story.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 Rename `addon/globalPlugins/ClipBoardEditor/` to `addon/globalPlugins/TaskList/` and preserve `addon/globalPlugins/TaskList/__init__.py`
- [X] T005 Update the Python source globs and plugin identity references for `TaskList` in `buildVars.py`
- [X] T006 Update project metadata for the TaskList repository in `pyproject.toml`
- [X] T007 Update package build and source references in `sconstruct`
- [X] T008 [P] Confirm the existing TaskList persistence fields remain `taskListData.json` and implement no format migration beyond `data-model.md` definitions in `addon/globalPlugins/TaskList/__init__.py`
- [X] T009 [P] Remove or neutralize unused template sanity files under `tests/unit/template/` and `tests/e2e/template/`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Reconhecer o plugin como TaskList (Priority: P1) 🎯 MVP

**Goal**: Align the visible plugin identity, window, commands, labels, and user documentation with the implemented TaskList.

**Independent Test**: Install and inspect the built package, verify the manifest and command category identify TaskList, open the window, and confirm documented shortcuts match the implemented handlers.

- [X] T010 [P] [US1] Update public metadata values in `buildVars.py` for `Complemento TaskList.name`, `Complemento TaskList.summary`, `Complemento TaskList.description`, `Complemento TaskList.version`, `Complemento TaskList.author`, `Complemento TaskList.url`, and `Complemento TaskList.sourceURL` as defined by `data-model.md`
- [X] T011 [P] [US1] Update the TaskList window title and TaskList-specific visible labels in `addon/globalPlugins/TaskList/__init__.py`
- [X] T012 [P] [US1] Verify and update the global gesture descriptions and `scriptCategory = "TaskList"` handlers in `addon/globalPlugins/TaskList/__init__.py`
- [X] T013 [US1] Rewrite the user guide in `readme.md` with pt-BR TaskList installation, task/list operations, search, priority, notes, completion, export/import, and the gestures in `specs/001-tasklist-template-migration/contracts/user-interaction.md`
- [X] T014 [US1] Synchronize the distributed pt-BR guide in `addon/doc/pt_BR/readme.md` with `readme.md`
- [X] T015 [US1] Add migration checks for visible TaskList identity and shortcut handlers in `tests/unit/test_tasklist_identity.py`
- [X] T016 [US1] Add a package identity inspection test that validates name, summary, description, category, and window strings in `tests/e2e/test_tasklist_package.py`

**Checkpoint**: User Story 1 is complete and independently testable.

---

## Phase 4: User Story 2 - Separar o conteúdo novo dos resíduos do template (Priority: P1)

**Goal**: Remove old ClipBoardEditor identity and documentation from source, distributed artifacts, and package output.

**Independent Test**: Search the repository and built `.nvda-addon`, then confirm zero old-identity references remain in distributed names, paths, metadata, or documents.

- [X] T017 [P] [US2] Remove old identity values from the generated manifest source or template in `addon/manifest.ini`
- [X] T018 [P] [US2] Replace old project, repository, package, and documentation references in `changelog.md`
- [X] T019 [P] [US2] Rewrite `DocumentaçãoTecnica.md` for the TaskList build, validation, and package workflow
- [X] T020 [P] [US2] Remove old template identity references from repository metadata and release configuration under `.github/workflows/`
- [X] T021 [US2] Add repository-wide old-template residue assertions for paths, metadata, and docs in `tests/unit/test_tasklist_migration.py`
- [X] T022 [US2] Add built-package inspection for old names and paths in `tests/e2e/test_tasklist_package.py`
- [X] T023 [US2] Run `uv run scons` and inspect the single generated `.nvda-addon` package against `specs/001-tasklist-template-migration/quickstart.md`

**Checkpoint**: User Story 2 is complete and independently testable.

---

## Phase 5: User Story 3 - Preservar o comportamento real do TaskList (Priority: P1)

**Goal**: Keep implemented task, list, persistence, keyboard, search, export/import, and recovery behavior consistent with documentation.

**Independent Test**: Run unit and manual flows for task and list operations, legacy data loading, protected lists, import/export failures, and closing/reopening the plugin.

- [X] T024 [P] [US3] Add normalization and persistence tests for `data-model.md` entities `Configuração persistida.settings.soundEnabled`, `Configuração persistida.settings.recentReadCount`, `Configuração persistida.lists`, `Lista.name`, and `Lista.tasks` in `tests/unit/test_tasklist_persistence.py`
- [X] T025 [P] [US3] Add task-model tests for `data-model.md` fields `Tarefa.text`, `Tarefa.priority`, `Tarefa.notes`, `Tarefa.created_at`, `Tarefa.completed_at`, and `Tarefa.origin_list` in `tests/unit/test_tasklist_tasks.py`
- [X] T026 [P] [US3] Add legacy-format load tests covering each format listed under `data-model.md` `Formatos legados aceitos` in `tests/unit/test_tasklist_persistence.py`
- [X] T027 [US3] Verify the implemented dialog, keyboard handlers, and success/failure announcements against `specs/001-tasklist-template-migration/contracts/user-interaction.md` in `addon/globalPlugins/TaskList/__init__.py`
- [X] T028 [US3] Update only documentation or mismatch handling needed to preserve real behavior; do not add unimplemented features in `readme.md`
- [ ] T029 [US3] Add manual runtime validation for task/list creation, editing, priority, notes, completion, reopening, undo, search, export, and import in `specs/001-tasklist-template-migration/quickstart.md`

**Checkpoint**: User Story 3 is complete and independently testable.

---

## Phase 6: User Story 4 - Centralizar os metadados do complemento (Priority: P2)

**Goal**: Make `buildVars.py` the single authoritative source for public package metadata and derived artifacts.

**Independent Test**: Change a test fixture or sample public value in build metadata, rebuild, and verify manifest and package values remain aligned with no conflicting values.

- [X] T030 [P] [US4] Consolidate public product identity in `buildVars.py` and ensure every derived field cites or matches `Complemento TaskList.name`, `summary`, `description`, `version`, `author`, `url`, `sourceURL`, and compatibility in `data-model.md`
- [X] T031 [P] [US4] Ensure `addon/manifest.ini` is generated from `buildVars.py` rather than maintained as a separate source of truth
- [X] T032 [P] [US4] Update project repository URLs and package metadata consistently in `pyproject.toml`
- [X] T033 [US4] Add metadata consistency tests comparing build variables, generated manifest, and package contents in `tests/e2e/test_tasklist_package.py`

**Checkpoint**: User Story 4 is complete and independently testable.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Complete documentation, validation, cleanup, and release checks across all user stories.

- [X] T034 [P] Update localized and generated documentation files under `addon/doc/pt_BR/` and ensure no old user-facing identity remains
- [X] T035 [P] Update final release notes and public compatibility details in `changelog.md`
- [X] T036 [P] Add final package and source scans for forbidden old names under `tests/unit/test_tasklist_migration.py`
- [X] T037 Run `uv run python -m unittest discover -s tests -v`
- [ ] T038 Run `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, and `uv run prek run --all-files`
- [X] T039 Run `uv run scons` and validate the package manifest, name, version, source path `globalPlugins/TaskList/`, documentation, and absence of old-template references
- [ ] T040 Complete manual NVDA and data-preservation validation using `specs/001-tasklist-template-migration/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User stories can proceed in parallel after the foundation is complete.
  - Recommended delivery order is P1 User Story 1, P1 User Story 2, P1 User Story 3, then P2 User Story 4.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependency on other stories after Foundational.
- **User Story 2 (P1)**: No dependency on other stories after Foundational, but package checks depend on final identity changes.
- **User Story 3 (P1)**: No dependency on identity or metadata tasks; validates existing behavior and legacy compatibility.
- **User Story 4 (P2)**: Can proceed after build metadata is established; package checks integrate with US1 and US2.

### Within Each User Story

- Identity and metadata tasks precede package validation.
- Migration residue scans precede final package scan.
- Persistence/model tests precede behavior-preservation documentation changes.
- Core implementation and package build precede manual validation.
- Story complete before moving to the next priority.

### Parallel Opportunities

- T002-T003 can run in parallel in Setup.
- T008-T009 can run in parallel in Foundational after the rename and build configuration.
- T010-T012 can run in parallel once the metadata and rename are complete.
- T017-T020 can run in parallel because they edit separate source files.
- T024-T026 can run in parallel across separate test modules.
- T030-T032 can run in parallel across metadata files.
- T034-T036 can run in parallel for localized docs, release notes, and scans.

---

## Parallel Example: User Story 1

```bash
Task: "T010 [P] [US1] Update public metadata values in buildVars.py"
Task: "T011 [P] [US1] Update window title and visible labels in addon/globalPlugins/TaskList/__init__.py"
Task: "T012 [P] [US1] Verify global gestures and script category in addon/globalPlugins/TaskList/__init__.py"
```

## Parallel Example: User Story 2

```bash
Task: "T017 [P] [US2] Remove old identity values from addon/manifest.ini"
Task: "T018 [P] [US2] Replace old references in changelog.md"
Task: "T019 [P] [US2] Rewrite DocumentaçãoTecnica.md"
Task: "T020 [P] [US2] Remove old references under .github/workflows/"
```

## Parallel Example: User Story 3

```bash
Task: "T024 [P] [US3] Add persistence and settings tests"
Task: "T025 [P] [US3] Add task field tests"
Task: "T026 [P] [US3] Add legacy-format load tests"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Build and inspect the package.
5. Stop and validate User Story 1 independently before residue cleanup.

### Incremental Delivery

1. Complete Setup and Foundational.
2. Add User Story 1 and validate visible TaskList identity.
3. Add User Story 2 and validate no old template residue remains.
4. Add User Story 3 and validate behavior and legacy persistence.
5. Add User Story 4 and validate centralized metadata.
6. Run the Polish phase and release validation.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup and Foundational together.
2. Developer A: User Story 1 identity and documentation.
3. Developer B: User Story 2 residue removal and package scan.
4. Developer C: User Story 3 behavior and persistence tests.
5. Developer D or team member: User Story 4 metadata consistency.
6. Finish with shared Polish validation.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to a specific user story for traceability.
- Each user story is independently completable and testable.
- Verify tests fail before implementation fixes where test-first coverage is added.
- Commit after each task or logical group.
- Stop at each checkpoint to validate the story independently.
