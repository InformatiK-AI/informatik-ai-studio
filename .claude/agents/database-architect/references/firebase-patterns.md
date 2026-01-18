# Firebase/Firestore Patterns Reference

This document provides comprehensive patterns and best practices for Firebase Firestore database design.

## Collection Design Patterns

### Basic Collection Structure
```javascript
// Collection: users
{
  uid: "user_123",  // Usually matches Firebase Auth UID
  email: "user@example.com",
  username: "johndoe",
  displayName: "John Doe",
  avatarUrl: "https://...",
  bio: "Hello world",
  createdAt: Timestamp,
  updatedAt: Timestamp
}

// Collection: posts
{
  id: "post_abc",
  authorId: "user_123",  // Reference to user
  author: {  // Denormalized for faster reads
    uid: "user_123",
    username: "johndoe",
    avatarUrl: "https://..."
  },
  title: "My First Post",
  content: "...",
  published: true,
  publishedAt: Timestamp,
  tags: ["tech", "firebase"],
  likeCount: 42,
  commentCount: 5,
  createdAt: Timestamp,
  updatedAt: Timestamp
}
```

### Subcollections
```javascript
// posts/{postId}/comments/{commentId}
{
  id: "comment_xyz",
  postId: "post_abc",
  authorId: "user_456",
  author: {
    uid: "user_456",
    username: "janedoe"
  },
  content: "Great post!",
  createdAt: Timestamp
}

// users/{userId}/notifications/{notificationId}
{
  id: "notif_123",
  type: "like",
  actorId: "user_789",
  postId: "post_abc",
  read: false,
  createdAt: Timestamp
}
```

## Security Rules Patterns

### Basic CRUD Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Users collection
    match /users/{userId} {
      // Anyone can read profiles
      allow read: if true;

      // Only owner can write
      allow create: if request.auth != null && request.auth.uid == userId;
      allow update: if request.auth != null && request.auth.uid == userId;
      allow delete: if false;  // Prevent deletion
    }

    // Posts collection
    match /posts/{postId} {
      // Anyone can read published posts
      allow read: if resource.data.published == true
                  || request.auth.uid == resource.data.authorId;

      // Authenticated users can create
      allow create: if request.auth != null
                    && request.resource.data.authorId == request.auth.uid;

      // Only author can update/delete
      allow update, delete: if request.auth != null
                            && resource.data.authorId == request.auth.uid;
    }

    // Comments subcollection
    match /posts/{postId}/comments/{commentId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null
                            && resource.data.authorId == request.auth.uid;
    }
  }
}
```

### Advanced Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }

    function hasRole(role) {
      return isAuthenticated()
             && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == role;
    }

    function validatePost() {
      let data = request.resource.data;
      return data.title is string
             && data.title.size() <= 255
             && data.content is string
             && data.content.size() <= 50000;
    }

    // Admin access
    match /{document=**} {
      allow read, write: if hasRole('admin');
    }

    // Posts with validation
    match /posts/{postId} {
      allow create: if isAuthenticated() && validatePost();
      allow update: if isOwner(resource.data.authorId) && validatePost();
    }
  }
}
```

## Denormalization Strategies

### Embed Frequently Accessed Data
```javascript
// Instead of just storing authorId, embed common fields
const post = {
  authorId: "user_123",
  author: {
    uid: "user_123",
    username: "johndoe",
    avatarUrl: "https://..."
  },
  // ... rest of post
};
```

### Keep Denormalized Data in Sync
```javascript
// Cloud Function to sync user updates
exports.onUserUpdate = functions.firestore
  .document('users/{userId}')
  .onUpdate(async (change, context) => {
    const before = change.before.data();
    const after = change.after.data();
    const userId = context.params.userId;

    // Check if relevant fields changed
    if (before.username === after.username &&
        before.avatarUrl === after.avatarUrl) {
      return null;
    }

    const batch = db.batch();

    // Update all posts by this user
    const postsSnapshot = await db
      .collection('posts')
      .where('authorId', '==', userId)
      .get();

    postsSnapshot.docs.forEach(doc => {
      batch.update(doc.ref, {
        'author.username': after.username,
        'author.avatarUrl': after.avatarUrl
      });
    });

    return batch.commit();
  });
```

### Counter Pattern (Distributed Counters)
```javascript
// For high-throughput counters, use sharded counters
// Collection: posts/{postId}/likeCounters/{shardId}

const NUM_SHARDS = 10;

// Initialize counter shards
async function initCounter(postId) {
  const batch = db.batch();
  for (let i = 0; i < NUM_SHARDS; i++) {
    batch.set(
      db.doc(`posts/${postId}/likeCounters/${i}`),
      { count: 0 }
    );
  }
  return batch.commit();
}

// Increment random shard
async function incrementCounter(postId) {
  const shardId = Math.floor(Math.random() * NUM_SHARDS);
  const shardRef = db.doc(`posts/${postId}/likeCounters/${shardId}`);
  return shardRef.update({
    count: FieldValue.increment(1)
  });
}

// Get total count
async function getCount(postId) {
  const snapshot = await db
    .collection(`posts/${postId}/likeCounters`)
    .get();

  let total = 0;
  snapshot.forEach(doc => {
    total += doc.data().count;
  });
  return total;
}
```

