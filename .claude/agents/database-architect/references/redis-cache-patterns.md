# Redis Cache Patterns Reference

This document provides comprehensive patterns and best practices for Redis caching and data structures.

## Caching Strategies

### Read-Through Cache
```javascript
// Application checks cache first, then database
async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  let user = await redis.get(cacheKey);
  if (user) {
    return JSON.parse(user);
  }

  // Cache miss - fetch from database
  user = await db.users.findById(userId);

  // Store in cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

### Write-Through Cache
```javascript
// Update cache when writing to database
async function updateUser(userId, data) {
  const cacheKey = `user:${userId}`;

  // Update database
  const user = await db.users.update(userId, data);

  // Update cache synchronously
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

### Write-Behind (Write-Back) Cache
```javascript
// Write to cache immediately, sync to database asynchronously
async function updateUserAsync(userId, data) {
  const cacheKey = `user:${userId}`;

  // Update cache immediately
  await redis.setex(cacheKey, 3600, JSON.stringify(data));

  // Queue database update
  await redis.lpush('db:write:queue', JSON.stringify({
    operation: 'update',
    table: 'users',
    id: userId,
    data: data
  }));
}

// Background worker processes queue
async function processWriteQueue() {
  while (true) {
    const item = await redis.brpop('db:write:queue', 0);
    const { operation, table, id, data } = JSON.parse(item[1]);

    await db[table][operation](id, data);
  }
}
```

### Cache-Aside (Lazy Loading)
```javascript
// Application manages cache explicitly
async function getProduct(productId) {
  const cacheKey = `product:${productId}`;

  // Try cache
  let product = await redis.get(cacheKey);
  if (product) return JSON.parse(product);

  // Load from database
  product = await db.products.findById(productId);

  if (product) {
    // Cache it
    await redis.setex(cacheKey, 3600, JSON.stringify(product));
  }

  return product;
}

async function updateProduct(productId, data) {
  // Update database
  await db.products.update(productId, data);

  // Invalidate cache
  await redis.del(`product:${productId}`);
}
```

## TTL and Expiration Policies

### Static TTL
```javascript
// Fixed expiration time
await redis.setex('session:abc123', 86400, sessionData);  // 24 hours

// Set expiration on existing key
await redis.expire('cache:user:123', 3600);

// Set expiration at specific Unix timestamp
await redis.expireat('temp:data', Math.floor(Date.now() / 1000) + 3600);
```

### Sliding Expiration
```javascript
// Refresh TTL on each access
async function getWithSliding(key, ttl = 3600) {
  const value = await redis.get(key);
  if (value) {
    // Refresh TTL on access
    await redis.expire(key, ttl);
  }
  return value;
}
```

### Adaptive TTL
```javascript
// Adjust TTL based on access patterns
async function getWithAdaptiveTTL(key) {
  const multi = redis.multi();
  multi.get(key);
  multi.incr(`access:${key}`);
  const [value, accessCount] = await multi.exec();

  if (value) {
    // More accesses = longer TTL (max 24 hours)
    const ttl = Math.min(3600 * accessCount, 86400);
    await redis.expire(key, ttl);
  }

  return value;
}
```

## Redis Data Structures

### Strings
```javascript
// Simple key-value
await redis.set('user:123:name', 'John Doe');
await redis.get('user:123:name');

// Atomic operations
await redis.incr('page:views');
await redis.incrby('user:123:score', 10);
await redis.decr('inventory:item:456');

// Bit operations
await redis.setbit('users:active:2024-01-15', userId, 1);
await redis.bitcount('users:active:2024-01-15');
```

### Hashes
```javascript
// Store object fields
await redis.hset('user:123', {
  name: 'John Doe',
  email: 'john@example.com',
  age: 30
});

// Get single field
await redis.hget('user:123', 'name');

// Get all fields
await redis.hgetall('user:123');

// Increment field
await redis.hincrby('user:123', 'age', 1);

// Check field existence
await redis.hexists('user:123', 'email');
```

### Lists
```javascript
// Queue (FIFO)
await redis.lpush('queue:tasks', JSON.stringify(task));
const task = await redis.rpop('queue:tasks');

// Stack (LIFO)
await redis.lpush('stack:history', item);
const item = await redis.lpop('stack:history');

// Blocking pop (for workers)
const [queue, task] = await redis.brpop('queue:tasks', 30);  // 30s timeout

// Range operations
await redis.lrange('recent:posts', 0, 9);  // Get first 10
await redis.ltrim('recent:posts', 0, 99);  // Keep only first 100
```

### Sets
```javascript
// Add members
await redis.sadd('tags:post:123', 'redis', 'cache', 'database');

// Check membership
await redis.sismember('tags:post:123', 'redis');

// Get all members
await redis.smembers('tags:post:123');

// Set operations
await redis.sunion('user:123:follows', 'user:456:follows');
await redis.sinter('user:123:follows', 'user:456:follows');
await redis.sdiff('user:123:follows', 'user:456:follows');

// Random member
await redis.srandmember('tags:post:123');
```

### Sorted Sets
```javascript
// Leaderboard
await redis.zadd('leaderboard', { score: 1500, member: 'player:123' });
await redis.zadd('leaderboard', { score: 1200, member: 'player:456' });

// Get top 10
await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES');

// Get rank
await redis.zrevrank('leaderboard', 'player:123');

// Get score
await redis.zscore('leaderboard', 'player:123');

// Range by score
await redis.zrangebyscore('leaderboard', 1000, 2000);

// Increment score
await redis.zincrby('leaderboard', 50, 'player:123');
```

## Session Storage

### Simple Session
```javascript
async function createSession(userId) {
  const sessionId = crypto.randomUUID();
  const sessionData = {
    userId,
    createdAt: Date.now(),
    lastAccess: Date.now()
  };

  await redis.setex(
    `session:${sessionId}`,
    86400,  // 24 hour TTL
    JSON.stringify(sessionData)
  );

  return sessionId;
}

async function getSession(sessionId) {
  const data = await redis.get(`session:${sessionId}`);
  if (!data) return null;

  // Refresh session
  await redis.expire(`session:${sessionId}`, 86400);

  return JSON.parse(data);
}

async function destroySession(sessionId) {
  await redis.del(`session:${sessionId}`);
}
```

### Session with Hash
```javascript
// More efficient for partial updates
async function updateSession(sessionId, updates) {
  const key = `session:${sessionId}`;

  await redis.hset(key, updates);
  await redis.expire(key, 86400);
}

async function getSessionField(sessionId, field) {
  return await redis.hget(`session:${sessionId}`, field);
}
```

## Rate Limiting

### Fixed Window
```javascript
async function checkRateLimit(userId, limit = 100, windowSeconds = 60) {
  const key = `ratelimit:${userId}:${Math.floor(Date.now() / 1000 / windowSeconds)}`;

  const count = await redis.incr(key);

  if (count === 1) {
    await redis.expire(key, windowSeconds);
  }

  return count <= limit;
}
```

### Sliding Window
```javascript
async function checkSlidingRateLimit(userId, limit = 100, windowMs = 60000) {
  const key = `ratelimit:${userId}`;
  const now = Date.now();
  const windowStart = now - windowMs;

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count requests in window
  const count = await redis.zcard(key);

  if (count < limit) {
    // Add current request
    await redis.zadd(key, { score: now, member: `${now}:${Math.random()}` });
    await redis.expire(key, Math.ceil(windowMs / 1000));
    return true;
  }

  return false;
}
```

### Token Bucket
```javascript
async function checkTokenBucket(userId, maxTokens = 10, refillRate = 1) {
  const key = `bucket:${userId}`;
  const now = Date.now();

  const data = await redis.hgetall(key);
  let tokens = parseFloat(data.tokens) || maxTokens;
  let lastRefill = parseInt(data.lastRefill) || now;

  // Refill tokens
  const elapsed = (now - lastRefill) / 1000;
  tokens = Math.min(maxTokens, tokens + elapsed * refillRate);

  if (tokens >= 1) {
    // Consume token
    await redis.hset(key, {
      tokens: (tokens - 1).toString(),
      lastRefill: now.toString()
    });
    await redis.expire(key, 3600);
    return true;
  }

  return false;
}
```

## Pub/Sub Patterns

### Basic Pub/Sub
```javascript
// Publisher
async function publishEvent(channel, event) {
  await redis.publish(channel, JSON.stringify(event));
}

// Subscriber
const subscriber = redis.duplicate();
await subscriber.subscribe('events:user', (message) => {
  const event = JSON.parse(message);
  console.log('Received:', event);
});

// Pattern subscribe
await subscriber.psubscribe('events:*', (message, channel) => {
  console.log(`Received on ${channel}:`, message);
});
```

### Streams (Persistent Pub/Sub)
```javascript
// Add to stream
await redis.xadd('events:stream', '*', {
  type: 'user_created',
  userId: '123',
  timestamp: Date.now().toString()
});

// Read from stream (consumer group)
await redis.xgroup('CREATE', 'events:stream', 'worker-group', '$', { MKSTREAM: true });

// Consumer reads
const events = await redis.xreadgroup(
  'GROUP', 'worker-group', 'worker-1',
  'COUNT', 10,
  'BLOCK', 5000,
  'STREAMS', 'events:stream', '>'
);

// Acknowledge processed
await redis.xack('events:stream', 'worker-group', messageId);
```

## Cache Invalidation Patterns

### Tag-Based Invalidation
```javascript
// Store with tags
async function setWithTags(key, value, tags, ttl = 3600) {
  const multi = redis.multi();

  multi.setex(key, ttl, JSON.stringify(value));

  for (const tag of tags) {
    multi.sadd(`tag:${tag}`, key);
    multi.expire(`tag:${tag}`, ttl);
  }

  await multi.exec();
}

// Invalidate by tag
async function invalidateByTag(tag) {
  const keys = await redis.smembers(`tag:${tag}`);

  if (keys.length > 0) {
    await redis.del(...keys, `tag:${tag}`);
  }
}

// Usage
await setWithTags('user:123', userData, ['users', 'user:123']);
await invalidateByTag('users');  // Invalidates all user caches
```

### Version-Based Invalidation
```javascript
async function getVersionedCache(key, fetchFn) {
  const version = await redis.get('cache:version') || '1';
  const versionedKey = `${key}:v${version}`;

  let value = await redis.get(versionedKey);
  if (value) return JSON.parse(value);

  value = await fetchFn();
  await redis.setex(versionedKey, 3600, JSON.stringify(value));

  return value;
}

// Invalidate all caches
async function invalidateAllCaches() {
  await redis.incr('cache:version');
}
```

## Performance Optimization

### Pipelining
```javascript
// Batch multiple commands
const pipeline = redis.pipeline();

for (const userId of userIds) {
  pipeline.get(`user:${userId}`);
}

const results = await pipeline.exec();
```

### Lua Scripts
```javascript
// Atomic operations with Lua
const script = `
  local current = redis.call('GET', KEYS[1])
  if current then
    return redis.call('SET', KEYS[1], current + ARGV[1])
  else
    return redis.call('SET', KEYS[1], ARGV[1])
  end
`;

await redis.eval(script, 1, 'counter', 5);
```

### Memory Optimization
```javascript
// Use hashes for small objects (hash-max-ziplist-entries)
// Instead of: SET user:123:name "John"
//             SET user:123:email "john@example.com"
// Use:        HSET user:123 name "John" email "john@example.com"

// Enable compression for large values
const compressed = zlib.gzipSync(JSON.stringify(largeObject));
await redis.setex('large:data', 3600, compressed);
```

## Clustering Considerations

### Key Slot Distribution
```javascript
// Use hash tags for related keys on same slot
const userKey = 'user:{123}:profile';
const sessionKey = 'user:{123}:session';
// Both keys will be on the same slot due to {123}
```

### Cross-Slot Operations
```javascript
// Avoid multi-key operations across slots
// BAD: redis.mget('user:1', 'user:2', 'user:3')  // May fail in cluster

// GOOD: Use pipeline for cross-slot reads
const pipeline = redis.pipeline();
for (const id of ids) {
  pipeline.get(`user:${id}`);
}
await pipeline.exec();
```
