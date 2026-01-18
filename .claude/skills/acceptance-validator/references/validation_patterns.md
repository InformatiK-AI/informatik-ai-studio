# Validation Patterns by Method

## Overview

This document provides detailed patterns and examples for each validation method supported by the Acceptance Validator skill.

---

## Playwright Validation

### When to Use
- Frontend/UI testing
- End-to-end user flows
- Browser-specific behavior
- Visual regression testing

### Setup

```bash
# Install Playwright
npm init playwright@latest

# Install browsers
npx playwright install chromium firefox webkit
```

### Configuration
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: 2,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

### Common Patterns

#### Pattern 1: Form Submission
```typescript
test('User submits contact form', async ({ page }) => {
  await page.goto('/contact');

  await page.fill('[data-testid="name"]', 'John Doe');
  await page.fill('[data-testid="email"]', 'john@example.com');
  await page.fill('[data-testid="message"]', 'Hello world');

  await page.click('[data-testid="submit"]');

  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page).toHaveURL('/contact/success');
});
```

#### Pattern 2: Authentication Flow
```typescript
test('User can login and logout', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('#email', 'user@example.com');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');

  // Verify login
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();

  // Logout
  await page.click('[data-testid="user-menu"]');
  await page.click('[data-testid="logout"]');

  // Verify logout
  await expect(page).toHaveURL('/login');
});
```

#### Pattern 3: Cookie Validation
```typescript
test('Session cookie is secure', async ({ page, context }) => {
  await page.goto('/login');
  await page.fill('#email', 'user@example.com');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');

  const cookies = await context.cookies();
  const sessionCookie = cookies.find(c => c.name === 'session');

  expect(sessionCookie).toBeDefined();
  expect(sessionCookie?.httpOnly).toBe(true);
  expect(sessionCookie?.secure).toBe(true);
  expect(sessionCookie?.sameSite).toBe('Strict');
});
```

#### Pattern 4: Network Request Validation
```typescript
test('API call is made correctly', async ({ page }) => {
  const responsePromise = page.waitForResponse(
    response => response.url().includes('/api/data') && response.status() === 200
  );

  await page.click('[data-testid="load-data"]');

  const response = await responsePromise;
  const data = await response.json();

  expect(data.items).toHaveLength(10);
});
```

### Checklist for Playwright
- [ ] Test runs in CI environment
- [ ] Screenshots captured on failure
- [ ] Traces available for debugging
- [ ] Tests are independent (no shared state)
- [ ] Selectors use data-testid where possible
- [ ] Timeouts are reasonable

---

## API-Test Validation

### When to Use
- Backend API testing
- Microservice validation
- Contract testing
- Integration testing

### Setup

```bash
# Using curl (built-in)
curl --version

# Or using httpie
pip install httpie

# Or using jq for JSON parsing
sudo apt-get install jq
```

### Common Patterns

#### Pattern 1: GET Request Validation
```bash
#!/bin/bash
# Test: GET /api/users returns list

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/users")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Assert status code
[ "$HTTP_CODE" -eq 200 ] || { echo "[FAIL] Expected 200, got $HTTP_CODE"; exit 1; }

# Assert response is array
COUNT=$(echo "$BODY" | jq '. | length')
[ "$COUNT" -gt 0 ] || { echo "[FAIL] Expected non-empty array"; exit 1; }

# Assert required fields
HAS_ID=$(echo "$BODY" | jq '.[0] | has("id")')
[ "$HAS_ID" = "true" ] || { echo "[FAIL] Missing id field"; exit 1; }

echo "[PASS] GET /api/users"
```

#### Pattern 2: POST Request with Body
```bash
#!/bin/bash
# Test: POST /api/users creates user

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"John Doe","email":"john@example.com"}' \
  "$BASE_URL/api/users")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Assert status code
[ "$HTTP_CODE" -eq 201 ] || { echo "[FAIL] Expected 201, got $HTTP_CODE"; exit 1; }

# Assert created user has ID
USER_ID=$(echo "$BODY" | jq -r '.id')
[ -n "$USER_ID" ] && [ "$USER_ID" != "null" ] || { echo "[FAIL] No ID returned"; exit 1; }

echo "[PASS] POST /api/users - Created ID: $USER_ID"
```

