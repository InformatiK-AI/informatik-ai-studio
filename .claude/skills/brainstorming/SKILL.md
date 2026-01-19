---
name: brainstorming
description: 'You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.'
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**IMPORTANT**: Check if `MODE` parameter is set to `planning-only`:

- If `MODE == planning-only`: Skip the "Implementation" section entirely. Do NOT ask about implementation.
- If `MODE` is not set or is `normal`: Proceed with both documentation and implementation offer.

---

### Documentation

**Output Location:**

- If `PLAN_NAME` parameter is provided: Write to `.claude/docs/{PLAN_NAME}/brainstorming.md` (used by /flow-plan)
- Otherwise: Write to `docs/plans/YYYY-MM-DD-<topic>-design.md` (standalone usage)

**CRITICAL: Use the Write tool explicitly:**

1. Determine the output path based on parameters above
2. Use the Write tool to create the file with the validated design
3. Include all sections: Overview, Approach, Architecture, Components, Data Flow, Error Handling, Testing
4. Use elements-of-style:writing-clearly-and-concisely skill if available
5. Commit the design document to git

**Template Structure:**

```markdown
# Design: {Feature Name}

## Overview

{Brief description and goals}

## Approach

{Chosen approach and rationale}

## Architecture

{High-level architecture decisions}

## Components

{Key components and their responsibilities}

## Data Flow

{How data moves through the system}

## Error Handling

{Error scenarios and handling strategy}

## Testing Strategy

{How this will be tested}
```

**Do NOT skip the Write step** - the design file MUST be created.

---

### Implementation (Skip if MODE is planning-only)

**When MODE is NOT planning-only:**

- Ask: "Ready to set up for implementation?"
- Use superpowers:using-git-worktrees to create isolated workspace
- Use superpowers:writing-plans to create detailed implementation plan

**When MODE is planning-only (invoked from /flow-plan):**

- Do NOT ask about implementation
- Do NOT offer to create worktrees
- STOP after writing the design file
- Output: "Design saved to `{output_path}`. Brainstorming complete."

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense
