# PostgreSQL Patterns Reference

This document provides comprehensive patterns and best practices for PostgreSQL database design.

## Schema Design Patterns

### Table Design with Prisma ORM

```markdown
## Schema Design

### Table: users
- id: UUID PRIMARY KEY DEFAULT gen_random_uuid()
- email: VARCHAR(255) UNIQUE NOT NULL
- username: VARCHAR(50) UNIQUE NOT NULL
- password_hash: VARCHAR(255) NOT NULL
- created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
- updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()

### Table: posts
- id: UUID PRIMARY KEY DEFAULT gen_random_uuid()
- user_id: UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
- title: VARCHAR(255) NOT NULL
- content: TEXT NOT NULL
- published: BOOLEAN DEFAULT false
- created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
- updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
```

## Indexing Strategies

### Basic Indexes
```sql
-- Foreign key index for joins
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Partial index for filtered queries
CREATE INDEX idx_posts_published ON posts(published) WHERE published = true;

-- Descending index for recent-first queries
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

### Full-Text Search
```sql
-- GIN index for text search
CREATE INDEX idx_posts_search ON posts USING GIN(to_tsvector('english', title || ' ' || content));

-- Using the search
SELECT * FROM posts
WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', 'search term');
```

### JSONB Indexes
```sql
-- GIN index for JSONB containment
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);

-- Expression index for specific JSONB path
CREATE INDEX idx_users_role ON users((metadata->>'role'));
```

### Composite Indexes
```sql
-- Multi-column index for common query patterns
CREATE INDEX idx_posts_user_published ON posts(user_id, published, created_at DESC);

-- Covering index (INCLUDE)
CREATE INDEX idx_posts_covering ON posts(user_id) INCLUDE (title, created_at);
```

## Migration Strategy

```markdown
### Migration 1: Create users table
- Create table with all columns
- Add primary key constraint
- Add unique constraints

### Migration 2: Create posts table
- Create table with foreign key reference
- Add ON DELETE CASCADE

### Migration 3: Add indexes
- Add foreign key indexes
- Add partial indexes

### Migration 4: Add full-text search
- Add GIN index for text search
```

## Optimization Strategies

### Connection Pooling
```yaml
# PgBouncer configuration
[databases]
mydb = host=localhost dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

### Query Optimization
```sql
-- Profile slow queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM posts WHERE user_id = $1;

-- Materialized views for complex aggregations
CREATE MATERIALIZED VIEW post_stats AS
SELECT user_id, COUNT(*) as post_count, MAX(created_at) as last_post
FROM posts
GROUP BY user_id;

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY post_stats;
```

### Partitioning
```sql
-- Range partitioning by date
CREATE TABLE posts (
    id UUID DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    content TEXT,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE posts_2024_01 PARTITION OF posts
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## PostgreSQL Extensions

### Common Extensions
```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Full-text search improvements
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- JSON path queries
CREATE EXTENSION IF NOT EXISTS "jsonpath";

-- PostGIS for geospatial
CREATE EXTENSION IF NOT EXISTS "postgis";
```

## Constraints and Validation

```sql
-- Check constraints
ALTER TABLE users ADD CONSTRAINT email_format
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Exclusion constraints (prevent overlapping ranges)
ALTER TABLE reservations ADD CONSTRAINT no_overlapping
EXCLUDE USING GIST (room_id WITH =, daterange(start_date, end_date) WITH &&);
```

## Triggers and Functions

```sql
-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON posts
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
```

## Common Query Patterns

### Pagination
```sql
-- Cursor-based pagination (recommended for large datasets)
SELECT * FROM posts
WHERE created_at < $cursor
ORDER BY created_at DESC
LIMIT 20;

-- Offset pagination (simpler but slower for large offsets)
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 100;
```

### Upsert
```sql
-- Insert or update on conflict
INSERT INTO users (email, username)
VALUES ($1, $2)
ON CONFLICT (email)
DO UPDATE SET username = EXCLUDED.username;
```

### CTEs for Complex Queries
```sql
-- Recursive CTE for hierarchical data
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as depth
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ct.depth + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree;
```
