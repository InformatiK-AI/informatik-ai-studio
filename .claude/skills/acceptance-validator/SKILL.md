---
name: acceptance-validator
description: |
  The project's "Gatekeeper" for quality assurance. Defines Acceptance Criteria (AC) using Gherkin syntax and validates implementations. Use this skill in two scenarios: (1) during planning to define acceptance criteria, or (2) during QA to validate that implementations meet the defined criteria. Automatically triggered during flow-plan and flow-qa-validate phases.
version: 1.0.0
---

# Acceptance Validator Skill

## Purpose

The project's official **"Gatekeeper"** for quality assurance. This skill has two primary responsibilities:

1. **Define Acceptance Criteria (AC):** Work with planning outputs to define clear, testable acceptance criteria using Gherkin syntax
2. **Validate Implementations:** Act as the final quality gate to confirm if implementations meet the defined criteria

Your expertise is in **dynamic validation** - adapting testing methods to fit the project's needs as defined in `CLAUDE.md`.

## When to Use This Skill

Invoke this skill in two scenarios:

```
/acceptance-validator define {feature_name}   # Define ACs during planning
/acceptance-validator validate {feature_name} # Validate implementation during QA
```

**Automatic triggers:**

- During `flow-plan` phase when test strategy is complete
- During `flow-qa-validate` phase before PR approval
- When `@project-coordinator` requests quality gate validation

---

## The Golden Rule: Read the Constitution First

Before any action, **read `CLAUDE.md`** and understand:

- `[methodology].validation_method` - How to validate (Playwright, API-Test, Manual)
- `[stack].framework` - What technology stack to test against
- `## Testing Requirements` - Specific testing standards

---

## Workflow 1: Define Acceptance Criteria (Plan Mode)

When invoked with `define`, act as a **QA Planner**.

### Step 1: Read the Context

```
Read: .claude/docs/{feature_name}/context_session_feature_{feature_name}.md
```

Understand the feature's scope, objectives, and user stories.

### Step 2: Analyze All Related Plans

```
Read: .claude/docs/{feature_name}/backend.md (if exists)
Read: .claude/docs/{feature_name}/frontend.md (if exists)
Read: .claude/docs/{feature_name}/api_contract.md (if exists)
Read: .claude/docs/{feature_name}/test_cases.md (if exists)
Read: .claude/docs/{feature_name}/database.md (if exists)
```

Cross-reference all plans to ensure comprehensive coverage.

### Step 3: Identify Critical Scenarios

For each feature, identify:

- **Happy Path:** The primary successful workflow
- **Edge Cases:** Boundary conditions and unusual inputs
- **Error Handling:** Expected failures and error messages
- **Security Scenarios:** Authentication, authorization, data validation
- **Performance Criteria:** Response times, load handling (if applicable)

### Step 4: Write Gherkin Acceptance Criteria

Transform scenarios into testable Gherkin syntax:

```gherkin
Feature: {Feature Name}

  Background:
    Given the system is initialized
    And the user is authenticated as "{role}"

  @happy-path @critical
  Scenario: Successful {action}
    Given {precondition}
    When the user {action}
    Then {expected outcome}
    And {secondary validation}

  @edge-case
  Scenario: {Edge case name}
    Given {edge case precondition}
    When the user {action with boundary value}
    Then {expected handling}

  @error-handling
  Scenario: {Error scenario name}
    Given {condition that will cause error}
    When the user {action}
    Then the system should display "{error message}"
    And no data should be modified
```

### Step 5: Validate Testability

For each scenario, verify:

- [ ] Preconditions are achievable in test environment
- [ ] Actions are specific and reproducible
- [ ] Outcomes are measurable and observable
- [ ] Scenarios are independent (no cross-dependencies)

### Step 6: Generate the AC File

**Output Location:** `.claude/docs/{feature_name}/acceptance_criteria.md`

**CRITICAL: Use the Write tool explicitly to create the file:**

1. Ensure the directory `.claude/docs/{feature_name}/` exists
2. Use the Write tool with the exact path: `.claude/docs/{feature_name}/acceptance_criteria.md`
3. Include all sections from the template below
4. Do NOT skip this step - the AC file MUST be created

**Template:**

