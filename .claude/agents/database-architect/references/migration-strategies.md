# Database Migration Strategies Reference

This document provides comprehensive strategies and best practices for database migrations across different technologies.

## Migration Principles

### The Golden Rules

1. **Reversibility**: Every migration should have a rollback strategy
2. **Atomicity**: Migrations should be transactional when possible
3. **Idempotency**: Running a migration twice should produce the same result
4. **Testing**: Always test migrations on staging before production
5. **Backup**: Always backup before running migrations

## Zero-Downtime Migrations

### Expand-Contract Pattern

```markdown
## Phase 1: Expand
Add new structures without removing old ones.

## Phase 2: Migrate
Copy data from old to new structures.

## Phase 3: Contract
Remove old structures after verification.
```

### Example: Renaming a Column

```sql
-- WRONG: Direct rename causes downtime
ALTER TABLE users RENAME COLUMN name TO full_name;

-- RIGHT: Expand-Contract approach

-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name TEXT;

-- Step 2: Backfill data
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Step 3: Add trigger for new writes (during transition)
CREATE OR REPLACE FUNCTION sync_name_columns()
RETURNS TRIGGER AS $$
BEGIN
  NEW.full_name = COALESCE(NEW.full_name, NEW.name);
  NEW.name = COALESCE(NEW.name, NEW.full_name);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_names BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_name_columns();

-- Step 4: Update application to use full_name

-- Step 5: Remove old column and trigger (after deployment)
DROP TRIGGER sync_names ON users;
ALTER TABLE users DROP COLUMN name;
```

### Example: Splitting a Table

```sql
-- Original: users table with address fields

-- Step 1: Create new addresses table
CREATE TABLE addresses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  street TEXT,
  city TEXT,
  country TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 2: Create view that joins both (backward compatibility)
CREATE VIEW users_with_address AS
SELECT
  u.*,
  a.street,
  a.city,
  a.country
FROM users u
LEFT JOIN addresses a ON a.user_id = u.id;

-- Step 3: Migrate data
INSERT INTO addresses (user_id, street, city, country)
SELECT id, street, city, country FROM users WHERE street IS NOT NULL;

-- Step 4: Update application to use new structure

-- Step 5: Drop old columns
ALTER TABLE users
  DROP COLUMN street,
  DROP COLUMN city,
  DROP COLUMN country;
```

## ORM-Specific Migrations

### Prisma (Node.js)

```bash
# Create migration
npx prisma migrate dev --name add_user_profile

# Apply migrations in production
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset

# Generate migration SQL without applying
npx prisma migrate diff --from-schema-datamodel prisma/schema.prisma --to-schema-datasource prisma/schema.prisma --script
```

```prisma
// schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  profile   Profile?
  createdAt DateTime @default(now())
}

model Profile {
  id     String @id @default(uuid())
  bio    String?
  user   User   @relation(fields: [userId], references: [id])
  userId String @unique
}
```

### TypeORM (Node.js)

```bash
# Generate migration
npm run typeorm migration:generate -- -n AddUserProfile

# Run migrations
npm run typeorm migration:run

# Revert last migration
npm run typeorm migration:revert
```

```typescript
// migrations/1234567890-AddUserProfile.ts
export class AddUserProfile1234567890 implements MigrationInterface {
  async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "users" ADD COLUMN "bio" TEXT
    `);
  }

  async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      ALTER TABLE "users" DROP COLUMN "bio"
    `);
  }
}
```

### SQLAlchemy + Alembic (Python)

```bash
# Create migration
alembic revision --autogenerate -m "add user profile"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current version
alembic current
```

```python
# alembic/versions/xxx_add_user_profile.py
def upgrade():
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.create_index('idx_users_bio', 'users', ['bio'])

def downgrade():
    op.drop_index('idx_users_bio')
    op.drop_column('users', 'bio')
```

### Django (Python)

```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration plan
python manage.py showmigrations

# SQL preview
python manage.py sqlmigrate app_name 0001
```

```python
# migrations/0002_add_profile.py
class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
```

### Active Record (Ruby/Rails)

```bash
# Create migration
rails generate migration AddBioToUsers bio:text

# Run migrations
rails db:migrate

# Rollback
rails db:rollback

# Rollback specific version
rails db:migrate:down VERSION=20240115123456
```

```ruby
# db/migrate/20240115123456_add_bio_to_users.rb
class AddBioToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :bio, :text
    add_index :users, :bio
  end
end

# For non-reversible migrations
class ComplexMigration < ActiveRecord::Migration[7.0]
  def up
    # Forward migration
  end

  def down
    # Rollback
    raise ActiveRecord::IrreversibleMigration
  end
end
```

## Large Data Migrations

