# Agent Dependency Graph (DAG)

## Overview

This document defines the execution order and dependencies between specialist agents during feature implementation. The dependency graph ensures that agents are invoked in the correct sequence, preventing architectural inconsistencies.

## Dependency Graph Visualization

```
┌─────────────────────┐
│ database-architect  │ (Step 1: No dependencies)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│ api-contract-designer   │ (Step 2: Depends on database)
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ domain-logic-architect  │ (Step 3: Depends on API contract)
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────────┐
│ presentation-layer-architect │ (Step 4: Depends on backend)
└──────────┬───────────────────┘
           │
           ▼
┌─────────────────────────┐
│ ui-component-architect  │ (Step 5: Depends on frontend)
└─────────────────────────┘
```

## Dependency Rules

### Layer 1: Database (Foundation)
**Agent**: `database-architect`
**Dependencies**: None
**Outputs**: `database.md`

**Why First?**
- Database schema defines the fundamental data structures
- All upper layers (API, backend, frontend) depend on database models
- Schema changes have the broadest impact on the system

**What It Defines:**
- Tables/collections
- Fields and data types
- Relationships (foreign keys, associations)
- Indexes and constraints
- Migrations strategy

---

### Layer 2: API Contract (Interface)
**Agent**: `api-contract-designer`
**Dependencies**: `database-architect`
**Outputs**: `api_contract.md`

**Why Second?**
- API contracts expose database entities to external consumers
- Request/response schemas must align with database types
- Defines the "contract" that backend must implement

**What It Defines:**
- Endpoints (REST), Queries/Mutations (GraphQL), Services (gRPC)
- Request schemas (input validation)
- Response schemas (output format)
- Authentication and authorization
- Error codes and formats

**Dependency on Database:**
- API schemas use database field names and types
- API relationships mirror database relationships
- Data transformations (DB → API format) must be consistent

---

### Layer 3: Backend/Business Logic (Implementation)
**Agent**: `domain-logic-architect`
**Dependencies**: `api-contract-designer`
**Outputs**: `backend.md`

**Why Third?**
- Backend implements the API contract defined in Layer 2
- Business logic transforms database data according to API schemas
- Acts as the bridge between database and API

**What It Defines:**
- Services and business logic
- API route handlers
- Data access layer (repositories, queries)
- Business rules and validations
- Error handling

**Dependency on API Contract:**
- Each API endpoint requires a backend handler
- Request validation follows API contract schemas
- Response transformations match API contract formats
- Error responses use API-defined error codes

---

### Layer 4: Frontend/Presentation (Consumer)
**Agent**: `presentation-layer-architect`
**Dependencies**: `domain-logic-architect`
**Outputs**: `frontend.md`

**Why Fourth?**
- Frontend consumes the API provided by backend
- State management structures align with API responses
- User interactions trigger API calls defined in backend

**What It Defines:**
- Page/route structure
- State management (Redux, Context, etc.)
- API client integration
- Data fetching and mutations
- Form handling and validation

**Dependency on Backend:**
- Frontend calls APIs implemented in backend
- API client uses endpoints from API contract
- State shapes match API response schemas
- Error handling covers backend error codes

---

### Layer 5: UI Components (Visual Layer)
**Agent**: `ui-component-architect`
**Dependencies**: `presentation-layer-architect`
**Outputs**: `ui_components.md`

**Why Fifth (Last)?**
- UI components are used by frontend pages/routes
- Component props align with frontend data structures
- Visual elements depend on underlying data flow

**What It Defines:**
- Component library (Button, Input, Card, etc.)
- Component props and API
- Design system implementation
- Component composition patterns

**Dependency on Frontend:**
- Components receive data from frontend state
- Component props match frontend data structures
- Event handlers integrate with frontend logic

---

## Execution Order Examples

### Example 1: Full-Stack Feature (All Layers)

**Feature**: User Authentication