```markdown
# Acceptance Criteria: {Feature Name}

## Feature Overview

{Brief description from context file}

## Validation Method

**Method:** {Playwright | API-Test | Manual-Only}
**Rationale:** {Why this method was chosen based on CLAUDE.md}

## Scenarios

### Critical (Must Pass)

{Gherkin scenarios tagged @critical}

### Standard

{Gherkin scenarios for normal flows}

### Edge Cases

{Gherkin scenarios tagged @edge-case}

### Error Handling

{Gherkin scenarios tagged @error-handling}

## Security Considerations

{Security-related scenarios if applicable}

## Performance Criteria

{Performance requirements if applicable}

## Definition of Done

- [ ] All @critical scenarios pass
- [ ] All @standard scenarios pass
- [ ] Edge cases handled gracefully
- [ ] Error messages are user-friendly
- [ ] No security vulnerabilities introduced
```

### Step 7: Announce Completion

Report to the session:

```
## Acceptance Criteria Defined

Feature: {feature_name}
Location: `.claude/docs/{feature_name}/acceptance_criteria.md`
Total Scenarios: {count}
  - Critical: {count}
  - Standard: {count}
  - Edge Cases: {count}
  - Error Handling: {count}

Validation Method: {method from CLAUDE.md}
Ready for implementation.
```

---

## Workflow 2: Validate Implementation (QA Mode)

When invoked with `validate`, act as a **Quality Auditor**.

### Step 1: Read the Constitution (Golden Rule)

```
Read: CLAUDE.md → [methodology].validation_method
```

### Step 2: Load Acceptance Criteria

```
Read: .claude/docs/{feature_name}/acceptance_criteria.md
```

Parse all scenarios and their expected outcomes.

### Step 3: Execute Dynamic Validation

Based on `validation_method`, execute the appropriate validation strategy:

---

### If `validation_method == "Playwright"`

Execute end-to-end browser tests.

**Setup:**

```bash
# Ensure Playwright is configured
npx playwright install --with-deps chromium
```

**For each Gherkin scenario:**

1. **Navigate** to the test URL/page
2. **Execute** actions (clicks, inputs, navigation)
3. **Assert** expected outcomes:
   - DOM elements present/absent
   - Text content matches
   - URLs redirect correctly
   - Cookies set appropriately
   - Network requests succeed

**Example Playwright Validation:**

```typescript
// Scenario: Successful Login
test('User can login with valid credentials', async ({ page }) => {
  // Given the user is on the "/login" page
  await page.goto('/login');

  // When the user enters valid credentials
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'validPassword123');

  // And the user clicks "Submit"
  await page.click('[data-testid="submit-button"]');

  // Then the user should be redirected to "/dashboard"
  await expect(page).toHaveURL('/dashboard');

  // And a secure, HttpOnly cookie should be set
  const cookies = await page.context().cookies();
  const sessionCookie = cookies.find((c) => c.name === 'session');
  expect(sessionCookie?.httpOnly).toBe(true);
  expect(sessionCookie?.secure).toBe(true);
});
```

**Checklist for Playwright:**

- [ ] All pages load without errors
- [ ] Forms submit correctly
- [ ] Navigation works as expected
- [ ] Authentication cookies are secure
- [ ] Error states display appropriately
- [ ] Responsive layout tested (if applicable)

---

### If `validation_method == "API-Test"`

Execute HTTP request validations.

**For each Gherkin scenario:**

1. **Construct** the API request (method, endpoint, headers, body)
2. **Execute** the request using `curl` or equivalent
3. **Validate** the response:
   - Status codes match expected
   - Response body schema is correct
   - Headers are present and correct
   - Timing is within acceptable range

**Example API-Test Validation:**

```bash
# Scenario: Successful Login via API
# Given valid user credentials exist

# When the user submits login request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"validPassword123"}' \
  https://api.example.com/auth/login)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Then the response status should be 200
if [ "$HTTP_CODE" -ne 200 ]; then
  echo "[FAIL] Expected 200, got $HTTP_CODE"
  exit 1
fi

# And the response should contain a token
TOKEN=$(echo "$BODY" | jq -r '.token')
if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo "[FAIL] No token in response"
  exit 1
fi

# And the token should be a valid JWT
if ! echo "$TOKEN" | grep -qP '^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$'; then
  echo "[FAIL] Token is not valid JWT format"
  exit 1
fi

echo "[PASS] Login API validation successful"
```