### Batched Updates

```sql
-- PostgreSQL: Update in batches to avoid locks
DO $$
DECLARE
  batch_size INT := 1000;
  affected_rows INT;
BEGIN
  LOOP
    UPDATE users
    SET status = 'active'
    WHERE id IN (
      SELECT id FROM users
      WHERE status IS NULL
      LIMIT batch_size
    );

    GET DIAGNOSTICS affected_rows = ROW_COUNT;

    IF affected_rows = 0 THEN
      EXIT;
    END IF;

    -- Small delay to allow other transactions
    PERFORM pg_sleep(0.1);
  END LOOP;
END $$;
```

```javascript
// Node.js batched migration
async function migrateInBatches(batchSize = 1000) {
  let processed = 0;

  while (true) {
    const result = await db.query(`
      WITH batch AS (
        SELECT id FROM users
        WHERE migrated = false
        LIMIT $1
        FOR UPDATE SKIP LOCKED
      )
      UPDATE users SET migrated = true, new_field = compute_value(old_field)
      WHERE id IN (SELECT id FROM batch)
      RETURNING id
    `, [batchSize]);

    if (result.rowCount === 0) break;

    processed += result.rowCount;
    console.log(`Processed ${processed} rows`);

    await new Promise(resolve => setTimeout(resolve, 100));
  }
}
```

### Parallel Processing

```python
# Python parallel migration
from concurrent.futures import ThreadPoolExecutor
import threading

def migrate_batch(start_id, end_id):
    with db.connection() as conn:
        conn.execute("""
            UPDATE users
            SET status = 'migrated'
            WHERE id >= %s AND id < %s
        """, (start_id, end_id))
        conn.commit()

# Get ID ranges
ranges = get_id_ranges(batch_size=10000)

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(migrate_batch, start, end)
        for start, end in ranges
    ]
    for future in futures:
        future.result()
```

## Schema Versioning

### Version Table
```sql
CREATE TABLE schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TIMESTAMPTZ DEFAULT NOW(),
  checksum TEXT,
  execution_time_ms INT
);
```

### Migration File Structure
```
migrations/
├── 20240101_001_create_users.sql
├── 20240101_002_create_posts.sql
├── 20240115_001_add_user_bio.sql
└── 20240120_001_add_indexes.sql
```

## Rollback Strategies

### Transactional Rollback
```sql
BEGIN;

-- Migration steps
ALTER TABLE users ADD COLUMN bio TEXT;
CREATE INDEX idx_users_bio ON users(bio);

-- If something goes wrong
ROLLBACK;

-- If successful
COMMIT;
```

### Manual Rollback Script
```sql
-- up.sql
ALTER TABLE users ADD COLUMN bio TEXT;

-- down.sql
ALTER TABLE users DROP COLUMN bio;
```

### Feature Flags for Data Migrations
```javascript
// Gradual rollout with feature flag
async function getUser(id) {
  const user = await db.users.findById(id);

  if (featureFlags.useNewSchema) {
    return {
      ...user,
      fullName: user.full_name,  // New column
    };
  }

  return {
    ...user,
    fullName: user.name,  // Old column
  };
}
```

## Testing Migrations

### Unit Tests
```javascript
describe('Migration: AddUserBio', () => {
  beforeEach(async () => {
    await db.migrate.rollback();
    await db.migrate.latest();
  });

  it('adds bio column to users', async () => {
    const columns = await db.raw(`
      SELECT column_name FROM information_schema.columns
      WHERE table_name = 'users' AND column_name = 'bio'
    `);
    expect(columns.rows).toHaveLength(1);
  });

  it('preserves existing data', async () => {
    const user = await db.users.findFirst();
    expect(user.email).toBeDefined();
  });
});
```

### Staging Validation Checklist
```markdown
## Pre-Migration
- [ ] Database backup completed
- [ ] Migration tested on copy of production data
- [ ] Rollback script tested
- [ ] Team notified of maintenance window

## During Migration
- [ ] Monitor database performance
- [ ] Watch for lock contention
- [ ] Verify data integrity

## Post-Migration
- [ ] Application health checks passing
- [ ] Data validation queries executed
- [ ] Performance metrics normal
- [ ] Rollback window defined (e.g., 24 hours)
```

## Production Deployment

### Blue-Green Database Pattern
```markdown
1. Create new database instance (green)
2. Apply migrations to green database
3. Sync data from blue to green
4. Switch application to green database
5. Keep blue database as rollback option
```

### Maintenance Window Script
```bash
#!/bin/bash
set -e

echo "Starting migration at $(date)"

# Backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Apply migrations
npm run migrate:production

# Validate
npm run validate:schema

echo "Migration completed at $(date)"
```
