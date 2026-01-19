---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** This should be run in a dedicated worktree (created by brainstorming skill).

**Save plans to:**

- If `SESSION_FILE` parameter is provided: Save to `SESSION_FILE` path (used by flow-plan)
- Otherwise: Save to `docs/plans/YYYY-MM-DD-<feature-name>.md` (standalone usage)

**Session File Integration:**
When invoked from `/flow-plan`, the SESSION_FILE variable is passed. In this case:

1. Read the existing session file content
2. Update the "Implementation Plan" section with the generated plan
3. Preserve all other sections (Metadata, Summary, Requirements, etc.)
4. Write back to the same SESSION_FILE path

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**

- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```
````

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

```

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Execution Handoff

**IMPORTANT**: Check if `MODE` parameter is set to `planning-only`:
- If `MODE == planning-only`: Skip this entire section. Do NOT offer execution options.
- If `MODE` is not set or is `normal`: Proceed with execution handoff below.

---

**When MODE is NOT planning-only:**

After saving the plan, offer execution choice:

**"Plan complete and saved to `{SESSION_FILE or docs/plans/<filename>.md}`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Stay in this session
- Fresh subagent per task + code review

**If Parallel Session chosen:**
- Guide them to open new session in worktree
- **REQUIRED SUB-SKILL:** New session uses superpowers:executing-plans

---

**When MODE is planning-only (invoked from /flow-plan):**

After saving the plan, output:

**"Plan saved to `{SESSION_FILE}`. Planning complete.**

**Next steps (user action required):**
1. Review the plan in `{SESSION_FILE}`
2. Run `/flow-issue-create {SESSION_FILE}` to create issues
3. Run `/flow-feature-build` to implement"

**Do NOT offer to implement. Do NOT ask "Which approach?"**
```
