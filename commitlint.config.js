/**
 * ABOUTME: Commitlint configuration for Conventional Commits validation
 * RESPONSIBILITY: Enforce consistent commit message format
 * DEPENDENCIES: @commitlint/cli, @commitlint/config-conventional
 */

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Type must be one of the following
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting (no code change)
        'refactor', // Code restructure
        'test',     // Tests
        'chore',    // Maintenance
        'perf',     // Performance improvement
        'ci',       // CI/CD changes
        'build',    // Build system changes
        'revert',   // Revert previous commit
      ],
    ],

    // Scope is optional but recommended
    'scope-enum': [
      1, // Warning level
      'always',
      [
        'editor',   // Code editor features
        'ai',       // AI generation features
        'preview',  // Preview functionality
        'deploy',   // Deploy features
        'auth',     // Authentication
        'api',      // API routes
        'ui',       // UI components
        'db',       // Database changes
        'config',   // Configuration
        'deps',     // Dependencies
      ],
    ],

    // Subject (description) rules
    'subject-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-max-length': [2, 'always', 72],

    // Header rules
    'header-max-length': [2, 'always', 100],

    // Body rules
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 100],

    // Footer rules
    'footer-leading-blank': [2, 'always'],
  },
};
