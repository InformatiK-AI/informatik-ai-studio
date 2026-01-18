# MySQL Patterns Reference

This document provides comprehensive patterns and best practices for MySQL database design.

## Schema Design Patterns

### Table Design with InnoDB

```sql
-- Users table
CREATE TABLE users (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  email VARCHAR(255) NOT NULL,
  username VARCHAR(50) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_email (email),
  UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Posts table
CREATE TABLE posts (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  user_id CHAR(36) NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  published TINYINT(1) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_posts_user FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_published (published)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Character Set and Collation

### UTF8MB4 for Full Unicode Support
```sql
-- Database level
CREATE DATABASE myapp
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Table level
CREATE TABLE messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB;

-- Column level for specific needs
ALTER TABLE products
  MODIFY name VARCHAR(255)
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_bin; -- Case-sensitive comparison
```

### Collation Options
```sql
-- Case-insensitive (default)
COLLATE utf8mb4_unicode_ci

-- Case-sensitive
COLLATE utf8mb4_bin

-- German phonebook sorting
COLLATE utf8mb4_german2_ci
```

## Indexing Strategies

### Basic Indexes
```sql
-- Single column index
CREATE INDEX idx_email ON users(email);

-- Composite index
CREATE INDEX idx_user_published ON posts(user_id, published, created_at);

-- Prefix index for long strings
CREATE INDEX idx_content_prefix ON posts(content(100));

-- Descending index (MySQL 8.0+)
CREATE INDEX idx_created_desc ON posts(created_at DESC);
```

### Full-Text Search
```sql
-- Full-text index
CREATE FULLTEXT INDEX ft_posts ON posts(title, content);

-- Using full-text search
SELECT *, MATCH(title, content) AGAINST('search term' IN NATURAL LANGUAGE MODE) AS score
FROM posts
WHERE MATCH(title, content) AGAINST('search term' IN NATURAL LANGUAGE MODE)
ORDER BY score DESC;

-- Boolean mode for advanced queries
SELECT * FROM posts
WHERE MATCH(title, content) AGAINST('+mysql -oracle' IN BOOLEAN MODE);
```

### Covering Indexes
```sql
-- Include all needed columns to avoid table lookup
CREATE INDEX idx_posts_covering ON posts(user_id, published, title, created_at);

-- Query uses only index
SELECT title, created_at FROM posts WHERE user_id = ? AND published = 1;
```

## InnoDB-Specific Patterns

### Row Locking
```sql
-- Select for update (exclusive lock)
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;

-- Select for share (shared lock)
SELECT * FROM products WHERE id = 1 FOR SHARE;

-- Skip locked rows (MySQL 8.0+)
SELECT * FROM tasks WHERE status = 'pending'
FOR UPDATE SKIP LOCKED LIMIT 1;
```

### Transactions
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check for errors
IF (SELECT balance FROM accounts WHERE id = 1) < 0 THEN
  ROLLBACK;
ELSE
  COMMIT;
END IF;
```

### Buffer Pool Optimization
```ini
# my.cnf configuration
[mysqld]
innodb_buffer_pool_size = 4G  # 70-80% of available RAM
innodb_buffer_pool_instances = 4  # 1 per GB
innodb_log_file_size = 1G
innodb_flush_log_at_trx_commit = 1  # ACID compliance
```

## Partitioning

### Range Partitioning
```sql
CREATE TABLE logs (
  id BIGINT AUTO_INCREMENT,
  created_at DATETIME NOT NULL,
  message TEXT,
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

### Hash Partitioning
```sql
CREATE TABLE orders (
  id BIGINT AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date DATE,
  PRIMARY KEY (id, customer_id)
) PARTITION BY HASH(customer_id) PARTITIONS 8;
```

## JSON Support (MySQL 5.7+)

```sql
-- JSON column
CREATE TABLE products (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  attributes JSON,
  INDEX idx_category ((CAST(attributes->>'$.category' AS CHAR(50))))
);

-- Insert JSON data
INSERT INTO products VALUES (1, 'Laptop', '{"brand": "Dell", "specs": {"ram": 16, "storage": 512}}');

-- Query JSON data
SELECT * FROM products
WHERE attributes->>'$.brand' = 'Dell';

-- JSON functions
SELECT
  JSON_EXTRACT(attributes, '$.specs.ram') as ram,
  JSON_UNQUOTE(JSON_EXTRACT(attributes, '$.brand')) as brand
FROM products;
```

## Stored Procedures

```sql
DELIMITER //

CREATE PROCEDURE transfer_funds(
  IN from_account INT,
  IN to_account INT,
  IN amount DECIMAL(10,2),
  OUT success BOOLEAN
)
BEGIN
  DECLARE current_balance DECIMAL(10,2);

  START TRANSACTION;

  SELECT balance INTO current_balance
  FROM accounts WHERE id = from_account FOR UPDATE;

  IF current_balance >= amount THEN
    UPDATE accounts SET balance = balance - amount WHERE id = from_account;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account;
    SET success = TRUE;
    COMMIT;
  ELSE
    SET success = FALSE;
    ROLLBACK;
  END IF;
END //

DELIMITER ;
```

## Query Optimization

### EXPLAIN Analysis
```sql
-- Analyze query execution plan
EXPLAIN FORMAT=JSON SELECT * FROM posts WHERE user_id = ?;

-- With actual execution stats (MySQL 8.0.18+)
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = ?;
```

### Query Hints
```sql
-- Force index usage
SELECT * FROM posts FORCE INDEX (idx_user_id) WHERE user_id = ?;

-- Ignore index
SELECT * FROM posts IGNORE INDEX (idx_published) WHERE user_id = ?;

-- Optimizer hints (MySQL 8.0+)
SELECT /*+ INDEX(posts idx_user_id) */ * FROM posts WHERE user_id = ?;
```

## Replication Patterns

### Read/Write Splitting
```sql
-- Write to primary
INSERT INTO posts (title, content) VALUES ('Title', 'Content');

-- Read from replica (application-level routing)
SELECT * FROM posts WHERE published = 1;
```

### GTID-Based Replication
```ini
# Primary
[mysqld]
gtid_mode = ON
enforce_gtid_consistency = ON
log_bin = mysql-bin
server_id = 1

# Replica
[mysqld]
gtid_mode = ON
enforce_gtid_consistency = ON
server_id = 2
read_only = ON
```

## Migration Strategy

```markdown
### Migration 1: Create users table
- Create table with InnoDB engine
- Set character set to utf8mb4
- Add unique constraints

### Migration 2: Create posts table
- Create table with foreign key
- Add indexes for common queries

### Migration 3: Add full-text search
- Create full-text index

### Migration 4: Optimize for production
- Add covering indexes
- Configure buffer pool
```