## Query Patterns

### Compound Queries
```javascript
// Multiple conditions
const posts = await db.collection('posts')
  .where('authorId', '==', userId)
  .where('published', '==', true)
  .orderBy('createdAt', 'desc')
  .limit(20)
  .get();

// Requires composite index:
// Collection: posts
// Fields: authorId (Ascending), published (Ascending), createdAt (Descending)
```

### Pagination
```javascript
// Cursor-based pagination
let lastDoc = null;

async function getNextPage() {
  let query = db.collection('posts')
    .orderBy('createdAt', 'desc')
    .limit(20);

  if (lastDoc) {
    query = query.startAfter(lastDoc);
  }

  const snapshot = await query.get();
  lastDoc = snapshot.docs[snapshot.docs.length - 1];

  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
}
```

### Array Contains
```javascript
// Find posts with specific tag
const posts = await db.collection('posts')
  .where('tags', 'array-contains', 'firebase')
  .get();

// Find posts with any of these tags
const posts = await db.collection('posts')
  .where('tags', 'array-contains-any', ['firebase', 'react'])
  .limit(10)
  .get();
```

### Collection Group Queries
```javascript
// Query across all subcollections with same name
const allComments = await db.collectionGroup('comments')
  .where('authorId', '==', userId)
  .orderBy('createdAt', 'desc')
  .get();
```

## Realtime Updates

### Listen to Document
```javascript
const unsubscribe = db.doc(`posts/${postId}`)
  .onSnapshot((doc) => {
    console.log('Current data:', doc.data());
  });

// Cleanup
unsubscribe();
```

### Listen to Collection
```javascript
const unsubscribe = db.collection('posts')
  .where('published', '==', true)
  .orderBy('createdAt', 'desc')
  .limit(50)
  .onSnapshot((snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added') {
        console.log('New post:', change.doc.data());
      }
      if (change.type === 'modified') {
        console.log('Modified post:', change.doc.data());
      }
      if (change.type === 'removed') {
        console.log('Removed post:', change.doc.data());
      }
    });
  });
```

## Transactions and Batches

### Transaction
```javascript
// Atomic read-then-write
await db.runTransaction(async (transaction) => {
  const postRef = db.doc(`posts/${postId}`);
  const postDoc = await transaction.get(postRef);

  if (!postDoc.exists) {
    throw new Error('Post not found');
  }

  const newLikeCount = postDoc.data().likeCount + 1;
  transaction.update(postRef, { likeCount: newLikeCount });
});
```

### Batched Writes
```javascript
// Multiple writes atomically (no reads)
const batch = db.batch();

const postRef = db.doc('posts/post_123');
batch.update(postRef, { published: true });

const userRef = db.doc('users/user_123');
batch.update(userRef, { postCount: FieldValue.increment(1) });

await batch.commit();
```

## Cloud Functions Integration

### Trigger on Create
```javascript
exports.onPostCreated = functions.firestore
  .document('posts/{postId}')
  .onCreate(async (snapshot, context) => {
    const post = snapshot.data();

    // Update user's post count
    await db.doc(`users/${post.authorId}`).update({
      postCount: FieldValue.increment(1)
    });

    // Send notification to followers
    // ...
  });
```

### Scheduled Cleanup
```javascript
exports.cleanupOldNotifications = functions.pubsub
  .schedule('every 24 hours')
  .onRun(async (context) => {
    const cutoff = Timestamp.fromDate(
      new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    );

    const snapshot = await db.collectionGroup('notifications')
      .where('createdAt', '<', cutoff)
      .limit(500)
      .get();

    const batch = db.batch();
    snapshot.docs.forEach(doc => batch.delete(doc.ref));

    return batch.commit();
  });
```

## Optimization Strategies

### Index Management
```json
// firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "posts",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "authorId", "order": "ASCENDING" },
        { "fieldPath": "published", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ],
  "fieldOverrides": []
}
```

### Reduce Document Reads
```javascript
// Use select() to get only needed fields
const snapshot = await db.collection('posts')
  .select('title', 'author', 'createdAt')
  .limit(20)
  .get();
```

## Migration Strategy

```markdown
### Migration 1: Set up collections
- Create users collection structure
- Create posts collection structure

### Migration 2: Configure security rules
- Deploy initial security rules
- Test with security rules simulator

### Migration 3: Create indexes
- Deploy composite indexes
- Wait for index builds

### Migration 4: Set up Cloud Functions
- Deploy triggers for denormalization
- Deploy scheduled jobs
```
