# Template: Path-Specific Rules File

This template is for files in `.claude/rules/domain/` that are loaded ONLY when working on matching file paths.

**Characteristics**:
- Auto-loaded only when working on matching paths
- Uses YAML frontmatter to specify paths
- More detailed than global rules
- Specific to a domain/area of the codebase

---

## Frontmatter Format

```yaml
---
description: Brief description of what these rules cover
paths:
  - "src/api/**"
  - "src/routes/**"
  - "**/*.api.ts"
---
```

**Frontmatter Fields**:
- `description` (required): One-line summary of the rules
- `paths` (required): Glob patterns for matching files
- `priority` (optional): Loading order if multiple rules match (default: 0)

---

## Template: api-rules.md

```yaml
---
description: Rules for API endpoints, routes, and controllers
paths:
  - "src/api/**"
  - "src/routes/**"
  - "app/api/**"
  - "**/*.controller.ts"
  - "**/*.route.ts"
---
```

```markdown
# API Development Rules

## Endpoint Design

### URL Conventions

```
GET    /api/v1/resources          # List resources
GET    /api/v1/resources/:id      # Get single resource
POST   /api/v1/resources          # Create resource
PUT    /api/v1/resources/:id      # Update resource (full)
PATCH  /api/v1/resources/:id      # Update resource (partial)
DELETE /api/v1/resources/:id      # Delete resource
```

### Naming

- Use plural nouns: `/users`, `/products`
- Use kebab-case: `/user-profiles`, `/order-items`
- Version in path: `/api/v1/`
- No verbs in URLs: `/users` not `/getUsers`

## Request/Response

### Request Validation

```typescript
// ALWAYS validate input
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
});

const validated = schema.parse(req.body);
```

### Response Format

```typescript
// Success response
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [...]
  }
}
```

### Status Codes

| Code | Use When |
|------|----------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation) |
| 401 | Unauthorized (auth required) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

## Security

### Authentication

- Use Bearer tokens in Authorization header
- Validate token on every protected route
- Never expose tokens in URLs or logs

### Authorization

```typescript
// Check permissions before action
if (!user.can('update', resource)) {
  throw new ForbiddenError('Insufficient permissions');
}
```

### Rate Limiting

- Apply rate limits to all endpoints
- Stricter limits on auth endpoints
- Return 429 with Retry-After header

## Error Handling

```typescript
// Use typed errors
throw new ApiError({
  code: 'USER_NOT_FOUND',
  message: 'User does not exist',
  statusCode: 404,
  details: { userId }
});
```

## Documentation

- Use JSDoc or OpenAPI comments
- Document all parameters
- Include example requests/responses
```

---

## Template: ui-rules.md

```yaml
---
description: Rules for UI components, pages, and layouts
paths:
  - "src/components/**"
  - "src/pages/**"
  - "app/**/*.tsx"
  - "**/*.component.tsx"
---
```

```markdown
# UI Development Rules

## Component Structure

### File Organization

```
ComponentName/
├── index.ts              # Re-export
├── ComponentName.tsx     # Main component
├── ComponentName.test.tsx # Tests
├── ComponentName.styles.ts # Styles (if CSS-in-JS)
└── types.ts              # Types (if complex)
```

### Component Template

```tsx
/**
 * ABOUTME: [What this component does]
 * RESPONSIBILITY: [Primary responsibility]
 */

interface Props {
  /** Description of prop */
  propName: string;
}

