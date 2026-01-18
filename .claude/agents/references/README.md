# Agent References (Canonical Location)

This directory contains reference materials used by agents during the planning phase. These are the **canonical source** for examples and patterns shared between agents and skills.

## Purpose

1. **Single Source of Truth** - Reference materials are stored here once, avoiding duplication
2. **Agent-First Design** - Agents consume these references during planning
3. **Skill Sharing** - Skills can reference these via relative paths

## Directory Structure

```
references/
├── REFERENCES.json       # Central index and mapping
├── README.md             # This file
├── api-examples/         # API specification examples
│   ├── openapi-example.md
│   ├── graphql-example.md
│   ├── grpc-example.md
│   └── trpc-example.md
└── deployment-examples/  # CI/CD and deployment configs
    ├── github-actions-vercel.md
    ├── gitlab-ci-aws-ecs.md
    ├── docker-compose-self-hosted.md
    └── kubernetes.md
```

## How Agents Use References

Agents load references based on the project's `CLAUDE.md` configuration:

```
IF [stack].api_type == "REST":
    LOAD api-examples/openapi-example.md
ELSE IF [stack].api_type == "GraphQL":
    LOAD api-examples/graphql-example.md
```

See `REFERENCES.json` for the complete mapping.

## How Skills Access These References

Skills can access these references via relative paths:

```markdown
For advanced API patterns, see `../../agents/references/api-examples/openapi-example.md`
```

Or skills can have their own specialized references in their local `references/` directory.

## Adding New References

1. Create the reference file in the appropriate subdirectory
2. Update `REFERENCES.json` with the mapping
3. Update relevant agent `.md` files to reference the new file
4. Update relevant skill `SKILL.md` files if needed

## Relationship with Skill References

| Location | Purpose | Example |
|----------|---------|---------|
| `agents/references/` | Shared examples used during planning | OpenAPI specs, K8s manifests |
| `skills/*/references/` | Skill-specific patterns and guides | React patterns, Backend best practices |

**Rule:** If a reference is used by multiple agents OR shared between agents and skills, it belongs here.