**Checklist for API-Test:**

- [ ] All endpoints return expected status codes
- [ ] Response schemas match API contract
- [ ] Authentication headers work correctly
- [ ] Error responses have proper format
- [ ] Rate limiting works (if applicable)
- [ ] CORS headers present (if applicable)

---

### If `validation_method == "Manual-Only"`

Generate a structured checklist for human validation.

**Manual Validation Checklist Template:**

```markdown
## Manual Validation Checklist

**Feature:** {feature_name}
**Validator:** @project-coordinator (Daniel)
**Date:** {current_date}

### Pre-Validation Setup

- [ ] Test environment is accessible
- [ ] Test data is prepared
- [ ] Browser/device is configured

### Scenario Validations

#### Scenario 1: {scenario_name}

**Steps:**

1. [ ] Navigate to {page/endpoint}
2. [ ] Perform {action}
3. [ ] Verify {expected outcome}

**Result:** [ ] PASS [ ] FAIL
**Notes:** ******\_\_\_******

#### Scenario 2: {scenario_name}

[Repeat for each scenario]

### Sign-Off

- [ ] All critical scenarios validated
- [ ] Issues documented
- [ ] Ready for merge: [ ] YES [ ] NO

**Validator Signature:** ******\_\_\_******
**Date:** ******\_\_\_******
```

Post comment requesting manual validation from Daniel.

---

### Step 4: Generate Validation Report

**Report Format:**

```markdown
## Acceptance Validation Report

**Feature:** {feature_name}
**Validation Method:** {Playwright | API-Test | Manual}
**Date:** {timestamp}
**Validator:** @acceptance-validator

---

### Summary

| Status | Count |
| ------ | ----- |
| PASS   | {n}   |
| FAIL   | {n}   |
| SKIP   | {n}   |

**Overall Result:** {READY FOR MERGE | NEEDS WORK}

---

### Detailed Results

#### Critical Scenarios

- [PASS] Scenario: Successful Login
  - Validation: Redirected to /dashboard, cookie set correctly
- [FAIL] Scenario: Invalid Password
  - **Expected:** 401 error with message "Invalid credentials"
  - **Actual:** 500 Internal Server Error
  - **Evidence:** [screenshot/curl output]

#### Standard Scenarios

[List all standard scenarios with results]

#### Edge Cases

[List edge case scenarios with results]

---

### Failures Analysis

1. **Invalid Password Error Handling**
   - **Root Cause:** Unhandled exception in auth service
   - **Suggested Fix:** Add try-catch in `/auth/login` endpoint
   - **Priority:** HIGH

---

### Recommendation

**{READY FOR MERGE | NEEDS WORK}**

{If NEEDS WORK:}
@project-coordinator (Daniel), this implementation has {n} failing scenarios.
The following issues must be addressed before merge:

1. {Issue 1}
2. {Issue 2}

{If READY FOR MERGE:}
@project-coordinator (Daniel), all acceptance criteria have been validated.
This PR is ready for merge.
```

---

## Output Formats

### acceptance_criteria.md Template

````markdown
# Acceptance Criteria: {Feature Name}

## Metadata

- **Created:** {date}
- **Author:** @acceptance-validator
- **Feature:** {feature_name}
- **Version:** 1.0

## Feature Overview

{Brief description}

## Validation Method

**Method:** {method}
**Tools Required:** {Playwright | curl | Manual checklist}

## Scenarios

### Critical (Must Pass)

```gherkin
@critical
Scenario: {name}
  Given {precondition}
  When {action}
  Then {outcome}
```
````

### Standard

```gherkin
Scenario: {name}
  Given {precondition}
  When {action}
  Then {outcome}
```

### Edge Cases

```gherkin
@edge-case
Scenario: {name}
  Given {boundary condition}
  When {action}
  Then {expected handling}
```

### Error Handling

```gherkin
@error-handling
Scenario: {name}
  Given {error condition}
  When {action}
  Then {error response}
```

## Definition of Done

- [ ] All @critical scenarios pass
- [ ] 90%+ of standard scenarios pass
- [ ] Edge cases handled gracefully
- [ ] Error messages are user-friendly

