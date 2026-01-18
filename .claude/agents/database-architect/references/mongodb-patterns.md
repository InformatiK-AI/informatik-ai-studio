# MongoDB Patterns Reference

This document provides comprehensive patterns and best practices for MongoDB database design.

## Collection Design Patterns

### Basic Collection with Mongoose

```javascript
// Collection: users
{
  _id: ObjectId,
  email: { type: String, required: true, unique: true, index: true },
  username: { type: String, required: true, unique: true },
  passwordHash: String,
  profile: {
    firstName: String,
    lastName: String,
    avatar: String
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
}

// Collection: posts
{
  _id: ObjectId,
  userId: { type: ObjectId, ref: 'User', required: true, index: true },
  title: { type: String, required: true },
  content: String,
  published: { type: Boolean, default: false, index: true },
  tags: [String],
  createdAt: { type: Date, default: Date.now, index: -1 },
  updatedAt: { type: Date, default: Date.now }
}
```

## Indexing Strategies

### Basic Indexes
```javascript
// Single field index
db.users.createIndex({ email: 1 }, { unique: true });

// Compound index
db.posts.createIndex({ userId: 1, createdAt: -1 });

// Sparse index (only documents with the field)
db.posts.createIndex({ published: 1 }, { sparse: true });

// Text index for full-text search
db.posts.createIndex({ title: "text", content: "text" });
```

### Advanced Indexes
```javascript
// TTL index for auto-expiring documents
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 });

// Partial index (only matching documents)
db.posts.createIndex(
  { viewCount: 1 },
  { partialFilterExpression: { published: true } }
);

// Wildcard index for dynamic fields
db.products.createIndex({ "attributes.$**": 1 });

// 2dsphere for geospatial queries
db.locations.createIndex({ coordinates: "2dsphere" });
```

## Denormalization Strategy

### Embed User Info in Posts for Faster Reads
```javascript
// Embedded approach - faster reads
{
  _id: ObjectId("..."),
  title: "My Post",
  content: "...",
  author: {
    _id: ObjectId("..."),
    username: "john_doe",
    avatar: "/avatars/john.jpg"
  }
}

// Use change streams to keep embedded data in sync
const changeStream = db.users.watch([
  { $match: { operationType: "update" } }
]);

changeStream.on("change", async (change) => {
  // Update all posts with embedded user data
  await db.posts.updateMany(
    { "author._id": change.documentKey._id },
    { $set: {
      "author.username": change.updateDescription.updatedFields.username
    }}
  );
});
```

### Bucket Pattern for Time-Series
```javascript
// Instead of one document per event
{
  _id: ObjectId,
  sensorId: "sensor_001",
  day: ISODate("2024-01-15"),
  measurements: [
    { time: ISODate("2024-01-15T00:00:00Z"), value: 23.5 },
    { time: ISODate("2024-01-15T00:01:00Z"), value: 23.6 },
    // ... up to ~100-200 per bucket
  ],
  count: 1440,
  sum: 33840,
  avg: 23.5
}
```

### Computed Pattern
```javascript
// Pre-compute frequently accessed values
{
  _id: ObjectId,
  title: "Product Name",
  ratings: [5, 4, 5, 3, 5, 4],
  // Computed fields
  ratingCount: 6,
  ratingSum: 26,
  ratingAvg: 4.33
}
```

## Aggregation Pipelines

### Common Patterns
```javascript
// Lookup (join-like operation)
db.orders.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "productId",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" }
]);

// Group and count
db.posts.aggregate([
  { $match: { published: true } },
  { $group: {
    _id: "$userId",
    postCount: { $sum: 1 },
    lastPost: { $max: "$createdAt" }
  }},
  { $sort: { postCount: -1 } },
  { $limit: 10 }
]);

// Faceted search
db.products.aggregate([
  {
    $facet: {
      byCategory: [{ $group: { _id: "$category", count: { $sum: 1 } } }],
      byPrice: [
        { $bucket: {
          groupBy: "$price",
          boundaries: [0, 50, 100, 500],
          default: "500+"
        }}
      ],
      results: [{ $limit: 20 }]
    }
  }
]);
```

## Schema Validation

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "username"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        username: {
          bsonType: "string",
          minLength: 3,
          maxLength: 50
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 150
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});
```

## Optimization Strategies

### Query Optimization
```javascript
// Use projection to limit returned fields
db.posts.find({ userId: userId }, { title: 1, createdAt: 1 });

// Use hint to force index usage
db.posts.find({ userId: userId }).hint({ userId: 1, createdAt: -1 });

// Explain query execution
db.posts.find({ userId: userId }).explain("executionStats");
```

### Sharding
```javascript
// Enable sharding on database
sh.enableSharding("mydb");

// Shard collection by user_id (hashed for even distribution)
sh.shardCollection("mydb.posts", { userId: "hashed" });

// Or use range sharding for ordered data
sh.shardCollection("mydb.events", { timestamp: 1 });
```

### Read Preferences
```javascript
// Read from secondary for analytics queries
db.posts.find({}).readPref("secondary");

// Read from nearest for low latency
db.posts.find({}).readPref("nearest");
```

## Transactions

```javascript
const session = client.startSession();
try {
  session.startTransaction();

  await users.updateOne(
    { _id: userId },
    { $inc: { balance: -amount } },
    { session }
  );

  await transactions.insertOne(
    { userId, amount, type: "debit" },
    { session }
  );

  await session.commitTransaction();
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

## Change Streams

```javascript
// Watch for changes
const changeStream = db.posts.watch([
  { $match: { operationType: { $in: ["insert", "update"] } } }
]);

changeStream.on("change", (change) => {
  console.log("Change detected:", change);
  // Update cache, send notification, etc.
});
```
