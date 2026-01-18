#

# Task: TDD Workflow Module (v1.0)

# This is a modular component of flow-feature-build.md
# Do not invoke directly - called by flow-feature-build when WORKFLOW == "TDD"

#

## TDD Workflow: Strategy → Red → Green → Refactor

**Workflow Pattern**: Test-first development with explicit test planning phase.

### Prerequisites

- WORKFLOW variable == "TDD"
- Cached context JSON loaded from Phase 0.5
- Feature requirements defined

### Phase TDD-0: Strategy - Test Planning

**Purpose**: Plan test strategy before writing any test code (per dag.json dependency).

1. **Invoke `@test-strategy-planner` agent:**
   ```
   Run @test-strategy-planner with:
   - timeout: 300000ms
   - input: Feature requirements, CLAUDE.md, cached context JSON
   - output: .claude/docs/{feature_name}/test_cases.md
   ```

2. **Validate Output:**
   - Check `test_cases.md` exists and contains Gherkin scenarios
   - Verify test coverage plan addresses all acceptance criteria
   - **GATE**: Cannot proceed to Red Phase without `test_cases.md`

3. **Test Strategy Contents:**
   - Unit test scenarios (with expected inputs/outputs)
   - Integration test scenarios
   - Edge cases and error conditions
   - Performance test considerations (if applicable)

### Phase TDD-1: Red - Write Failing Tests

**Purpose**: Write tests that capture desired behavior before implementation.

1. **Invoke `@implementation-test-engineer` agent:**
   ```
   Run @implementation-test-engineer with:
   - timeout: 300000ms
   - input: test_cases.md (REQUIRED - from Strategy Phase)
   - mode: "write_failing_tests"
   ```

2. **Run Tests:**
   ```bash
   # Execute test suite
   npm test / pytest / go test (per project config)
   ```

3. **Validate Red State:**
   - Tests MUST fail (red)
   - If tests pass: Something is wrong - review test logic
   - Log: "Red Phase complete - {N} failing tests"

### Phase TDD-2: Green - Implement Minimum Code

**Purpose**: Write minimum code to make tests pass.

1. **Invoke Architecture Team (per feature scope):**

   **For Backend/API changes** (sequential per dag.json layers):
   ```
   Layer 1: @database-architect (if database changes needed)
            → Wait for database.md
   Layer 2: @api-contract-designer (if API endpoints involved)
            → Wait for api_contract.md
   Layer 3: @domain-logic-architect (business logic)
            → Wait for backend.md
   ```

   **For Frontend/UI changes:**
   ```
   @frontend-architect (component architecture)
   → Wait for frontend.md
   ```

   **For Full-stack changes** (PARALLEL where possible):
   ```
   Layers 1-2: Sequential (database → api-contract)
   Layer 3: PARALLEL (@domain-logic-architect, @frontend-architect)
   Layer 4: @security-architect (MANDATORY gate)
   ```

2. **Implement Following Plans:**
   - Follow architect plans to implement minimum viable code
   - Focus on making tests pass, not perfection
   - No premature optimization

3. **Run Tests:**
   ```bash
   npm test / pytest / go test
   ```

4. **Validate Green State:**
   - All tests MUST pass (green)
   - If tests fail: Continue implementing until green
   - Log: "Green Phase complete - all tests passing"

### Phase TDD-3: Refactor - Improve Code Quality

**Purpose**: Improve code while keeping tests passing.

1. **Code Quality Improvements:**
   - Extract duplicate code
   - Improve naming and readability
   - Apply design patterns where appropriate
   - Remove dead code

2. **Continuous Test Execution:**
   ```bash
   # Run tests after each refactor step
   npm test / pytest / go test
   ```

3. **Maintain Green State:**
   - Tests MUST remain passing throughout refactoring
   - If tests break: Revert last change, try smaller refactor
   - Log: "Refactor complete - tests still passing"

4. **Final Verification:**
   ```
   Run @implementation-test-engineer with:
   - mode: "verify_coverage"
   - minimum_coverage: (from CLAUDE.md or default 80%)
   ```

### Exit Conditions

**Success**: All phases complete, tests green, coverage met
- Return to flow-feature-build Phase 1.5 (Plan Validation Gate)

**Failure**: Cannot achieve green state after 3 implementation attempts
- Escalate to user with diagnostic report
- Set TASK_STATUS = "tdd_blocked"

---

## Version

**Version**: 1.0.0
**Extracted From**: flow-feature-build.md v3.3
**Created**: 2026-01-17
