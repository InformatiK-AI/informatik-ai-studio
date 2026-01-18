# Tutorial Completo: InformatiK-AI-meth Framework v6.0

## Tabla de Contenidos

1. [Introduccion](#1-introduccion)
2. [Antes de Empezar](#2-antes-de-empezar)
3. [Flujo de Trabajo Principal](#3-flujo-de-trabajo-principal)
4. [Guia de Comandos](#4-guia-de-comandos)
   - [flow-md-architect](#41-flow-md-architect)
   - [flow-plan](#42-flow-plan)
   - [flow-issue-create](#43-flow-issue-create)
   - [flow-feature-build](#44-flow-feature-build)
   - [flow-feature-tdd](#45-flow-feature-tdd)
   - [flow-feature-rad](#46-flow-feature-rad)
   - [flow-qa-validate](#47-flow-qa-validate)
   - [flow-feedback-fix](#48-flow-feedback-fix)
   - [flow-analyze-bug](#49-flow-analyze-bug)
   - [flow-rollback](#410-flow-rollback)
   - [flow-worktree-recovery](#411-flow-worktree-recovery)
5. [Casos de Uso Completos](#5-casos-de-uso-completos)
6. [Mapa de Interacciones](#6-mapa-de-interacciones)
7. [Recomendaciones y Mejores Practicas](#7-recomendaciones-y-mejores-practicas)
8. [Troubleshooting](#8-troubleshooting)
9. [Referencia Rapida](#9-referencia-rapida)

---

## 1. Introduccion

### Que es InformatiK-AI-meth?

InformatiK-AI-meth es un framework metodologico para desarrollo de software asistido por IA. Proporciona una estructura organizada de comandos, agentes y skills que trabajan en conjunto para automatizar y optimizar el ciclo completo de desarrollo.

### Filosofia del Framework

El framework se basa en tres principios fundamentales:

1. **Orquestacion Inteligente**: Los comandos orquestan agentes especializados que trabajan en capas (database -> API -> backend -> frontend -> seguridad).

2. **Calidad por Diseno**: Seguridad y testing son obligatorios, no opcionales. El `@security-architect` es una puerta (gate) mandatoria.

3. **Automatizacion con Supervision**: El framework automatiza tareas repetitivas pero mantiene al humano en el ciclo de decision.

### Componentes Principales

```
InformatiK-AI-meth/
├── Commands (11)     # Flujos de trabajo orquestados
│   └── flow-*.md     # Cada comando define un workflow completo
│
├── Agents (10)       # Especialistas autonomos de planificacion
│   └── @agent-name   # Invocados con @ (ej: @security-architect)
│
├── Skills (34)       # Herramientas especificas dirigidas por usuario
│   └── /skill-name   # Invocados con / (ej: /code-reviewer)
│
└── DAG (dag.json)    # Grafo de dependencias entre agentes
```

---

## 2. Antes de Empezar

### 2.1 Configuracion Inicial: CLAUDE.md

El archivo `CLAUDE.md` es la "Constitucion" del proyecto. Define:

- Stack tecnologico
- Metodologia de trabajo (TDD, RAD, Standard)
- Equipo de agentes (core_team)
- Requisitos de testing
- Variables de entorno

**Crear CLAUDE.md por primera vez:**

```bash
claude -p .claude/commands/flow-md-architect.md create
```

### 2.2 Pre-requisitos

1. **Claude Code CLI** instalado y configurado
2. **Git** inicializado en el proyecto
3. **VCS Tool** configurado (gh para GitHub, glab para GitLab)
4. **Dependencias** del proyecto instaladas

### 2.3 Estructura de Carpetas

El framework utiliza estas ubicaciones:

```
proyecto/
├── CLAUDE.md                           # Constitucion del proyecto
├── .claude/
│   ├── agents/
│   │   ├── dag.json                    # Grafo de dependencias
│   │   └── *.md                        # Definiciones de agentes
│   ├── commands/
│   │   └── flow-*.md                   # Comandos del framework
│   ├── skills/
│   │   └── {skill-name}/SKILL.md       # Definiciones de skills
│   ├── sessions/
│   │   └── context_session_*.md        # Contexto de sesion
│   ├── docs/
│   │   └── {feature}/                  # Planes de agentes
│   │       ├── database.md
│   │       ├── api_contract.md
│   │       ├── backend.md
│   │       ├── frontend.md
│   │       └── security_plan.md
│   ├── state/
│   │   └── {feature}/                  # Estado persistente
│   │       └── validation_state.json
│   ├── cache/
│   │   └── context_{feature}.json      # Cache de contexto
│   └── logs/                           # Metricas y auditorias
└── .trees/
    └── feature-{name}/                 # Git worktrees
```

---

## 3. Flujo de Trabajo Principal

### Diagrama Visual del Flujo Tipico

```
                         INICIO
                            |
                            v
            +-------------------------------+
            |    /flow-md-architect create  |  <-- Si es proyecto nuevo
            +-------------------------------+
                            |
                            v
            +-------------------------------+
            |         /flow-plan            |  <-- Planificacion estrategica
            +-------------------------------+
                            |
                            v
            +-------------------------------+
            |      /flow-issue-create       |  <-- Crear issue en VCS
            +-------------------------------+
                            |
                            v
            +-------------------------------+
            |      /flow-feature-build      |  <-- Implementacion
            |                               |
            |   +-------+-------+-------+   |
            |   | TDD   |  RAD  |Standard|  |
            +---+-------+-------+-------+---+
                            |
                            v
            +-------------------------------+
            |       /flow-qa-validate       |  <-- Validacion QA
            +-------------------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
        +----------+              +--------------+
        |   PASS   |              |    FAIL      |
        +----------+              +--------------+
              |                           |
              v                           v
        +----------+              +--------------+
        |  MERGE   |              |/flow-feedback|
        +----------+              |    -fix      |
                                  +--------------+
                                         |
                                         v
                                  (Vuelve a QA)
```

### Ciclo de Validacion-Correccion

El framework implementa un ciclo automatico de hasta 3 iteraciones:

```
Iteracion 1 --> QA Fail --> feedback-fix --> Re-QA
Iteracion 2 --> QA Fail --> feedback-fix --> Re-QA
Iteracion 3 --> QA Fail --> ESCALATE TO HUMAN REVIEW
```

---

## 4. Guia de Comandos

### 4.1 flow-md-architect

**Descripcion**: Crea, audita o mejora el archivo CLAUDE.md, la "Constitucion" del proyecto.

**Cuando usarlo**:
- Al iniciar un proyecto nuevo
- Al auditar un proyecto existente
- Para modernizar configuraciones antiguas

**Sintaxis**:

```bash
# Crear nuevo CLAUDE.md
claude -p .claude/commands/flow-md-architect.md create

# Auditar CLAUDE.md existente
claude -p .claude/commands/flow-md-architect.md audit

# Mejorar CLAUDE.md existente
claude -p .claude/commands/flow-md-architect.md improve

# Reemplazar completamente
claude -p .claude/commands/flow-md-architect.md recreate
```

**Agentes y Skills utilizados**:
- Skill: `claude-md-architect` (principal)
- Skill: `hooks-setup` (post-creacion, opcional)

**Fases**:
1. Deteccion de modo y validacion
2. Recopilacion de contexto del proyecto
3. Invocacion del skill claude-md-architect
4. Revision y validacion
5. Post-procesamiento (crear directorios, hooks)

**Ejemplo de uso**:

```
Usuario: Mi proyecto nuevo es una API REST con Node.js y PostgreSQL

Claude ejecuta:
> claude -p .claude/commands/flow-md-architect.md create

El skill analiza el proyecto y genera un CLAUDE.md con:
- [stack]: Node.js, Express, PostgreSQL
- [methodology]: TDD recomendado
- [core_team]: database-architect, api-contract-designer,
               domain-logic-architect, security-architect
```

**Consejos**:
- Siempre ejecutar `audit` antes de `improve` para entender el estado actual
- Despues de crear/recrear, considerar ejecutar `hooks-setup`

---

### 4.2 flow-plan

**Descripcion**: Planificacion estrategica multi-scope (feature, epic, project).

**Cuando usarlo**:
- Antes de implementar cualquier feature
- Para planificar epics (multiples features relacionadas)
- Para roadmaps de proyecto completo

**Sintaxis**:

```bash
# Planificar una feature (scope por defecto)
claude -p .claude/commands/flow-plan.md user-authentication

# Planificar un epic
claude -p .claude/commands/flow-plan.md epic authentication-system

# Planificar un proyecto
claude -p .claude/commands/flow-plan.md project e-commerce-platform
```

**Agentes utilizados** (segun scope):
- **Feature**: core_team + especialistas segun keyword
- **Epic**: + domain-logic-architect, presentation-layer-architect, test-strategy-planner
- **Project**: roster completo de agentes

**Skills utilizados**:
- `brainstorming` (Fase 0.5 - Ideacion)
- `writing-plans` (Fase 4 - Generacion de plan)

**Fases**:
1. Fase 0: Deteccion de scope y parsing
2. Fase 0.5: Ideacion con brainstorming (MANDATORIO)
3. Fase 1: Setup de sesion
4. Fase 2: Lectura de CLAUDE.md
5. Fase 3: Seleccion de equipo (DAG-integrated)
6. Fase 3.5: Ajuste de equipo segun scope
7. Fase 4: Generacion de plan con writing-plans
8. Fase 5: Consejo de agentes (paralelo)
9. Fase 6: Sintesis del plan maestro
10. Fase 7: Clarificacion con usuario

**Outputs**:
- Feature: `.claude/sessions/context_session_feature_{name}.md`
- Epic: `.claude/sessions/context_session_epic_{name}.md`
- Project: `.claude/sessions/context_session_project_{name}.md`
- Brainstorming: `.claude/docs/{name}/brainstorming.md`

**Ejemplo de uso**:

```
Usuario: Necesito planificar un carrito de compras para mi e-commerce

> claude -p .claude/commands/flow-plan.md feature carrito-compras

Resultado:
1. Brainstorming genera ideas y opciones
2. Equipo seleccionado: database-architect, api-contract-designer,
   domain-logic-architect, frontend-architect, security-architect
3. Plan maestro sintetizado en context_session_feature_carrito_compras.md
```

**Consejos**:
- Usar scope `epic` cuando hay 3-5 features relacionadas
- Usar scope `project` para roadmaps y arquitectura inicial
- Revisar el output de brainstorming antes de continuar

---

### 4.3 flow-issue-create

**Descripcion**: Crea issues/tareas en el VCS con estructura profesional incluyendo criterios de aceptacion en Gherkin.

**Cuando usarlo**:
- Despues de completar flow-plan
- Para crear issues trackables en GitHub/GitLab

**Sintaxis**:

```bash
# Path al archivo de sesion del plan
claude -p .claude/commands/flow-issue-create.md .claude/sessions/context_session_feature_carrito.md
```

**Agentes utilizados**:
- `@test-strategy-planner` - Genera test_cases.md

**Skills utilizados**:
- `/acceptance-validator define {feature}` - Refina criterios de aceptacion

**Fases**:
1. Lectura de CLAUDE.md y setup de VCS
2. Generacion de estrategia de test y AC (Gherkin)
3. Draft del issue con estructura profesional
4. Revision con usuario
5. Creacion del issue en VCS

**Estructura del Issue**:

```markdown
### User Story
As a [role], I want [feature], So that [benefit].

### Acceptance Criteria (Gherkin)
Given [context]
When [action]
Then [result]

### Definition of Done
- [ ] Implementation complete
- [ ] Tests passed (NO EXCEPTIONS)
- [ ] QA Validation passed
```

**Ejemplo de uso**:

```
> claude -p .claude/commands/flow-issue-create.md \
    .claude/sessions/context_session_feature_carrito_compras.md

Issue #42 creado:
Titulo: "feat: Implementar carrito de compras"
Body: User story, AC en Gherkin, DoD
Labels: enhancement, feature
```

**Consejos**:
- Siempre ejecutar flow-plan antes para tener un context_session valido
- Revisar el draft antes de confirmar la creacion

---

### 4.4 flow-feature-build

**Descripcion**: El comando principal de implementacion. Orquesta todo el ciclo de desarrollo con soporte para TDD, RAD y Standard.

**Cuando usarlo**:
- Para implementar una feature despues de crear el issue
- Es el comando mas completo del framework

**Sintaxis**:

```bash
# Usando numero de issue
claude -p .claude/commands/flow-feature-build.md 42

# O usando nombre de feature
claude -p .claude/commands/flow-feature-build.md carrito-compras
```

**Agentes utilizados** (segun feature pattern en dag.json):

| Pattern | Agentes en secuencia |
|---------|---------------------|
| backend-only | database -> api-contract -> domain-logic -> security |
| frontend-only | frontend -> security |
| fullstack | database -> api-contract -> [domain-logic || frontend] -> security |
| infrastructure | devops -> security |
| workflow-automation | n8n -> security |

**Agentes MANDATORIOS (siempre)**:
- `@security-architect` - Gate de seguridad (bloquea si no se invoca)
- `@implementation-test-engineer` - Escribir tests

**Skills utilizados**:
- `/preflight-check` - Validacion pre-implementacion
- `/implementation-orchestrator` - Coordinar planes
- `/code-reviewer` - Revision de codigo pre-PR

**Fases Detalladas**:

```
Phase 0: Pre-Flight Check (con retry loop, max 3)
    |
    v
Phase 0.5: Load Shared Context (cache JSON)
    |
    v
Phase 1: Constitution & Setup
    ├── Lee CLAUDE.md
    └── Crea worktree: .trees/feature-{arg}
         (con recovery si existe)
    |
    v
Phase 2: Dynamic Implementation Cycle
    ├── CASE 1: TDD (Strategy -> Red -> Green -> Refactor)
    ├── CASE 2: RAD (Prototype -> Analyze -> Iterate -> Test)
    └── CASE 3: Standard (Plan + Implement + Test)
    |
    v
Phase 1.5: Plan Validation Gate
    ├── Verifica planes existen
    └── Valida coherencia (database <-> API <-> backend <-> frontend)
    |
    v
Phase 3: Validation Loop
    ├── Code Review (dedupe: solo calidad, no security)
    ├── Create PR
    ├── Monitor CI/CD
    ├── QA Validation (flow-qa-validate)
    └── Feedback loop si falla (flow-feedback-fix)
```

**Timeouts configurados**:
- Agentes: 300000ms (5 minutos)
- Skills: 180000ms (3 minutos)
- VCS CLI: 120000ms (2 minutos)
- CI/CD: 600000ms (10 minutos)

**Ejemplo de uso TDD**:

```
> claude -p .claude/commands/flow-feature-build.md 42

Pre-flight check: GO
Worktree creado: .trees/feature-42
CLAUDE.md indica: [methodology].workflow = TDD

TDD Workflow:
  Strategy: @test-strategy-planner genera test_cases.md
  Red: @implementation-test-engineer escribe tests (fallan)
  Green: Agentes implementan codigo minimo
  Refactor: Mejora codigo manteniendo tests verdes

Plan Validation Gate: PASS
Code Review: 2 warnings (documentados en PR)
PR #15 creado
QA Validation: PASS
READY TO MERGE
```

**Consejos**:
- El pre-flight puede auto-remediar problemas comunes
- Si el worktree ya existe, elegir "b) Continue" para resumir trabajo
- Revisar los warnings de Plan Validation antes de continuar

---

### 4.5 flow-feature-tdd

**Descripcion**: Modulo de workflow TDD. NO invocar directamente - es llamado por flow-feature-build.

**Workflow**: Strategy -> Red -> Green -> Refactor

**Fases TDD**:

```
TDD-0: Strategy (Test Planning)
    @test-strategy-planner -> test_cases.md
    GATE: No continuar sin test_cases.md
    |
    v
TDD-1: Red (Write Failing Tests)
    @implementation-test-engineer mode="write_failing_tests"
    Ejecutar tests -> DEBEN FALLAR
    |
    v
TDD-2: Green (Implement Minimum Code)
    Invocar arquitectos segun scope:
    - Backend: @database -> @api-contract -> @domain-logic
    - Frontend: @frontend
    - Fullstack: Paralelo donde posible
    Implementar codigo minimo -> tests DEBEN PASAR
    |
    v
TDD-3: Refactor
    Mejorar codigo manteniendo tests verdes
    @implementation-test-engineer mode="verify_coverage"
```

**Condiciones de exit**:
- **Success**: Todas las fases completas, tests verdes, coverage met
- **Failure**: No puede lograr estado verde despues de 3 intentos

---

### 4.6 flow-feature-rad

**Descripcion**: Modulo de workflow RAD. NO invocar directamente - es llamado por flow-feature-build.

**Workflow**: Prototype -> Analyze -> Iterate (max 3) -> Test

**Configuracion**:
- MAX_RAD_ITERATIONS = 3
- ITERATION_TIMEOUT = 600000ms (10 min/iteracion)

**Fases RAD**:

```
RAD-1: Minimal Viable Prototype
    Arquitectos en modo "guidance" (no bloquean)
    Implementar "happy path" solamente
    Sin polish, sin edge cases
    |
    v
RAD-2: Experience Analysis
    @experience-analyzer:
      - UI project -> UX analysis con Playwright
      - API project -> DX analysis con curl
    Output: experience_analysis_iteration_{N}.md
    |
    v
RAD-3: Decision Point
    IF critical_issues == 0 AND major_issues <= 2:
      SKIP_TO_TESTING
    ELSE IF iteration < 3:
      ITERATE
    ELSE:
      FORCE_TEST
    |
    v
RAD-4: Refinement (Iteration 2, si necesario)
    Arreglar SOLO issues criticos
    NO agregar features nuevas
    Re-analizar
    |
    v
RAD-5: Polish (Iteration 3, opcional)
    Mejoras nice-to-have
    Loading states, animaciones
    Analisis final
    |
    v
RAD-6: Comprehensive Testing
    @test-strategy-planner + @implementation-test-engineer
    Tests cubren todas las iteraciones
```

**Condiciones de exit**:
- **Success**: Testing completo, coverage met
- **Failure**: No estabiliza despues de 3 iteraciones + tests fallan

---

### 4.7 flow-qa-validate

**Descripcion**: Validacion de calidad con ciclo de hasta 3 iteraciones antes de escalar a revision humana.

**Cuando usarlo**:
- Automaticamente invocado por flow-feature-build
- Manualmente para validar PRs existentes

**Sintaxis**:

```bash
# Validar PR
claude -p .claude/commands/flow-qa-validate.md 15
```

**Skills utilizados**:
- `/code-reviewer analyze` - Revision de codigo
- `/acceptance-validator validate {feature}` - Validar AC

**Agentes utilizados**:
- `@security-architect` (modo validacion)

**Fases**:

```
Phase 1: Setup
    Lee CLAUDE.md
    Carga/inicializa validation_state.json
    |
    v
Phase 2: Orchestrate Validation
    Step 1: /code-reviewer (MANDATORIO, pre-merge gate)
    Step 2: PARALELO:
      - /acceptance-validator validate
      - @security-architect validation mode
    |
    v
Phase 3: Review & Decision
    Analiza feedback
    FINAL_STATUS = "READY" o "NEEDS_WORK"
    |
    v
Phase 4: Action
    CASE 1: READY -> Comentar PR, MERGE
    CASE 2: NEEDS_WORK + iteration < 3 -> flow-feedback-fix
    CASE 3: NEEDS_WORK + iteration >= 3 -> ESCALATE TO HUMAN
```

**Estado persistente** (validation_state.json):

```json
{
  "feature_name": "carrito-compras",
  "pr_number": 15,
  "current_iteration": 2,
  "max_iterations": 3,
  "status": "in_progress",
  "validation_history": [
    {"iteration": 1, "status": "failed", "issues": [...]}
  ]
}
```

**Escalacion** (cuando max iterations alcanzado):
1. Comentario en PR
2. Reporte de escalacion estructurado
3. Crear issue de escalacion en GitHub
4. Notificar usuario

**Ejemplo de uso**:

```
> claude -p .claude/commands/flow-qa-validate.md 15

Iteration 2/3
Code Review: PASS
Acceptance Validation: 1 [FAIL] - AC-3 not met
Security Review: PASS

QA VALIDATION FAILED - Triggering feedback loop
Invoking flow-feedback-fix...
```

**Consejos**:
- Revisar validation_history para entender patrones de fallos
- Si un issue persiste en multiples iteraciones, considerar cambio arquitectural

---

### 4.8 flow-feedback-fix

**Descripcion**: Implementa correcciones basadas en feedback de QA, siempre con test-first.

**Cuando usarlo**:
- Automaticamente invocado por flow-qa-validate cuando falla
- Manualmente para PRs que necesitan correccion

**Sintaxis**:

```bash
# Invocacion basica
claude -p .claude/commands/flow-feedback-fix.md 15

# Con estado pre-cargado (optimizado)
claude -p .claude/commands/flow-feedback-fix.md "15 --state-file .claude/state/carrito/validation_state.json --iteration 2"
```

**Agentes utilizados**:
- `@implementation-test-engineer` - Escribir test para el bug

**Fases**:

```
Phase 0: Load State Context
    Parsear argumentos (soporta --state-file, --iteration)
    Cargar validation_history
    Revisar intentos previos (NO repetir approach fallido)
    |
    v
Phase 1: Analysis
    Leer feedback de /acceptance-validator y @security-architect
    Cross-reference con history
    Identificar: nuevos, recurrentes, parcialmente arreglados
    |
    v
Phase 2: Implementation Cycle (NO EXCEPTIONS)
    1. Escribir test que falla (reproduce bug)
    2. Run tests -> Expect FAIL
    3. Implementar fix
    4. Run tests -> Expect PASS
    |
    v
Phase 3: Finalize & Re-validate
    git commit -m "fix: Address QA feedback (iteration N)"
    git push
    Invocar flow-qa-validate automaticamente
```

**Reglas estrictas**:
- NO EXCEPTIONS: Nuevo test para el bug es requerido
- Abordar root causes, no sintomas (especialmente en iteration 2+)
- Siempre re-trigger validation despues de fix

**Ejemplo de uso**:

```
> claude -p .claude/commands/flow-feedback-fix.md 15

Loading iteration 2 from state file
Previous attempts: [iteration 1 failed: missing validation]

Analysis:
- Issue: AC-3 email validation not implemented
- Pattern: NEW (not seen before)

Implementation:
1. Writing failing test for email validation
2. Tests: 1 failing (expected)
3. Implementing validation logic
4. Tests: All passing

Commit: "fix: Add email validation (iteration 2)"
Re-triggering flow-qa-validate...
```

---

### 4.9 flow-analyze-bug

**Descripcion**: Diagnostica bugs con equipo de agentes especialistas.

**Cuando usarlo**:
- Cuando hay un bug reportado sin causa clara
- Antes de crear un issue de fix

**Sintaxis**:

```bash
# Con descripcion del bug
claude -p .claude/commands/flow-analyze-bug.md "login fails with OAuth tokens"
```

**Agentes utilizados**:
- Equipo dinamico basado en keywords
- `@agent-librarian` si se necesita especialista adicional

**Fases**:

```
Phase 1: Setup
    Crear context_session_bug_{ID}.md
    |
    v
Phase 2: Team Selection (Auto-Healing)
    Analizar keywords (ej: "performance", "security", "database")
    Si especialista no existe -> @agent-librarian "scout: $specialist"
    |
    v
Phase 3: Diagnosis
    Agentes investigan
    Sintetizan en bug_diagnosis_report.md:
    - Root Cause
    - Evidence
    - Recommendation
    |
    v
Phase 4: Recommendation
    Presentar reporte al usuario
    Preguntar si crear issue de fix
```

**Output**: `.claude/doc/bug_{ID}/bug_diagnosis_report.md`

**Ejemplo de uso**:

```
> claude -p .claude/commands/flow-analyze-bug.md "OAuth token expiration"

Keywords detected: OAuth, authentication, security
Team selected: security-architect, domain-logic-architect

Diagnosis:
Root Cause: Token refresh not implemented correctly
Evidence: Tokens expire but refresh_token not being used
Recommendation: Implement token refresh interceptor

Create fix issue? [y/n]
```

---

### 4.10 flow-rollback

**Descripcion**: Revierte cambios de una feature, con modos soft y hard.

**Cuando usarlo**:
- Feature abandonada o fallida
- Necesidad de limpiar estado

**Sintaxis**:

```bash
# Soft rollback (default) - preserva commits y PR
claude -p .claude/commands/flow-rollback.md my-feature

# Hard rollback - elimina todo
claude -p .claude/commands/flow-rollback.md my-feature --mode hard
```

**Fases**:

```
Phase 0: Argument Parsing
    Extraer feature_name y mode
    Validar que feature existe
    |
    v
Phase 1: State Analysis
    Verificar: worktree, uncommitted changes, commits, PR, plans
    Mostrar resumen al usuario
    |
    v
Phase 2: Rollback Options
    SOFT: Preservar commits/PR, stash changes, archivar estado
    HARD: Confirmar, cerrar PR, eliminar worktree/branch/state
    |
    v
Phase 3: Cleanup Verification
    Verificar limpieza completa
    Log de accion
```

**Modo SOFT**:
- Preserva commits en branch
- Preserva PR abierto
- Stash uncommitted changes
- Archiva planes a `.claude/archive/{feature}/{timestamp}/`

**Modo HARD** (DESTRUCTIVO):
- Requiere confirmacion explicita: `DELETE {FEATURE_NAME}`
- Cierra PR
- Elimina worktree y branch
- Elimina todos los archivos de estado

**Ejemplo de uso**:

```
> claude -p .claude/commands/flow-rollback.md carrito-compras

Feature Rollback Analysis: carrito-compras
- Worktree: EXISTS
- Uncommitted changes: 3 files
- Commits on branch: 5
- Open PR: #15
- Agent plans: EXIST

Rollback Mode: soft

Soft rollback complete!
- Stashed changes: rollback-stash-20260117
- Plans archived to .claude/archive/carrito-compras/20260117/

To resume later:
  git worktree add .trees/feature-carrito-compras feature-carrito-compras
  git stash pop
```

---

### 4.11 flow-worktree-recovery

**Descripcion**: Modulo de recuperacion de worktrees. NO invocar directamente - es llamado por flow-feature-build.

**Cuando se activa**:
- Cuando `git worktree add` falla porque el worktree ya existe

**Fases**:

```
WR-1: Detect Existing Worktree
    git worktree list | grep "feature-{ARG}"
    |
    v
WR-2: Analyze Worktree State
    - Last commit date
    - Uncommitted changes count
    - Branch status
    - Sync status (ahead/behind)
    |
    v
WR-3: Present Recovery Options
    a) Delete and recreate (FRESH START)
    b) Continue in existing (RESUME)
    c) Abort command (EXIT)
    |
    v
WR-4: Handle User Choice
    a) Force remove worktree, delete branch, create fresh
    b) cd to existing, show status, continue
    c) Exit with cleanup instructions
    |
    v
WR-5: Log Recovery Metrics
```

**Ejemplo de output**:

```
Worktree already exists: .trees/feature-42

Worktree Info:
- Last commit: 2 hours ago
- Uncommitted changes: 5 files
- Branch: feature-42
- Sync status: [ahead 3]

Recovery Options:
a) Delete and recreate (FRESH START)
b) Continue in existing worktree (RESUME)
c) Abort command (EXIT)

Choose option (a/b/c):
```

---

## 5. Casos de Uso Completos

### Caso 1: Desarrollar Feature "Carrito de Compras" (E-commerce)

**Contexto**: Proyecto e-commerce existente con CLAUDE.md configurado.

**Flujo completo**:

```
Paso 1: Planificacion
> claude -p .claude/commands/flow-plan.md feature carrito-compras

  Brainstorming genera:
  - Opciones de almacenamiento (localStorage vs DB)
  - Integracion con inventario
  - Calculo de precios/descuentos

  Equipo seleccionado: database-architect, api-contract-designer,
                       domain-logic-architect, frontend-architect,
                       security-architect

  Plan maestro: context_session_feature_carrito_compras.md

Paso 2: Crear Issue
> claude -p .claude/commands/flow-issue-create.md \
    .claude/sessions/context_session_feature_carrito_compras.md

  Issue #42 creado con:
  - User Story
  - AC en Gherkin (add to cart, remove, calculate total, checkout)
  - Definition of Done

Paso 3: Implementacion
> claude -p .claude/commands/flow-feature-build.md 42

  Pre-flight: GO
  Worktree: .trees/feature-42 creado
  Workflow: TDD (segun CLAUDE.md)

  TDD Cycle:
  - Strategy: test_cases.md con 15 escenarios
  - Red: 15 tests fallando
  - Green: Implementacion minima
    - database.md: Cart, CartItem tables
    - api_contract.md: POST/DELETE /cart, GET /cart
    - backend.md: CartService, CartController
    - frontend.md: CartContext, CartItem component
  - Refactor: Mejoras de codigo

  Plan Validation Gate: PASS
  PR #15 creado

Paso 4: QA Validation
> flow-qa-validate (automatico)

  Iteration 1/3:
  - Code Review: 1 warning (missing JSDoc)
  - Acceptance Validator: PASS
  - Security Review: PASS

  QA VALIDATION PASSED - READY TO MERGE

Paso 5: Merge
  PR #15 merged to main
```

---

### Caso 2: Bug Critico en Autenticacion OAuth

**Contexto**: Bug reportado: "Usuarios deslogueados despues de 1 hora"

```
Paso 1: Analisis del Bug
> claude -p .claude/commands/flow-analyze-bug.md "OAuth tokens expire after 1 hour"

  Keywords: OAuth, tokens, authentication, security
  Team: security-architect, domain-logic-architect

  Diagnosis Report:
  - Root Cause: refresh_token not being used when access_token expires
  - Evidence: AuthInterceptor only checks access_token validity
  - Recommendation: Implement token refresh flow

  Create fix issue? [y]
  Issue #43 created: "fix: Implement OAuth token refresh"

Paso 2: Implementar Fix
> claude -p .claude/commands/flow-feature-build.md 43

  Pre-flight: GO
  Workflow: TDD

  TDD Cycle:
  - Strategy: test para token expiration y refresh
  - Red: Test falla (refresh no implementado)
  - Green: Implementar refresh logic en AuthInterceptor
  - Refactor: Clean up

  PR #16 created

Paso 3: QA Validation
  Iteration 1/3: FAIL - refresh not working for edge case
  Invoking flow-feedback-fix...

  Iteration 2/3: PASS
  READY TO MERGE

Paso 4: Merge
  PR #16 merged
  Bug fix deployed
```

---

### Caso 3: Feature con TDD - Sistema de Pagos Stripe

**Contexto**: Integrar pagos con Stripe

```
Paso 1: Planificar
> claude -p .claude/commands/flow-plan.md feature pagos-stripe

  Brainstorming:
  - Webhooks vs polling para confirmacion
  - Manejo de refunds
  - Compliance PCI

  Plan generado con dependencias:
  api-contract -> domain-logic -> security (critico para pagos)

Paso 2: Issue
> claude -p .claude/commands/flow-issue-create.md \
    .claude/sessions/context_session_feature_pagos_stripe.md

  Issue #50: AC incluye:
  - Given valid payment info, When process payment, Then create PaymentIntent
  - Given webhook event, When payment_intent.succeeded, Then update order status

Paso 3: Implementar con TDD
> claude -p .claude/commands/flow-feature-build.md 50

  TDD-0 Strategy:
    test_cases.md con escenarios:
    - Successful payment
    - Declined card
    - Network error
    - Webhook processing
    - Refund flow

  TDD-1 Red:
    @implementation-test-engineer escribe:
    - PaymentService.test.ts
    - StripeWebhook.test.ts
    Tests: 12 failing

  TDD-2 Green:
    @api-contract-designer: POST /payments, POST /webhooks/stripe
    @domain-logic-architect: PaymentService, WebhookHandler
    @security-architect: OWASP review, PCI compliance notes

    Implementacion:
    - StripeService wrapper
    - PaymentController
    - WebhookSignatureValidator

    Tests: 12 passing

  TDD-3 Refactor:
    - Extract StripeClient
    - Add retry logic
    Tests: still 12 passing

  Security Gate: PASS (with 2 recommendations documented)

Paso 4: QA
  PASS on iteration 1
  PR merged
```

---

### Caso 4: Prototipo Rapido con RAD - Dashboard Analytics

**Contexto**: CEO quiere ver demo de dashboard en 2 dias

```
Paso 1: Plan
> claude -p .claude/commands/flow-plan.md feature dashboard-analytics

  Scope: Frontend-heavy con API calls a analytics existente

Paso 2: Build con RAD
> claude -p .claude/commands/flow-feature-build.md dashboard-analytics

  Workflow detectado: RAD (CLAUDE.md config para prototypes)

  RAD-1 Prototype:
    @frontend-architect en modo "guidance"
    Implementacion rapida:
    - Dashboard layout
    - Chart components (happy path only)
    - API integration basica

  RAD-2 Analysis:
    @experience-analyzer (UX mode):
    - CRITICAL: Charts not responsive on mobile
    - MAJOR: No loading states
    - MINOR: Color contrast could improve

  RAD-3 Decision: ITERATE (critical issues)

  RAD-4 Refinement (Iteration 2):
    - Fix responsive charts
    - Add loading states
    Re-analysis:
    - MAJOR: Export button not discoverable
    - MINOR: Animation jank

  RAD-3 Decision: SKIP_TO_TESTING (acceptable)

  RAD-6 Testing:
    Tests escritos para:
    - Chart rendering
    - Responsive behavior
    - Loading states

  PR created, QA passed

Demo exitosa!
```

---

### Caso 5: Auditar y Mejorar Proyecto Existente

**Contexto**: Proyecto legacy sin CLAUDE.md, estructura desorganizada

```
Paso 1: Auditar CLAUDE.md (o ausencia)
> claude -p .claude/commands/flow-md-architect.md audit

  Output:
  - CLAUDE.md: NOT FOUND
  - Detected: package.json (Node.js), prisma/ (PostgreSQL)
  - Recommendation: Create CLAUDE.md with detected stack

Paso 2: Crear CLAUDE.md
> claude -p .claude/commands/flow-md-architect.md create

  claude-md-architect skill analiza proyecto:
  - Framework: Express.js
  - Database: PostgreSQL con Prisma
  - Testing: Jest (existente pero incompleto)

  CLAUDE.md generado con:
  - [stack]: Node.js, Express, PostgreSQL, Prisma
  - [methodology]: Standard (proyecto existente)
  - [core_team]: database-architect, api-contract-designer,
                 domain-logic-architect, security-architect
  - [testing]: Jest, coverage 70% target

Paso 3: Setup Hooks
> claude -p .claude/commands/hooks-setup (interactivo)

  Configura:
  - pre-commit: lint-staged
  - commit-msg: commitlint
  - Claude hooks: PostToolUse linting

Paso 4: Mejorar CLAUDE.md
> claude -p .claude/commands/flow-md-architect.md improve

  Recommendations:
  - Add [environments] section for staging/prod
  - Define [conventions] for code style
  - Add [deployment] section

  Updated CLAUDE.md con secciones adicionales

Proyecto ahora listo para usar framework completo.
```

---

## 6. Mapa de Interacciones

### 6.1 Tabla de Comandos, Agentes y Skills

| Comando | Agentes Usados | Skills Usados |
|---------|---------------|---------------|
| `flow-md-architect` | - | `claude-md-architect`, `hooks-setup` (opcional) |
| `flow-plan` | DAG segun scope + `@agent-librarian` (si falta) | `brainstorming`, `writing-plans` |
| `flow-issue-create` | `@test-strategy-planner` | `/acceptance-validator define` |
| `flow-feature-build` | DAG completo + `@security-architect` (mandatorio) | `/preflight-check`, `/implementation-orchestrator`, `/code-reviewer` |
| `flow-feature-tdd` | `@test-strategy-planner`, `@implementation-test-engineer`, arquitectos | - |
| `flow-feature-rad` | Arquitectos (guidance), `@experience-analyzer`, `@test-strategy-planner`, `@implementation-test-engineer` | - |
| `flow-qa-validate` | `@security-architect` (validation mode) | `/code-reviewer`, `/acceptance-validator validate` |
| `flow-feedback-fix` | `@implementation-test-engineer` | - |
| `flow-analyze-bug` | Dinamico segun especialidad + `@agent-librarian` | - |
| `flow-rollback` | - | - |
| `flow-worktree-recovery` | - | - |

### 6.2 Diagrama de Dependencias (DAG)

```
Layer 1:           Layer 2:              Layer 3:              Layer 4:         Layer 5:           Layer 6:
                                         (PARALELO)
+----------+       +-------------+       +--------------+
| database |------>| api-contract|------>| domain-logic |--+
| architect|       | designer    |       | architect    |  |
+----------+       +-------------+       +--------------+  |
                          |                                |   +----------+    +-------------+    +------------+
                          |              +--------------+  +-->| security |    | test-strat  |    | experience |
                          +------------->| frontend     |--+   | architect|    | planner     |    | analyzer   |
                                         | architect    |  |   +----------+    +-------------+    +------------+
                                         +--------------+  |        |               |
                          +-------------+                  |        v               v
                          |   devops    |------------------+   (MANDATORY     +-------------+
                          |  architect  |                       GATE)         | impl-test   |
                          +-------------+                                     | engineer    |
                                                                              +-------------+
                          +-------------+
                          | n8n         |------------------+
                          | architect   |                  |
                          +-------------+                  |
                                                          |
                                    (Todos convergen en security-architect)
```

### 6.3 Feature Patterns

**backend-only**:
```
database-architect -> api-contract-designer -> domain-logic-architect -> security-architect
```

**frontend-only**:
```
frontend-architect -> security-architect
```

**fullstack**:
```
database-architect -> api-contract-designer -> [domain-logic-architect || frontend-architect] -> security-architect
                                               (paralelo)
```

**infrastructure**:
```
devops-architect -> security-architect
```

**workflow-automation**:
```
n8n-architect -> security-architect
```

### 6.4 Agentes y sus Outputs

| Agente | Output | Usado por |
|--------|--------|-----------|
| `@database-architect` | `database.md` | api-contract-designer, domain-logic-architect |
| `@api-contract-designer` | `api_contract.md` | domain-logic-architect, frontend-architect |
| `@domain-logic-architect` | `backend.md` | security-architect, implementation |
| `@frontend-architect` | `frontend.md` | security-architect, implementation |
| `@devops-architect` | `devops.md` | security-architect |
| `@security-architect` | `security_plan.md` | Plan Validation Gate (BLOCKER) |
| `@test-strategy-planner` | `test_cases.md` | implementation-test-engineer |
| `@implementation-test-engineer` | Test files | QA validation |
| `@experience-analyzer` | `experience_analysis.md` | RAD iterations |
| `@n8n-architect` | `n8n-workflow-plan.md` | security-architect |

---

## 7. Recomendaciones y Mejores Practicas

### 7.1 Orden Recomendado de Comandos

**Para proyecto nuevo**:
```
1. flow-md-architect create   # Configurar proyecto
2. (opcional) hooks-setup     # Configurar hooks
3. flow-plan                  # Planificar feature
4. flow-issue-create          # Crear issue
5. flow-feature-build         # Implementar
6. (automatico) flow-qa-validate
```

**Para feature en proyecto existente**:
```
1. flow-plan                  # Planificar
2. flow-issue-create          # Crear issue
3. flow-feature-build         # Implementar
```

**Para bug fix**:
```
1. flow-analyze-bug           # Diagnosticar
2. flow-feature-build (issue) # Implementar fix
```

### 7.2 Cuando Usar TDD vs RAD

**Usar TDD cuando**:
- Logica de negocio compleja
- Integraciones criticas (pagos, auth)
- Codigo que debe ser robusto
- Refactoring de sistema existente

**Usar RAD cuando**:
- Prototipos y demos
- Features UI-heavy
- Exploracion de UX
- Time-to-market es prioridad

**Workflow por defecto** (configurar en CLAUDE.md):
```yaml
[methodology]
workflow = TDD  # o RAD o Standard
```

### 7.3 Como Manejar Fallos de QA

**Iteration 1 fail**:
- Normal. Revisar feedback y corregir.

**Iteration 2 fail**:
- Revisar validation_history
- Verificar que no estas repitiendo approach fallido
- Considerar root cause vs sintoma

**Iteration 3 fail (escalation)**:
- El sistema escala automaticamente
- Revisar el escalation report
- Considerar:
  - Cambio arquitectural necesario?
  - Requisitos mal entendidos?
  - Test flaky?

### 7.4 Consejos de Productividad

1. **Pre-flight es tu amigo**: Si falla, deja que auto-remedie antes de investigar

2. **Resume worktrees**: Si interrumpiste trabajo, usa opcion "b) Continue"

3. **Brainstorming no es opcional**: La ideacion mejora calidad del plan

4. **Confiar en el DAG**: El orden de agentes esta optimizado

5. **Revisar planes antes de implementar**: Plan Validation Gate existe por algo

6. **No saltear security-architect**: Es gate mandatorio por buenas razones

7. **Usar soft rollback primero**: Siempre puedes hacer hard despues

8. **Metricas son utiles**: Revisar logs para entender patrones

---

## 8. Troubleshooting

### 8.1 Errores Comunes y Soluciones

#### Pre-flight check falla repetidamente

**Sintoma**: Pre-flight NO-GO despues de 3 intentos

**Posibles causas**:
1. Dependencias no instaladas
2. CLAUDE.md incompleto
3. Agentes faltantes

**Solucion**:
```bash
# 1. Verificar dependencias
npm install  # o equivalente

# 2. Auditar CLAUDE.md
claude -p .claude/commands/flow-md-architect.md audit

# 3. Si falta agente, agent-librarian lo draft
# El pre-flight intenta auto-fix esto
```

#### Worktree ya existe

**Sintoma**: Error al crear worktree

**Solucion**: El flow-worktree-recovery se activa automaticamente. Elegir:
- a) Fresh start si quieres empezar de nuevo
- b) Resume si quieres continuar trabajo previo

#### Plan Validation Gate falla

**Sintoma**: Coherence errors entre planes

**Posibles causas**:
1. Tipos no coinciden (database vs API)
2. Endpoints sin handlers
3. Frontend llama endpoint inexistente

**Solucion**:
```
1. Revisar mensajes de error especificos
2. Re-invocar agentes afectados con correccion
3. Re-validar
```

#### QA escala a human review

**Sintoma**: Iteration 3 fail, issue de escalacion creado

**Solucion**:
```
1. Leer escalation report (tiene root cause analysis)
2. Identificar persistent issues
3. Considerar:
   - Cambio arquitectural
   - Revision de requisitos
   - Sesion de code review manual
```

#### Security-architect bloquea

**Sintoma**: OWASP issues detectados

**Solucion**:
```
1. Leer security_plan.md
2. Identificar issues CRITICAL vs WARNING
3. Arreglar CRITICAL antes de continuar
4. WARNINGs pueden documentarse y aceptarse
```

### 8.2 Como Recuperarse de Fallos

#### Feature a medio implementar

```bash
# Opcion 1: Continuar
claude -p .claude/commands/flow-feature-build.md {feature}
# Elegir "b) Continue in existing worktree"

# Opcion 2: Soft rollback y replanificar
claude -p .claude/commands/flow-rollback.md {feature}
# Luego flow-plan de nuevo
```

#### Estado corrupto

```bash
# Limpiar estado
rm -rf .claude/state/{feature}/
rm -rf .claude/cache/context_{feature}.json

# Re-ejecutar
claude -p .claude/commands/flow-feature-build.md {feature}
```

#### Git worktree corrupto

```bash
# Forzar limpieza
git worktree remove .trees/feature-{name} --force
git branch -D feature-{name}

# Re-crear
claude -p .claude/commands/flow-feature-build.md {name}
```

---

## 9. Referencia Rapida

### 9.1 Tabla de Comandos

| Comando | Proposito | Sintaxis |
|---------|-----------|----------|
| `flow-md-architect` | Gestionar CLAUDE.md | `flow-md-architect.md create\|audit\|improve\|recreate` |
| `flow-plan` | Planificar feature/epic/project | `flow-plan.md [scope] name` |
| `flow-issue-create` | Crear issue en VCS | `flow-issue-create.md path/to/session.md` |
| `flow-feature-build` | Implementar feature | `flow-feature-build.md issue_number` |
| `flow-qa-validate` | Validar PR | `flow-qa-validate.md pr_number` |
| `flow-feedback-fix` | Corregir por feedback | `flow-feedback-fix.md pr_number` |
| `flow-analyze-bug` | Diagnosticar bug | `flow-analyze-bug.md "bug description"` |
| `flow-rollback` | Revertir feature | `flow-rollback.md feature [--mode soft\|hard]` |

### 9.2 Cheatsheet de Invocacion

```bash
# === CONFIGURACION ===
claude -p .claude/commands/flow-md-architect.md create
claude -p .claude/commands/flow-md-architect.md audit
claude -p .claude/commands/flow-md-architect.md improve

# === PLANIFICACION ===
claude -p .claude/commands/flow-plan.md mi-feature
claude -p .claude/commands/flow-plan.md epic mi-epic
claude -p .claude/commands/flow-plan.md project mi-proyecto

# === DESARROLLO ===
claude -p .claude/commands/flow-issue-create.md .claude/sessions/context_session_feature_x.md
claude -p .claude/commands/flow-feature-build.md 42

# === VALIDACION ===
claude -p .claude/commands/flow-qa-validate.md 15
claude -p .claude/commands/flow-feedback-fix.md 15

# === DIAGNOSTICO ===
claude -p .claude/commands/flow-analyze-bug.md "error description"

# === LIMPIEZA ===
claude -p .claude/commands/flow-rollback.md feature-name
claude -p .claude/commands/flow-rollback.md feature-name --mode hard
```

### 9.3 Agentes (invocacion con @)

| Agente | Trigger Keywords |
|--------|------------------|
| `@database-architect` | database, schema, migration, tables |
| `@api-contract-designer` | API, endpoints, OpenAPI, GraphQL |
| `@domain-logic-architect` | backend, business logic, services |
| `@frontend-architect` | UI, frontend, components, React |
| `@devops-architect` | deployment, CI/CD, infrastructure |
| `@security-architect` | SIEMPRE (mandatorio) |
| `@test-strategy-planner` | tests, QA, coverage |
| `@implementation-test-engineer` | write tests |
| `@experience-analyzer` | UX, DX, usability |
| `@n8n-architect` | workflow, automation, n8n |

### 9.4 Skills (invocacion con /)

| Skill | Uso |
|-------|-----|
| `/acceptance-validator define {f}` | Definir AC |
| `/acceptance-validator validate {f}` | Validar AC |
| `/preflight-check` | Validacion pre-build |
| `/code-reviewer analyze` | Revision de codigo |
| `/implementation-orchestrator` | Coordinar planes |
| `/brainstorming` | Ideacion creativa |
| `/writing-plans` | Generar planes |
| `/claude-md-architect` | Gestionar CLAUDE.md |
| `/hooks-setup` | Configurar hooks |

### 9.5 Ubicaciones de Archivos

| Tipo | Ubicacion |
|------|-----------|
| Constitucion | `CLAUDE.md` |
| Sesiones | `.claude/sessions/context_session_*.md` |
| Planes | `.claude/docs/{feature}/*.md` |
| Estado | `.claude/state/{feature}/validation_state.json` |
| Cache | `.claude/cache/context_{feature}.json` |
| Logs | `.claude/logs/` |
| Worktrees | `.trees/feature-{name}/` |
| Archivos | `.claude/archive/{feature}/{timestamp}/` |

---

## Version del Tutorial

**Version**: 1.0.0
**Fecha**: 2026-01-17
**Basado en**: InformatiK-AI-meth Framework v6.0
**Comandos documentados**: 11
**Agentes referenciados**: 10
**Skills referenciados**: 34

---

*Este tutorial fue generado para proporcionar una guia completa del framework InformatiK-AI-meth. Para actualizaciones, consultar los archivos fuente en `.claude/commands/` y `.claude/agents/`.*
