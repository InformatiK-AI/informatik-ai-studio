# tRPC Router Example: Blog API

Full example of a type-safe tRPC router with Zod validation.

```typescript
// router.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from './trpc';

// Input validation schemas
const createPostSchema = z.object({
  title: z.string().min(1).max(255),
  content: z.string().min(1),
  published: z.boolean().default(false),
});

const updatePostSchema = z.object({
  title: z.string().min(1).max(255).optional(),
  content: z.string().min(1).optional(),
  published: z.boolean().optional(),
});

const listPostsSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20),
  published: z.boolean().optional(),
});

export const postRouter = router({
  // Public procedures (no auth required)
  list: publicProcedure
    .input(listPostsSchema)
    .query(async ({ input, ctx }) => {
      const { page, limit, published } = input;
      // Implementation...
    }),

  byId: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ input, ctx }) => {
      // Implementation...
    }),

  // Protected procedures (auth required)
  create: protectedProcedure
    .input(createPostSchema)
    .mutation(async ({ input, ctx }) => {
      // Implementation...
    }),

  update: protectedProcedure
    .input(z.object({
      id: z.string().uuid(),
      data: updatePostSchema,
    }))
    .mutation(async ({ input, ctx }) => {
      // Implementation...
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ input, ctx }) => {
      // Implementation...
    }),

  // Subscription example
  onPostCreated: publicProcedure
    .subscription(async ({ ctx }) => {
      // Implementation with observable...
    }),
});

// Type exports for client
export type PostRouter = typeof postRouter;
```

## Client Usage

```typescript
// client.ts
import { createTRPCProxyClient, httpBatchLink } from '@trpc/client';
import type { AppRouter } from './server/router';

const client = createTRPCProxyClient<AppRouter>({
  links: [
    httpBatchLink({
      url: 'http://localhost:3000/api/trpc',
    }),
  ],
});

// Type-safe API calls
const posts = await client.post.list.query({ page: 1, limit: 10 });
const post = await client.post.byId.query({ id: 'uuid-here' });
const newPost = await client.post.create.mutate({
  title: 'Hello World',
  content: 'My first post',
});
```
