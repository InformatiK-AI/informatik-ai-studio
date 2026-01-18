# Template: Architecture Documentation

This template is for files in `.claude/docs/architecture/` that document technical architecture details. These files are loaded on-demand when relevant work is being done.

**Characteristics**:
- Loaded on-demand (not auto-loaded)
- Detailed technical documentation
- Referenced from CLAUDE.md `[modular_index]`
- Should be comprehensive but focused

---

## Template: tech-stack.md

```markdown
# Technology Stack Details

> Referenced from: CLAUDE.md [stack] section
> Load when: Making technology decisions, onboarding

## Core Stack

### Framework: [Name] v[Version]

**Why Chosen**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Key Features Used**:
- Feature 1: [How we use it]
- Feature 2: [How we use it]

**Configuration**:
```javascript
// [config-file-name].js
module.exports = {
  // Key configuration options
};
```

**Important Caveats**:
- [Limitation or gotcha to be aware of]

---

### Language: [Name] v[Version]

**Compiler/Runtime Options**:
```json
{
  "compilerOptions": {
    // Key options
  }
}
```

**Style Guide**: [Link or description]

---

### Database: [Name] v[Version]

**Connection**:
```typescript
// Database connection pattern
const db = createConnection({
  host: process.env.DATABASE_URL,
  // Other options
});
```

**Key Tables/Collections**:
- `users` - User accounts
- `products` - Product catalog
- [etc.]

**Migrations**: See `database-schema.md` for details

---

### Styling: [Name] v[Version]

**Configuration**:
```javascript
// [config-file].js
module.exports = {
  // Configuration
};
```

**Custom Extensions**:
- [Custom theme, plugins, etc.]

---

## Supporting Libraries

| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| [name] | ^x.x.x | [purpose] | [notes] |

## Development Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| [name] | [purpose] | `[config file]` |

## Infrastructure

| Service | Provider | Purpose |
|---------|----------|---------|
| Hosting | [Provider] | Application hosting |
| Database | [Provider] | Data storage |
| CDN | [Provider] | Static assets |
| Auth | [Provider] | Authentication |
```

---

## Template: database-schema.md

```markdown
# Database Schema

> Referenced from: CLAUDE.md [modular_index]
> Load when: Working on database changes, data modeling

## Overview

**Database**: [PostgreSQL/MySQL/MongoDB/etc.] v[Version]
**ORM/Driver**: [Prisma/Drizzle/Mongoose/etc.]
**Migration Tool**: [Tool name]

## Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐
│   users     │────<│   orders    │
├─────────────┤     ├─────────────┤
│ id (PK)     │     │ id (PK)     │
│ email       │     │ user_id (FK)│
│ name        │     │ total       │
│ created_at  │     │ status      │
└─────────────┘     └─────────────┘
        │                  │
        │           ┌──────┴──────┐
        │           │             │
        ▼           ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  profiles   │ │ order_items │ │  payments   │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Tables

### users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Primary identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| name | VARCHAR(100) | NOT NULL | Display name |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update |

**Indexes**:
- `idx_users_email` on `email` (unique)
- `idx_users_created_at` on `created_at`

**RLS Policies** (if applicable):
```sql
-- Users can only see their own data
CREATE POLICY users_isolation ON users
  USING (auth.uid() = id);
```

### [other_table]

[Repeat structure for each table]

## Relationships

| From | To | Type | Description |
|------|-----|------|-------------|
| users | orders | 1:N | User has many orders |
| orders | order_items | 1:N | Order has many items |
| order_items | products | N:1 | Item references product |

## Migrations

### Running Migrations

```bash
# Generate migration
[migration_command] generate [name]

# Apply migrations
[migration_command] migrate

# Rollback
[migration_command] rollback
```

### Migration History

| Version | Date | Description |
|---------|------|-------------|
| 001 | YYYY-MM-DD | Initial schema |
| 002 | YYYY-MM-DD | Add user profiles |

## Seeding

```bash
# Run seed script
[seed_command]
```

**Seed Data**:
- Admin user: admin@example.com
- Test products: 10 sample products
```

---

## Template: api-contracts.md

```markdown
# API Contracts

> Referenced from: CLAUDE.md [modular_index]
> Load when: Working on API endpoints, integrations

## Base Configuration

**Base URL**: `https://api.example.com/v1`
**Authentication**: Bearer token (JWT)
**Content-Type**: `application/json`

## Authentication

### POST /auth/login

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response (200):
```json
{
  "success": true,
  "data": {
    "token": "eyJ...",
    "refreshToken": "abc...",
    "expiresIn": 3600
  }
}
```

Errors:
- 400: Invalid input
- 401: Invalid credentials
- 429: Too many attempts

---

## Users

### GET /users

**Description**: List all users (admin only)

**Query Parameters**:
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| page | number | No | Page number (default: 1) |
| limit | number | No | Items per page (default: 20) |
| search | string | No | Search by name/email |

**Response** (200):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

---

### GET /users/:id

**Description**: Get user by ID

**Path Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| id | UUID | User ID |

**Response** (200):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "profile": { ... },
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

**Errors**:
- 401: Unauthorized
- 403: Forbidden (not owner/admin)
- 404: User not found

---

### POST /users

**Description**: Create new user

**Request Body**:
```json
{
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "password": "securepassword123"
}
```

**Validation**:
- email: Required, valid email, unique
- name: Required, 2-100 characters
- password: Required, min 8 characters

**Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "newuser@example.com",
    "name": "Jane Doe",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

**Common Error Codes**:
| Code | HTTP | Description |
|------|------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| UNAUTHORIZED | 401 | Authentication required |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource already exists |
| RATE_LIMITED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| /auth/* | 10 | 1 minute |
| /api/* | 100 | 1 minute |
| /upload/* | 20 | 1 minute |
```

---

## Usage Notes

1. **Load on-demand**: These files are NOT auto-loaded
2. **Reference in CLAUDE.md**: Add to `[modular_index]` section
3. **Keep updated**: Schema/contracts must match implementation
4. **Examples help**: Include request/response examples
5. **Version control**: Track changes to contracts