**Execution Order:**
1. **database-architect** → Create `users` table with fields: `id`, `email`, `password_hash`, `created_at`
2. **api-contract-designer** → Define API endpoints: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`
3. **domain-logic-architect** → Implement `AuthService` with password hashing, JWT generation, session management
4. **presentation-layer-architect** → Create `LoginPage`, `RegisterPage`, `useAuth` hook for state management
5. **ui-component-architect** → Build `LoginForm`, `RegisterForm` components with validation

**Dependencies Flow:**
```
users table → API schemas (email, password) → AuthService → useAuth hook → LoginForm
```

---

### Example 2: Backend-Only Feature (Subset)

**Feature**: Email Notification Service

**Execution Order:**
1. **api-contract-designer** → Define `POST /notifications/send` endpoint
2. **domain-logic-architect** → Implement `EmailService` with SMTP integration

**Skipped Layers:**
- Database (no new tables needed)
- Frontend (backend-only service)
- UI Components (no UI changes)

---

### Example 3: Frontend-Only Feature (UI Enhancement)

**Feature**: Add Dark Mode Toggle

**Execution Order:**
1. **presentation-layer-architect** → Add theme state to context, implement theme switching logic
2. **ui-component-architect** → Create `ThemeToggle` component

**Skipped Layers:**
- Database (no data changes)
- API Contract (no API changes)
- Backend (no backend logic)

---

## Conditional Execution

Not all features require all agents. The orchestrator detects which agents are needed based on available plan files:

```python
if "database.md" exists → invoke database-architect
if "api_contract.md" exists → invoke api-contract-designer (after database)
if "backend.md" exists → invoke domain-logic-architect (after API)
if "frontend.md" exists → invoke presentation-layer-architect (after backend)
if "ui_components.md" exists → invoke ui-component-architect (after frontend)
```

## Validation Between Layers

After each layer, the orchestrator validates coherence with previous layers:

### Database → API Validation
- ✅ Field names compatible (snake_case DB → camelCase API)
- ✅ Data types compatible (UUID → string, INT → number)
- ✅ Required fields present in both layers

### API → Backend Validation
- ✅ All API endpoints have backend handlers
- ✅ Request schemas match backend input validation
- ✅ Response schemas match backend output format

### Backend → Frontend Validation
- ✅ Frontend API calls match backend endpoints
- ✅ Request payloads match API contract
- ✅ Frontend handles all API responses and errors

### Frontend → UI Validation
- ✅ All UI components referenced in frontend exist
- ✅ Component props match frontend data structures
- ✅ Design system conventions consistent

## Parallel Execution (NOT Supported)

Agents **cannot** be executed in parallel due to strict dependencies. Each layer builds upon the previous:

**❌ Invalid**: Running `api-contract-designer` and `database-architect` in parallel
- API contract needs database schema to define correct types

**❌ Invalid**: Running `domain-logic-architect` before `api-contract-designer`
- Backend needs API contract to implement correct endpoints

**✅ Valid**: Sequential execution following DAG order

## Handling Missing Agents

If a required agent is missing from `.claude/agents/`, the orchestrator uses `@agent-librarian` to:

1. **Scout Mode**: Search for public/community version of the agent
2. **Interview Mode**: Draft a new agent based on project requirements
3. **Halt Execution**: Wait for user to review and approve the new agent

## Integration with flow-feature-build

The dependency graph is enforced in **Phase 1.5: Plan Validation Gate** of `flow-feature-build.md`:

1. All agents generate their plans
2. Orchestrator validates execution order
3. Orchestrator validates cross-layer coherence
4. Unified plan is generated with correct sequence
5. Implementation follows the DAG order

## References

- `orchestrate.py` - Implements topological sort for DAG execution
- `validate_plans.py` - Validates cross-layer coherence
- `SKILL.md` - Main orchestrator skill documentation

---

**Version**: 1.0.0
**Last Updated**: 2026-01-13
