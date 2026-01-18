# Database Schema - InformatiK-AI Studio

> Referenced from: CLAUDE.md [modular_index]
> Load when: Working on database changes, data modeling

## Overview

**Database**: PostgreSQL (via Supabase)
**Client**: @supabase/supabase-js
**Migration Tool**: Supabase CLI

## Entity Relationship Diagram

```
┌──────────────────┐     ┌──────────────────┐
│      users       │────<│     projects     │
│  (auth.users)    │     │                  │
├──────────────────┤     ├──────────────────┤
│ id (PK)          │     │ id (PK)          │
│ email            │     │ user_id (FK)     │
│ created_at       │     │ name             │
│ updated_at       │     │ description      │
└──────────────────┘     │ template         │
                         │ created_at       │
                         │ updated_at       │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  project_files   │ │   generations    │ │   deployments    │
├──────────────────┤ ├──────────────────┤ ├──────────────────┤
│ id (PK)          │ │ id (PK)          │ │ id (PK)          │
│ project_id (FK)  │ │ project_id (FK)  │ │ project_id (FK)  │
│ path             │ │ prompt           │ │ provider         │
│ content          │ │ model            │ │ url              │
│ language         │ │ tokens_input     │ │ status           │
│ created_at       │ │ tokens_output    │ │ created_at       │
│ updated_at       │ │ created_at       │ └──────────────────┘
└──────────────────┘ └──────────────────┘
```

## Tables

### projects

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Primary identifier |
| user_id | UUID | FK(auth.users), NOT NULL | Owner reference |
| name | VARCHAR(100) | NOT NULL | Project name |
| description | TEXT | NULL | Project description |
| template | VARCHAR(50) | NOT NULL, DEFAULT 'blank' | Template used |
| settings | JSONB | DEFAULT '{}' | Project settings |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

**Indexes**:
- `idx_projects_user_id` on `user_id`
- `idx_projects_created_at` on `created_at DESC`

**RLS Policies**:
```sql
-- Users can only see their own projects
CREATE POLICY "Users can view own projects" ON projects
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own projects" ON projects
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects" ON projects
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects" ON projects
  FOR DELETE USING (auth.uid() = user_id);
```

---

### project_files

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | File identifier |
| project_id | UUID | FK(projects), NOT NULL | Parent project |
| path | VARCHAR(500) | NOT NULL | File path (e.g., src/App.tsx) |
| content | TEXT | NOT NULL | File content |
| language | VARCHAR(50) | NOT NULL | Language for highlighting |
| is_entry | BOOLEAN | DEFAULT false | Is entry point file |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update |

**Indexes**:
- `idx_project_files_project_id` on `project_id`
- `idx_project_files_path` on `(project_id, path)` UNIQUE

**RLS Policies**:
```sql
-- Access through project ownership
CREATE POLICY "Access via project" ON project_files
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM projects
      WHERE projects.id = project_files.project_id
      AND projects.user_id = auth.uid()
    )
  );
```

---

### generations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Generation identifier |
| project_id | UUID | FK(projects), NOT NULL | Related project |
| prompt | TEXT | NOT NULL | User prompt |
| prompt_hash | VARCHAR(64) | NOT NULL | SHA256 of prompt |
| model | VARCHAR(50) | NOT NULL | Model used |
| tokens_input | INT | NOT NULL | Input tokens |
| tokens_output | INT | NOT NULL | Output tokens |
| duration_ms | INT | NOT NULL | Generation time |
| status | VARCHAR(20) | NOT NULL | completed/failed/cancelled |
| error_message | TEXT | NULL | Error if failed |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_generations_project_id` on `project_id`
- `idx_generations_created_at` on `created_at DESC`

**RLS Policies**: Same pattern as project_files (via project ownership)

---

### deployments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Deploy identifier |
| project_id | UUID | FK(projects), NOT NULL | Related project |
| provider | VARCHAR(20) | NOT NULL | vercel/netlify |
| url | VARCHAR(500) | NULL | Deployed URL |
| status | VARCHAR(20) | NOT NULL | pending/building/deployed/failed |
| build_log | TEXT | NULL | Build output |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation time |
| completed_at | TIMESTAMPTZ | NULL | Completion time |

**Indexes**:
- `idx_deployments_project_id` on `project_id`
- `idx_deployments_status` on `status`

---

## Migrations

### Running Migrations

```bash
# Generate migration
supabase migration new add_generations_table

# Apply migrations locally
supabase db push

# Apply to production
supabase db push --db-url $SUPABASE_DB_URL

# Generate TypeScript types
supabase gen types typescript --local > lib/database.types.ts
```

### Migration History

| Version | Date | Description |
|---------|------|-------------|
| 001 | 2026-01-17 | Initial schema (projects, project_files) |
| 002 | 2026-01-17 | Add generations table |
| 003 | 2026-01-17 | Add deployments table |
| 004 | TBD | Add collaboration features |

## Seeding

```bash
# Run seed script
supabase db seed
```

**Seed Data** (for development):
- Demo user: demo@informatik-ai.studio
- Sample projects with code files
- Example generations history

## TypeScript Types

Generated types are at `lib/database.types.ts`:

```typescript
import { Database } from '@/lib/database.types';

type Project = Database['public']['Tables']['projects']['Row'];
type ProjectInsert = Database['public']['Tables']['projects']['Insert'];
type ProjectUpdate = Database['public']['Tables']['projects']['Update'];
```