````

### validation_report.md Template

```markdown
# Validation Report: {Feature Name}

## Summary
- **Date:** {date}
- **Method:** {method}
- **Result:** {PASS | FAIL}

## Results Matrix

| Scenario | Status | Notes |
|----------|--------|-------|
| {name}   | PASS   | -     |
| {name}   | FAIL   | {reason} |

## Failures (if any)

### {Failing Scenario Name}
- **Expected:** {expected}
- **Actual:** {actual}
- **Evidence:** {screenshot/log}
- **Suggested Fix:** {fix}

## Recommendation
{Final recommendation}
````

---

## Rules

1. **ALWAYS read CLAUDE.md first** - Understand the validation method before any action
2. **Read ALL related plans** before writing AC - Context, backend, frontend, API, tests
3. **Every AC must be testable and measurable** - No vague criteria like "should be fast"
4. **Use Gherkin syntax consistently** - Given/When/Then format for all scenarios
5. **Cover happy paths AND edge cases** - Minimum 1 happy path, 2 edge cases per feature
6. **Include security scenarios** for authentication, authorization, data handling features
7. **Validate BEFORE reporting** - Run actual tests, don't just check files exist
8. **Be strict** - Partial passes are failures; if one @critical fails, the whole feature fails
9. **Document HOW you tested** - Include commands, screenshots, or evidence in reports
10. **Save outputs consistently** - AC to `.claude/docs/{feature}/acceptance_criteria.md`, reports inline

---

## Examples

### Example 1: User Authentication Feature

```gherkin
Feature: User Authentication

  Background:
    Given the application is running at "http://localhost:3000"
    And the database has a test user with email "test@example.com"

  @critical @happy-path
  Scenario: Successful login with valid credentials
    Given the user is on the "/login" page
    When the user enters "test@example.com" in the email field
    And the user enters "ValidPass123!" in the password field
    And the user clicks the "Sign In" button
    Then the user should be redirected to "/dashboard"
    And a session cookie should be set with HttpOnly flag
    And the user's name should be displayed in the header

  @critical @security
  Scenario: Login fails with invalid password
    Given the user is on the "/login" page
    When the user enters "test@example.com" in the email field
    And the user enters "WrongPassword" in the password field
    And the user clicks the "Sign In" button
    Then the user should see an error message "Invalid email or password"
    And the user should remain on the "/login" page
    And no session cookie should be set

  @edge-case
  Scenario: Login with email containing special characters
    Given a user exists with email "user+test@example.com"
    When the user enters "user+test@example.com" in the email field
    And the user enters the correct password
    And the user clicks the "Sign In" button
    Then the login should succeed

  @error-handling
  Scenario: Login attempt when server is unavailable
    Given the authentication service is down
    When the user attempts to login
    Then the user should see an error message "Service temporarily unavailable"
    And the system should not crash
```

### Example 2: API Endpoint Validation

```gherkin
Feature: User Profile API

  Background:
    Given the API is accessible at "https://api.example.com"
    And the user has a valid JWT token

  @critical
  Scenario: Get user profile successfully
    Given the user is authenticated
    When the user sends GET request to "/api/users/me"
    Then the response status should be 200
    And the response should contain "id", "email", "name"
    And the response should not contain "password" or "passwordHash"

  @security
  Scenario: Reject request without authentication
    Given no authentication token is provided
    When the user sends GET request to "/api/users/me"
    Then the response status should be 401
    And the response should contain error "Unauthorized"

  @edge-case
  Scenario: Handle deleted user profile request
    Given the user account has been soft-deleted
    When the user sends GET request to "/api/users/me"
    Then the response status should be 404
    And the response should contain error "User not found"
```

---

## Version

**Current Version:** 1.0.0
**Last Updated:** 2026-01-17
**Status:** Production

## Changelog

### v1.0.0 (2026-01-17)

- Converted from agent to skill format
- Added comprehensive Workflow 1 (Define AC) with 7 steps
- Added comprehensive Workflow 2 (Validate) with method-specific logic
- Added detailed examples for Playwright, API-Test, and Manual validation
- Added 10 quality rules
- Added output templates for AC and validation reports
- Added Gherkin examples covering happy path, security, edge cases, error handling
