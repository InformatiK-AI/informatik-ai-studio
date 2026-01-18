# SQLite Patterns Reference

This document provides comprehensive patterns and best practices for SQLite database design.

## Schema Design Patterns

### Basic Schema
```sql
-- Enable foreign keys (must be done per connection)
PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE users (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Posts table
CREATE TABLE posts (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Create indexes
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published) WHERE published = 1;
```

## Important PRAGMAs

### Performance PRAGMAs
```sql
-- Write-Ahead Logging for better concurrency
PRAGMA journal_mode = WAL;

-- Synchronous mode (trade-off between safety and speed)
PRAGMA synchronous = NORMAL;  -- or FULL for maximum safety

-- Memory-mapped I/O
PRAGMA mmap_size = 268435456;  -- 256MB

-- Cache size (negative = KB, positive = pages)
PRAGMA cache_size = -64000;  -- 64MB

-- Temp store in memory
PRAGMA temp_store = MEMORY;

-- Enable foreign keys
PRAGMA foreign_keys = ON;
```

### Analysis PRAGMAs
```sql
-- Analyze tables for query optimizer
ANALYZE;

-- Check database integrity
PRAGMA integrity_check;

-- Get table information
PRAGMA table_info(users);

-- Get index information
PRAGMA index_list(posts);
PRAGMA index_info(idx_posts_user_id);
```

## Indexing Strategies

### Basic Indexes
```sql
-- Single column index
CREATE INDEX idx_email ON users(email);

-- Composite index
CREATE INDEX idx_posts_user_published ON posts(user_id, published);

-- Partial index
CREATE INDEX idx_published_posts ON posts(created_at) WHERE published = 1;

-- Expression index
CREATE INDEX idx_email_lower ON users(lower(email));
```

### Covering Indexes
```sql
-- Include all query columns
CREATE INDEX idx_posts_covering ON posts(user_id, published, title, created_at);

-- Query uses only index
SELECT title, created_at FROM posts WHERE user_id = ? AND published = 1;
```

### Full-Text Search (FTS5)
```sql
-- Create FTS5 virtual table
CREATE VIRTUAL TABLE posts_fts USING fts5(
  title,
  content,
  content='posts',
  content_rowid='rowid'
);

-- Keep FTS in sync with triggers
CREATE TRIGGER posts_ai AFTER INSERT ON posts BEGIN
  INSERT INTO posts_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
END;

CREATE TRIGGER posts_ad AFTER DELETE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, content) VALUES('delete', old.rowid, old.title, old.content);
END;

CREATE TRIGGER posts_au AFTER UPDATE ON posts BEGIN
  INSERT INTO posts_fts(posts_fts, rowid, title, content) VALUES('delete', old.rowid, old.title, old.content);
  INSERT INTO posts_fts(rowid, title, content) VALUES (new.rowid, new.title, new.content);
END;

-- Search queries
SELECT * FROM posts WHERE rowid IN (
  SELECT rowid FROM posts_fts WHERE posts_fts MATCH 'search term'
);

-- With ranking
SELECT posts.*, bm25(posts_fts) as rank
FROM posts
JOIN posts_fts ON posts.rowid = posts_fts.rowid
WHERE posts_fts MATCH 'search term'
ORDER BY rank;
```

## JSON Support (SQLite 3.38+)

```sql
-- Store JSON
CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  attributes TEXT  -- JSON stored as TEXT
);

INSERT INTO products VALUES (1, 'Laptop', '{"brand": "Dell", "specs": {"ram": 16}}');

-- Query JSON
SELECT json_extract(attributes, '$.brand') as brand FROM products;

-- JSON operators (SQLite 3.38+)
SELECT * FROM products WHERE attributes->>'$.brand' = 'Dell';

-- Update JSON
UPDATE products
SET attributes = json_set(attributes, '$.specs.storage', 512)
WHERE id = 1;
```

## Transactions and Locking

### Transaction Modes
```sql
-- Deferred (default) - locks on first write
BEGIN DEFERRED TRANSACTION;

-- Immediate - locks immediately (prevents deadlocks)
BEGIN IMMEDIATE TRANSACTION;

-- Exclusive - full database lock
BEGIN EXCLUSIVE TRANSACTION;
```