export function ComponentName({ propName }: Props) {
  // Hooks first
  const [state, setState] = useState();

  // Effects
  useEffect(() => { ... }, []);

  // Handlers
  const handleClick = () => { ... };

  // Render
  return ( ... );
}
```

## Props & State

### Props

- Use TypeScript interfaces for props
- Document complex props with JSDoc
- Provide default values where sensible
- Keep props minimal and focused

### State Management

- Local state for UI-only concerns
- Global state for shared data
- Avoid prop drilling (use context)
- Keep state close to where it's used

## Styling

### Class Naming (Tailwind)

```tsx
// Group related classes
<div className={cn(
  // Layout
  "flex flex-col gap-4",
  // Sizing
  "w-full max-w-md",
  // Colors
  "bg-white dark:bg-gray-800",
  // Conditional
  isActive && "ring-2 ring-primary"
)}>
```

### Responsive Design

```tsx
// Mobile-first approach
<div className="
  p-4 md:p-6 lg:p-8
  text-sm md:text-base
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
">
```

## Accessibility

### Required

- [ ] All images have alt text
- [ ] Interactive elements are focusable
- [ ] Color is not the only indicator
- [ ] Labels for all form inputs
- [ ] ARIA attributes where needed

### Keyboard Navigation

```tsx
<button
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  tabIndex={0}
>
```

## Performance

### Optimization Rules

- Memoize expensive computations
- Use React.memo for pure components
- Lazy load below-fold content
- Virtualize long lists

```tsx
// Memoize callbacks
const handleClick = useCallback(() => { ... }, [deps]);

// Memoize values
const computed = useMemo(() => expensive(data), [data]);
```

## Testing

### Test Requirements

- [ ] Renders without errors
- [ ] Displays correct content
- [ ] Handles user interactions
- [ ] Accessibility (a11y audit)
- [ ] Loading/error states
```

---

## Template: test-rules.md

```yaml
---
description: Rules for test files and test utilities
paths:
  - "tests/**"
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.spec.ts"
  - "**/__tests__/**"
---
```

```markdown
# Testing Rules

## Test File Structure

```typescript
/**
 * ABOUTME: Tests for [component/function name]
 */

describe('ComponentName', () => {
  // Setup
  beforeEach(() => { ... });
  afterEach(() => { ... });

  describe('when [condition]', () => {
    it('should [expected behavior]', () => {
      // Arrange
      const props = { ... };

      // Act
      const result = render(<Component {...props} />);

      // Assert
      expect(result).toMatchExpected();
    });
  });
});
```

## Naming Conventions

### Describe Blocks

```typescript
describe('UserService', () => {           // Class/Module
  describe('createUser', () => {          // Method
    describe('when email is valid', () => { // Condition
      it('should create user', () => {    // Expected behavior
```

### Test Names

- Start with "should"
- Be specific about behavior
- Include condition if relevant

```typescript
// Good
it('should return 404 when user not found')
it('should disable button while loading')

// Bad
it('test createUser')
it('works')
```

## Assertions

### Common Patterns

```typescript
// Equality
expect(result).toBe(expected);
expect(object).toEqual(expected);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();

// Collections
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Async
await expect(promise).resolves.toBe(expected);
await expect(promise).rejects.toThrow('Error');

// DOM (Testing Library)
expect(screen.getByText('Hello')).toBeInTheDocument();
expect(button).toBeDisabled();
```

## Mocking

### When to Mock

- External services (APIs, databases)
- Time-dependent functions
- Side effects (file system, network)
- Complex dependencies

### When NOT to Mock

- The code under test
- Simple utility functions
- Types and interfaces

```typescript
// Mock external service
vi.mock('@/services/api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1, name: 'Test' })
}));
```

## Test Data

### Factories

```typescript
// Use factories for test data
const createUser = (overrides = {}) => ({
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  ...overrides
});

// Usage
const user = createUser({ name: 'Custom Name' });
```

## Coverage

- Aim for 80% coverage minimum
- Focus on critical paths
- Don't test implementation details
- Quality over quantity
```

---

## Usage Notes

1. **Paths are globs**: Use `**` for recursive matching
2. **Multiple patterns**: List all relevant paths
3. **Specificity**: More specific rules can override general ones
4. **Keep focused**: Each file for ONE domain
5. **Examples matter**: Show correct patterns
