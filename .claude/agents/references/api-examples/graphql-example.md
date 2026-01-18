# GraphQL Schema Example: Blog API

Full example of a GraphQL schema using SDL.

```graphql
"""
Blog API GraphQL Schema
"""
scalar DateTime
scalar UUID

"""
A blog post
"""
type Post {
  """Unique identifier for the post"""
  id: UUID!

  """Post title (max 255 characters)"""
  title: String!

  """Post content in Markdown format"""
  content: String!

  """Whether the post is published"""
  published: Boolean!

  """Post author"""
  author: User!

  """When the post was created"""
  createdAt: DateTime!

  """When the post was last updated"""
  updatedAt: DateTime!

  """List of comments on this post"""
  comments(
    first: Int = 20
    after: String
  ): CommentConnection!
}

"""
A registered user
"""
type User {
  id: UUID!
  email: String!
  username: String!
  bio: String
  avatarUrl: String
  posts(
    first: Int = 20
    after: String
  ): PostConnection!
}

"""
Paginated connection for posts
"""
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

"""
Input for creating a post
"""
input CreatePostInput {
  title: String!
  content: String!
  published: Boolean = false
}

"""
Input for updating a post
"""
input UpdatePostInput {
  title: String
  content: String
  published: Boolean
}

"""
Filter options for posts
"""
input PostFilter {
  published: Boolean
  authorId: UUID
  search: String
}

type Query {
  """Get a post by ID"""
  post(id: UUID!): Post

  """List posts with pagination and filtering"""
  posts(
    first: Int = 20
    after: String
    filter: PostFilter
  ): PostConnection!

  """Search posts by title and content"""
  searchPosts(query: String!): [Post!]!

  """Get current authenticated user"""
  me: User
}

type Mutation {
  """Create a new post"""
  createPost(input: CreatePostInput!): Post!

  """Update an existing post"""
  updatePost(id: UUID!, input: UpdatePostInput!): Post!

  """Delete a post"""
  deletePost(id: UUID!): Boolean!

  """Publish a post"""
  publishPost(id: UUID!): Post!
}

type Subscription {
  """Subscribe to new posts"""
  postCreated(authorId: UUID): Post!

  """Subscribe to post updates"""
  postUpdated(id: UUID!): Post!
}

"""
API Error
"""
type Error {
  code: String!
  message: String!
  path: [String!]
}

"""
Standard error codes
"""
enum ErrorCode {
  VALIDATION_ERROR
  UNAUTHORIZED
  FORBIDDEN
  NOT_FOUND
  INTERNAL_ERROR
  RATE_LIMIT_EXCEEDED
}
```
