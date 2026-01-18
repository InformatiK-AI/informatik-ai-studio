#

# Task: RAD Workflow Module (v1.0)

# This is a modular component of flow-feature-build.md
# Do not invoke directly - called by flow-feature-build when WORKFLOW == "RAD"

#

## RAD Workflow: Prototype → Analyze → Iterate → Test

**Workflow Pattern**: Rapid prototyping with iterative refinement (max 3 cycles).

### Prerequisites

- WORKFLOW variable == "RAD"
- Cached context JSON loaded from Phase 0.5
- Feature requirements defined

### Configuration

```
MAX_RAD_ITERATIONS = 3    # Prevents infinite iteration
CURRENT_ITERATION = 1     # Initialize counter
ITERATION_TIMEOUT = 600000 # 10 minutes per iteration
```

### Phase RAD-1: Minimal Viable Prototype

**Purpose**: Build core functionality quickly without polish.

1. **Invoke Architecture Team (non-blocking guidance):**
   ```
   PARALLEL_INVOKE:
     - @domain-logic-architect (if backend work)
     - @frontend-architect (if frontend work)
     - @database-architect (if data model changes)
   Timeout: 300000ms each
   Mode: "guidance" (non-blocking - don't wait for full plans)
   ```

2. **Implement Core Functionality:**
   - Focus on "happy path" only
   - No UI polish, no edge cases
   - Skip error handling for now
   - Get something working FAST

3. **Log Prototype Status:**
   ```
   Log: "RAD Iteration 1 - Prototype complete"
   ```

### Phase RAD-2: Experience Analysis

**Purpose**: Analyze prototype for UX/DX issues.

1. **Invoke Experience Analyzer:**
   ```
   Run @experience-analyzer with:
   - timeout: 300000ms
   - mode: (auto-detect from CLAUDE.md)
     - If UI-heavy project: "ux_analysis" (uses Playwright)
     - If API-heavy project: "dx_analysis" (uses curl)
   - output: .claude/docs/{feature_name}/experience_analysis_iteration_{N}.md
   ```

2. **Analysis Outputs:**
   - **For UX**: Navigation flow, accessibility, visual hierarchy, user friction points
   - **For DX**: Error messages, API consistency, status codes, response formats

3. **Categorize Issues:**
   - **CRITICAL**: Blocking UX/DX problems (must fix)
   - **MAJOR**: Significant issues (should fix)
   - **MINOR**: Nice-to-have improvements (can skip)

### Phase RAD-3: Decision Point

**Purpose**: Determine if another iteration is needed.

1. **Analyze Results:**
   ```python
   critical_issues = count_issues(severity="CRITICAL")
   major_issues = count_issues(severity="MAJOR")

   IF critical_issues == 0 AND major_issues <= 2:
       DECISION = "SKIP_TO_TESTING"
   ELSE IF CURRENT_ITERATION < MAX_RAD_ITERATIONS:
       DECISION = "ITERATE"
   ELSE:
       DECISION = "FORCE_TEST"  # Max iterations reached
   ```

2. **Apply Decision:**
   - **SKIP_TO_TESTING**: Prototype is good enough → Go to Phase RAD-6
   - **ITERATE**: Issues found → Go to Phase RAD-4
   - **FORCE_TEST**: Max iterations → Log warning, go to Phase RAD-6

### Phase RAD-4: Refinement (Iteration 2)

**Only runs if DECISION == "ITERATE" and CURRENT_ITERATION < MAX_RAD_ITERATIONS**

1. **Increment Counter:**
   ```
   CURRENT_ITERATION += 1
   ```

2. **Address Critical Issues:**
   - Fix ONLY critical issues from previous analysis
   - Do NOT add new features
   - Focus on improving existing functionality
   - Examples:
     - UX: Fix navigation flow, improve accessibility
     - DX: Improve error responses, add validation

3. **Re-Analyze:**
   - Return to Phase RAD-2 with updated prototype
   - Generate new analysis file (iteration_2.md)
   - Compare improvement delta from iteration_1

4. **Decision Point Again:**
   - If significant improvement AND remaining issues → Iteration 3
   - If good enough → Phase RAD-6

### Phase RAD-5: Polish (Iteration 3 - Optional)

**Only runs if previous iteration has remaining issues and CURRENT_ITERATION < 3**

1. **Increment Counter:**
   ```
   CURRENT_ITERATION += 1  # Now equals 3
   ```

2. **Address Nice-to-Have Improvements:**
   - Loading states and animations
   - Micro-interactions
   - Documentation improvements
   - Consistent naming

3. **Final Analysis:**
   - Generate `experience_analysis_iteration_3.md`
   - Document final state

4. **Force Proceed:**
   ```
   Log: "RAD workflow reached max iterations (3)"
   GOTO Phase RAD-6
   ```

### Phase RAD-6: Comprehensive Testing

**Purpose**: Write tests after prototype is stable.

1. **Invoke Test Strategy Planner:**
   ```
   Run @test-strategy-planner with:
   - timeout: 300000ms
   - input: Final prototype, all iteration analysis files
   - output: test_cases.md
   ```

2. **Invoke Test Engineer:**
   ```
   Run @implementation-test-engineer with:
   - timeout: 300000ms
   - input: test_cases.md
   - mode: "comprehensive" (cover all iterations)
   ```

3. **Run Tests:**
   ```bash
   npm test / pytest / go test
   ```

4. **Verify Coverage:**
   - Check test coverage meets requirements
   - All core functionality covered
   - Edge cases from iterations 2/3 included

### Exit Conditions

**Success**: Testing complete, coverage met
- Return to flow-feature-build Phase 1.5 (Plan Validation Gate)
- Set ITERATIONS_USED = CURRENT_ITERATION

**Failure**: Cannot stabilize after 3 iterations + testing fails
- Escalate to user with full iteration history
- Set TASK_STATUS = "rad_blocked"

### Metrics

```
Log metrics:
- rad_iterations_used: CURRENT_ITERATION
- critical_issues_resolved: count
- total_analysis_time: sum of analysis phases
- prototype_to_test_time: total RAD workflow time
```

---

## Version

**Version**: 1.0.0
**Extracted From**: flow-feature-build.md v3.3
**Created**: 2026-01-17