### Busy Handling
```sql
-- Set timeout for busy database
PRAGMA busy_timeout = 5000;  -- 5 seconds
```

### Write-Ahead Logging (WAL)
```sql
-- Enable WAL mode
PRAGMA journal_mode = WAL;

-- Checkpoint WAL file
PRAGMA wal_checkpoint(TRUNCATE);

-- Check WAL status
PRAGMA wal_checkpoint;
```

## Common Patterns

### Upsert (INSERT OR REPLACE)
```sql
-- Replace on conflict
INSERT OR REPLACE INTO users (id, email, username)
VALUES (?, ?, ?);

-- Update on conflict (SQLite 3.24+)
INSERT INTO users (email, username)
VALUES (?, ?)
ON CONFLICT(email) DO UPDATE SET username = excluded.username;
```

### Pagination
```sql
-- Offset pagination
SELECT * FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;

-- Cursor-based pagination (more efficient)
SELECT * FROM posts
WHERE created_at < ?
ORDER BY created_at DESC
LIMIT 20;
```

### Triggers for Updated Timestamp
```sql
CREATE TRIGGER update_posts_timestamp
AFTER UPDATE ON posts
BEGIN
  UPDATE posts SET updated_at = datetime('now') WHERE id = NEW.id;
END;
```

### Soft Delete
```sql
-- Add deleted_at column
ALTER TABLE posts ADD COLUMN deleted_at TEXT;

-- Create view for active records
CREATE VIEW active_posts AS
SELECT * FROM posts WHERE deleted_at IS NULL;

-- Soft delete
UPDATE posts SET deleted_at = datetime('now') WHERE id = ?;
```

## Performance Optimization

### Query Optimization
```sql
-- Explain query plan
EXPLAIN QUERY PLAN SELECT * FROM posts WHERE user_id = ?;

-- Analyze for optimizer
ANALYZE posts;

-- Force index usage
SELECT * FROM posts INDEXED BY idx_posts_user_id WHERE user_id = ?;
```

### Vacuum
```sql
-- Rebuild database file
VACUUM;

-- Auto-vacuum settings
PRAGMA auto_vacuum = INCREMENTAL;
PRAGMA incremental_vacuum(100);  -- Free 100 pages
```

### Connection Pooling Considerations
```javascript
// Better-sqlite3 (Node.js) - synchronous, no pool needed
const db = new Database('mydb.sqlite');

// For async libraries, use connection pool
const pool = new Pool({
  max: 10,
  create: () => new Database('mydb.sqlite'),
  destroy: (db) => db.close()
});
```

## Backup Strategies

### Online Backup
```sql
-- Backup to file
.backup main backup.sqlite

-- Or using SQLite API
sqlite3_backup_init()
```

### WAL Checkpoint Before Backup
```sql
PRAGMA wal_checkpoint(TRUNCATE);
```

## Migration Strategy

```markdown
### Migration 1: Enable WAL mode
- PRAGMA journal_mode = WAL
- PRAGMA synchronous = NORMAL

### Migration 2: Create users table
- Create table with constraints
- Create unique indexes

### Migration 3: Create posts table
- Create table with foreign key
- Enable foreign_keys pragma
- Create indexes

### Migration 4: Add full-text search
- Create FTS5 virtual table
- Add sync triggers
```

## Limitations to Consider

1. **Concurrency**: One writer at a time (WAL helps with reads)
2. **No network access**: Local file only
3. **Type affinity**: Columns don't enforce types strictly
4. **No ALTER COLUMN**: Must recreate table to change columns
5. **Limited ALTER TABLE**: Can only ADD COLUMN and RENAME

### Workaround for Schema Changes
```sql
-- Create new table with desired schema
CREATE TABLE posts_new (
  id TEXT PRIMARY KEY,
  -- new schema here
);

-- Copy data
INSERT INTO posts_new SELECT ... FROM posts;

-- Swap tables
DROP TABLE posts;
ALTER TABLE posts_new RENAME TO posts;
```
