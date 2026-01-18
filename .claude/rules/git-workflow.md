# Git Workflow - InformatiK-AI Studio

## Branching Strategy

| Branch | Purpose | Protected |
|--------|---------|-----------|
| `main` | Production | Yes |
| `develop` | Integration | Yes |
| `feature/*` | New features | No |
| `fix/*` | Bug fixes | No |
| `hotfix/*` | Production fixes | No |

## Branch Naming

```
feature/{issue-number}-{short-description}
fix/{issue-number}-{short-description}
hotfix/{issue-number}-{short-description}

Examples:
feature/12-add-claude-integration
fix/45-editor-syntax-error
hotfix/89-api-key-leak
```

## Commit Messages

Use Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance
- `perf`: Performance improvement

**Scopes** (project-specific):
- `editor`: Code editor features
- `ai`: AI generation features
- `preview`: Preview functionality
- `deploy`: Deploy features
- `auth`: Authentication
- `api`: API routes
- `ui`: UI components
- `db`: Database changes

**Examples**:
```
feat(ai): add Claude 3.5 Sonnet support
fix(editor): resolve syntax highlighting for TypeScript
docs(readme): update installation instructions
test(api): add generation endpoint tests
```

## Pull Request Requirements

- [ ] Descriptive title (conventional commit format)
- [ ] Description with context and screenshots (if UI)
- [ ] Link to issue/ticket
- [ ] All tests passing
- [ ] No merge conflicts
- [ ] At least 1 approval
- [ ] Security review (if auth/keys/deploy changes)
- [ ] Acceptance criteria validated

## PR Template

```markdown
## Summary
Brief description of changes

## Type
- [ ] Feature
- [ ] Bug Fix
- [ ] Refactor
- [ ] Documentation

## Testing
- [ ] Unit tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Screenshots (if UI)
[Add screenshots]

## Related Issues
Closes #[issue-number]
```

## Merge Strategy

- **Feature branches**: Squash merge to develop
- **Develop to main**: Merge commit (preserves history)
- **Hotfixes**: Cherry-pick to both main and develop
