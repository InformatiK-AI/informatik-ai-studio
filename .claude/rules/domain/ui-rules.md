---
description: Rules for UI components, pages, and layouts
paths:
  - "components/**"
  - "app/**/page.tsx"
  - "app/**/layout.tsx"
  - "**/*.component.tsx"
---

# UI Development Rules - InformatiK-AI Studio

## Component Structure

### File Organization

```
components/
├── ui/                    # shadcn/ui primitives
│   ├── button.tsx
│   ├── input.tsx
│   └── ...
├── editor/               # Editor-specific components
│   ├── code-editor.tsx   # Monaco wrapper
│   ├── file-tree.tsx     # File explorer
│   └── toolbar.tsx       # Editor toolbar
├── preview/              # Preview components
│   ├── preview-frame.tsx # Iframe preview
│   └── console.tsx       # Console output
├── project/              # Project management
│   ├── project-card.tsx
│   └── project-list.tsx
└── shared/               # Shared components
    ├── header.tsx
    └── sidebar.tsx
```

### Component Template

```tsx
/**
 * ABOUTME: [What this component does]
 * RESPONSIBILITY: [Primary responsibility]
 */
'use client'; // Only if needed

import { useState, useCallback } from 'react';
import { cn } from '@/lib/utils';

interface CodeEditorProps {
  /** Initial code content */
  initialValue?: string;
  /** Language for syntax highlighting */
  language: 'typescript' | 'javascript' | 'html' | 'css';
  /** Callback when content changes */
  onChange?: (value: string) => void;
  /** Read-only mode */
  readOnly?: boolean;
}

export function CodeEditor({
  initialValue = '',
  language,
  onChange,
  readOnly = false,
}: CodeEditorProps) {
  // 1. Hooks first
  const [value, setValue] = useState(initialValue);

  // 2. Handlers
  const handleChange = useCallback((newValue: string) => {
    setValue(newValue);
    onChange?.(newValue);
  }, [onChange]);

  // 3. Render
  return (
    <div className={cn(
      "h-full w-full",
      readOnly && "opacity-75"
    )}>
      {/* Monaco Editor implementation */}
    </div>
  );
}
```

## Styling with Tailwind

### Class Organization

```tsx
<div className={cn(
  // Layout
  "flex flex-col gap-4",
  // Sizing
  "h-full w-full min-h-[400px]",
  // Colors/Background
  "bg-background text-foreground",
  // Border/Shadow
  "border border-border rounded-lg shadow-sm",
  // States
  "hover:border-primary focus-within:ring-2",
  // Conditional
  isActive && "ring-2 ring-primary",
  className
)}>
```

### Dark Mode Support

All components MUST support dark mode via CSS variables:

```tsx
// Use semantic color tokens
<div className="bg-background text-foreground">
  <span className="text-muted-foreground">Secondary text</span>
  <Button variant="primary">Action</Button>
</div>

// NOT hardcoded colors
<div className="bg-white text-black"> // WRONG
```

### Responsive Design

Mobile-first approach:

```tsx
<div className="
  p-4 md:p-6 lg:p-8
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
  text-sm md:text-base
">
```

## Editor-Specific Rules

### Monaco Editor Integration

```tsx
import Editor from '@monaco-editor/react';

export function CodeEditor({ value, onChange, language }: Props) {
  return (
    <Editor
      height="100%"
      language={language}
      value={value}
      onChange={onChange}
      theme="vs-dark" // or "light" based on theme
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        tabSize: 2,
        wordWrap: 'on',
        automaticLayout: true,
      }}
    />
  );
}
```

### Preview Frame Isolation

```tsx
// Preview MUST be isolated in sandbox iframe
<iframe
  ref={iframeRef}
  sandbox="allow-scripts allow-same-origin"
  className="w-full h-full bg-white"
  srcDoc={previewHtml}
/>
```

## Accessibility

### Required

- [ ] All images have alt text
- [ ] Interactive elements are focusable
- [ ] Keyboard navigation works
- [ ] Labels for all form inputs
- [ ] Proper heading hierarchy
- [ ] Color is not the only indicator

### Focus Management

```tsx
// Trap focus in modals
import { FocusTrap } from '@/components/ui/focus-trap';

<FocusTrap>
  <Dialog>...</Dialog>
</FocusTrap>
```

## Loading States

Every async operation MUST show loading state:

```tsx
function ProjectList() {
  const { data, isLoading, error } = useProjects();

  if (isLoading) return <ProjectListSkeleton />;
  if (error) return <ErrorState error={error} />;
  if (!data?.length) return <EmptyState />;

  return <div>{/* render projects */}</div>;
}
```

## Performance

- Use `React.memo` for list items
- Lazy load below-fold content
- Virtualize long file lists
- Debounce editor onChange (300ms)
- Use `useCallback` for handlers passed to children