#### Pattern 3: Error Response Validation
```bash
#!/bin/bash
# Test: POST /api/users with invalid data returns 400

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":""}' \
  "$BASE_URL/api/users")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Assert 400 Bad Request
[ "$HTTP_CODE" -eq 400 ] || { echo "[FAIL] Expected 400, got $HTTP_CODE"; exit 1; }

# Assert error message
ERROR=$(echo "$BODY" | jq -r '.error')
[ -n "$ERROR" ] || { echo "[FAIL] No error message"; exit 1; }

echo "[PASS] POST /api/users - Invalid data rejected"
```

#### Pattern 4: Authentication Test
```bash
#!/bin/bash
# Test: Unauthenticated request returns 401

RESPONSE=$(curl -s -w "\n%{http_code}" \
  "$BASE_URL/api/protected")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)

[ "$HTTP_CODE" -eq 401 ] || { echo "[FAIL] Expected 401, got $HTTP_CODE"; exit 1; }

echo "[PASS] Unauthenticated access blocked"
```

### Checklist for API-Test
- [ ] All endpoints tested (GET, POST, PUT, DELETE)
- [ ] Authentication/authorization verified
- [ ] Error responses have correct format
- [ ] Response schemas validated
- [ ] Rate limiting tested (if applicable)
- [ ] CORS headers checked (if applicable)

---

## Manual Validation

### When to Use
- Complex UI/UX flows that are hard to automate
- Visual design verification
- Accessibility testing
- User experience evaluation
- Third-party integrations without API access

### Checklist Template

```markdown
## Manual Validation Checklist

**Feature:** {feature_name}
**Tester:** {name}
**Date:** {date}
**Environment:** {staging/production}

### Pre-Test Setup
- [ ] Environment is accessible: {URL}
- [ ] Test account ready: {credentials location}
- [ ] Test data prepared
- [ ] Browser: {Chrome/Firefox/Safari} v{version}
- [ ] Device: {Desktop/Mobile}

---

### Scenario 1: {Happy Path Name}

**Preconditions:**
- {List required state}

**Steps:**
| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to {page} | Page loads without errors | [ ] |
| 2 | Click {button} | {Result} | [ ] |
| 3 | Enter {data} | {Result} | [ ] |
| 4 | Submit form | {Result} | [ ] |

**Result:** [ ] PASS  [ ] FAIL
**Notes:**

---

### Scenario 2: {Edge Case Name}

[Same format as above]

---

### Visual Verification
- [ ] Layout matches design mockups
- [ ] Colors and fonts are correct
- [ ] Responsive at mobile breakpoints
- [ ] No visual glitches or overflow

### Accessibility Check
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast sufficient
- [ ] Focus states visible

---

### Summary

| Scenario | Result |
|----------|--------|
| Scenario 1 | PASS/FAIL |
| Scenario 2 | PASS/FAIL |
| Visual | PASS/FAIL |
| Accessibility | PASS/FAIL |

**Overall Result:** [ ] PASS  [ ] FAIL

**Issues Found:**
1. {Issue description}

**Sign-Off:**
- Tester: _____________ Date: _______
- Reviewer: _____________ Date: _______
```

### Best Practices for Manual Testing
1. **Document everything** - Screenshots, videos, exact steps
2. **Test on multiple devices** - Desktop, tablet, mobile
3. **Use real-world data** - Not just "test" or "asdf"
4. **Test edge cases** - Empty states, long text, special characters
5. **Verify accessibility** - Keyboard nav, screen readers, contrast

---

## Choosing the Right Method

| Scenario | Recommended Method |
|----------|-------------------|
| Login/logout flow | Playwright |
| API CRUD operations | API-Test |
| Complex checkout process | Playwright + Manual |
| Email integration | API-Test (mock) + Manual |
| Mobile responsiveness | Manual |
| Visual design review | Manual |
| Performance under load | API-Test |
| Security headers | API-Test |
