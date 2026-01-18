# Gherkin Best Practices Guide

## Overview

Gherkin is a domain-specific language for writing acceptance criteria in a human-readable format. This guide ensures consistent, testable, and maintainable scenarios.

## Basic Syntax

```gherkin
Feature: {Feature Name}
  {Feature description}

  Background:
    Given {shared precondition for all scenarios}

  Scenario: {Scenario Name}
    Given {precondition/context}
    When {action taken}
    Then {expected outcome}
    And {additional outcome}
```

## The GIVEN-WHEN-THEN Pattern

### GIVEN (Preconditions)
Describes the initial state before the action.

**Good:**
```gherkin
Given the user is logged in as "admin"
Given the shopping cart contains 3 items
Given the API rate limit is set to 100 requests/minute
```

**Bad:**
```gherkin
Given the system works  # Too vague
Given everything is set up  # Not specific
```

### WHEN (Actions)
Describes the action or event being tested.

**Good:**
```gherkin
When the user clicks the "Submit" button
When the user sends a POST request to "/api/orders"
When the session expires after 30 minutes of inactivity
```

**Bad:**
```gherkin
When the user does something  # Too vague
When things happen  # Not actionable
```

### THEN (Outcomes)
Describes the expected result.

**Good:**
```gherkin
Then the user should see the message "Order confirmed"
Then the response status should be 201
Then a confirmation email should be sent to the user
```

**Bad:**
```gherkin
Then it should work  # Not measurable
Then the system should be fast  # Not specific
```

## SMART Criteria

Every acceptance criterion should be **SMART**:

| Attribute | Meaning | Example |
|-----------|---------|---------|
| **S**pecific | Clear and unambiguous | "Status code 200" not "success" |
| **M**easurable | Can be verified objectively | "Response < 500ms" |
| **A**chievable | Technically possible to test | Avoid testing external services |
| **R**elevant | Relates to the feature goal | Focus on user value |
| **T**ime-bound | Has clear boundaries | "Within 5 seconds" |

## Tags for Organization

Use tags to categorize scenarios:

```gherkin
@critical           # Must pass for release
@happy-path         # Primary success flow
@edge-case          # Boundary conditions
@error-handling     # Expected failure scenarios
@security           # Security-related tests
@performance        # Performance-related tests
@wip                # Work in progress (skip in CI)
```

## Anti-Patterns to Avoid

### 1. UI Implementation Details
**Bad:**
```gherkin
When the user clicks the div with class "btn-primary"
```
**Good:**
```gherkin
When the user clicks the "Submit" button
```

### 2. Multiple Actions in One Step
**Bad:**
```gherkin
When the user logs in and navigates to dashboard and creates a new project
```
**Good:**
```gherkin
When the user logs in
And the user navigates to the dashboard
And the user creates a new project
```

### 3. Testing Implementation, Not Behavior
**Bad:**
```gherkin
Then the database should have a new row in the users table
```
**Good:**
```gherkin
Then the user should appear in the admin user list
```

### 4. Vague Outcomes
**Bad:**
```gherkin
Then the page should load correctly
```
**Good:**
```gherkin
Then the page title should be "Dashboard"
And the user's name should be displayed in the header
```

### 5. Dependent Scenarios
**Bad:** Scenarios that require other scenarios to run first.
**Good:** Each scenario is independent with its own setup.

## Background Section

Use `Background` for shared preconditions:

```gherkin
Feature: Shopping Cart

  Background:
    Given the user is logged in
    And the product catalog is available

  Scenario: Add item to cart
    When the user adds "Laptop" to the cart
    Then the cart should contain 1 item

  Scenario: Remove item from cart
    Given the cart contains "Laptop"
    When the user removes "Laptop" from the cart
    Then the cart should be empty
```

## Scenario Outlines for Data-Driven Tests

```gherkin
Scenario Outline: Login validation
  Given the user is on the login page
  When the user enters "<email>" and "<password>"
  Then the result should be "<result>"

  Examples:
    | email              | password    | result        |
    | valid@example.com  | correct123  | success       |
    | valid@example.com  | wrong       | invalid_creds |
    | invalid            | any         | invalid_email |
    | (empty)            | (empty)     | required      |
```

## Minimum Coverage Requirements

For each feature, ensure:

- [ ] At least 1 happy path scenario (@critical)
- [ ] At least 2 edge case scenarios
- [ ] At least 1 error handling scenario
- [ ] Security scenarios for auth/data features
- [ ] Performance criteria where applicable

## Quick Reference

| Element | Purpose | Example |
|---------|---------|---------|
| Feature | Group related scenarios | `Feature: User Login` |
| Background | Shared setup | `Given the user is logged in` |
| Scenario | Single test case | `Scenario: Valid login` |
| Given | Precondition | `Given the user exists` |
| When | Action | `When the user submits` |
| Then | Outcome | `Then success is shown` |
| And/But | Chain steps | `And the email is sent` |
| @tag | Categorization | `@critical @security` |
