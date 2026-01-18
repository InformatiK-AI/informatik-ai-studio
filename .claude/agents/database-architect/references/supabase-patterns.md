# Supabase Patterns Reference

This document provides comprehensive patterns and best practices for Supabase database design with PostgreSQL and Row-Level Security.

## Schema Design Patterns

### Basic Schema with Auth Integration

```sql
-- Table: profiles (extends auth.users)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username VARCHAR(50) UNIQUE NOT NULL,
  full_name TEXT,
  bio TEXT,
  avatar_url TEXT,
  website TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: posts
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  published BOOLEAN DEFAULT false,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: comments
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Row-Level Security (RLS) Patterns

### Enable RLS
```sql
-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
```

### Profiles Table Policies
```sql
-- Anyone can view profiles
CREATE POLICY "Profiles are viewable by everyone"
ON profiles FOR SELECT
USING (true);

-- Users can update own profile
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Users can insert own profile (on signup)
CREATE POLICY "Users can insert own profile"
ON profiles FOR INSERT
WITH CHECK (auth.uid() = id);
```

### Posts Table Policies
```sql
-- Anyone can view published posts
CREATE POLICY "Published posts are viewable by everyone"
ON posts FOR SELECT
USING (published = true);

-- Authors can view own unpublished posts
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);

-- Authors can create posts
CREATE POLICY "Users can create posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Authors can update own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Authors can delete own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = user_id);
```

### Role-Based Policies
```sql
-- Admin users (stored in profiles.role)
CREATE POLICY "Admins can do anything"
ON posts FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid()
    AND role = 'admin'
  )
);

-- Team-based access
CREATE POLICY "Team members can view team posts"
ON posts FOR SELECT
USING (
  team_id IN (
    SELECT team_id FROM team_members
    WHERE user_id = auth.uid()
  )
);
```

## Realtime Configuration

```sql
-- Enable realtime for specific tables
ALTER PUBLICATION supabase_realtime ADD TABLE posts;
ALTER PUBLICATION supabase_realtime ADD TABLE comments;

-- Filter realtime events (Supabase Dashboard or SQL)
-- Only broadcast published posts
```

### Client-Side Realtime
```typescript
// Subscribe to realtime changes
const subscription = supabase
  .channel('posts-channel')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts',
      filter: 'published=eq.true'
    },
    (payload) => {
      console.log('New post:', payload.new);
    }
  )
  .subscribe();
```

## Database Functions

### Triggers for Automation
```sql
-- Auto-update updated_at timestamp
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

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, username, full_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW
EXECUTE FUNCTION handle_new_user();
```

### RPC Functions
```sql
-- Custom function for complex queries
CREATE OR REPLACE FUNCTION get_user_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT json_build_object(
    'post_count', (SELECT COUNT(*) FROM posts WHERE user_id = user_uuid),
    'comment_count', (SELECT COUNT(*) FROM comments WHERE user_id = user_uuid),
    'total_views', (SELECT COALESCE(SUM(view_count), 0) FROM posts WHERE user_id = user_uuid)
  ) INTO result;
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Call from client
-- const { data } = await supabase.rpc('get_user_stats', { user_uuid: userId });
```

## Storage Integration

```sql
-- Storage policies for avatars bucket
CREATE POLICY "Avatar images are publicly accessible"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own avatar"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);
```

## Edge Functions Integration

```typescript
// supabase/functions/process-post/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  const { postId } = await req.json()

  // Process with service role (bypasses RLS)
  const { data, error } = await supabase
    .from('posts')
    .update({ processed: true })
    .eq('id', postId)
    .select()

  return new Response(JSON.stringify({ data, error }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

## Optimization Strategies

### PostgREST Caching
```sql
-- Use immutable functions for caching
CREATE OR REPLACE FUNCTION get_published_posts()
RETURNS SETOF posts
LANGUAGE sql
STABLE  -- Allows caching within a transaction
AS $$
  SELECT * FROM posts WHERE published = true ORDER BY created_at DESC;
$$;
```

### Materialized Views
```sql
-- Dashboard analytics
CREATE MATERIALIZED VIEW post_analytics AS
SELECT
  user_id,
  COUNT(*) as total_posts,
  COUNT(*) FILTER (WHERE published) as published_posts,
  SUM(view_count) as total_views,
  MAX(created_at) as last_post_at
FROM posts
GROUP BY user_id;

-- Refresh on schedule (via pg_cron)
SELECT cron.schedule(
  'refresh-analytics',
  '*/15 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY post_analytics'
);
```

### Indexes for Common Queries
```sql
-- Index for user's posts
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Index for published posts (sorted)
CREATE INDEX idx_posts_published_date ON posts(published_at DESC)
WHERE published = true;

-- Full-text search
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || content));
```

## Migration Strategy

```markdown
### Migration 1: Create profiles table
- Create table extending auth.users
- Add unique constraints
- Enable RLS and create policies

### Migration 2: Create posts table
- Create table with foreign keys
- Add indexes
- Enable RLS and create policies

### Migration 3: Create realtime
- Add tables to publication
- Configure filters

### Migration 4: Create functions
- Add trigger functions
- Create RPC functions
```
