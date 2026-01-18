/**
 * Lint-staged Configuration
 * Runs linters and formatters on staged files before commit
 */

module.exports = {
  // TypeScript/JavaScript files
  '*.{ts,tsx,js,jsx,mjs,cjs}': [
    'eslint --fix',           // Lint and auto-fix
    'prettier --write',        // Format code
  ],

  // Astro files
  '*.astro': [
    'eslint --fix',
    'prettier --write',
  ],

  // CSS/Style files
  '*.{css,scss,sass,less}': [
    'prettier --write',
  ],

  // JSON/YAML/Markdown files
  '*.{json,yaml,yml,md,mdx}': [
    'prettier --write',
  ],

  // Type checking for TypeScript files (without fixing)
  '*.{ts,tsx}': () => 'tsc --noEmit',
};
