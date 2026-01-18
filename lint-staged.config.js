/**
 * ABOUTME: Lint-staged configuration for pre-commit hooks
 * RESPONSIBILITY: Run linters/formatters only on staged files
 * DEPENDENCIES: ESLint, Prettier, TypeScript
 */

module.exports = {
  // TypeScript and JavaScript files (exclude next-env.d.ts which is auto-generated)
  '!(next-env).{ts,tsx}': ['eslint --fix --max-warnings=0 --no-warn-ignored', 'prettier --write'],

  // JSON files (exclude tsconfig)
  '!(tsconfig).json': ['prettier --write'],

  // Markdown files
  '*.md': ['prettier --write'],

  // CSS and styling
  '*.{css,scss}': ['prettier --write'],

  // Type checking for TypeScript (run on all TS files if any staged)
  '**/*.{ts,tsx}': () => 'pnpm tsc --noEmit',
};
