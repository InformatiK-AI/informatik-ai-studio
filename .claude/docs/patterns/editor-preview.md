# Editor & Preview Patterns - InformatiK-AI Studio

> Load this document when working on the Monaco Editor integration or real-time preview system.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Editor Layout                             │
├─────────────┬───────────────────────┬───────────────────────┤
│  File Tree  │    Monaco Editor      │   Preview Frame       │
│   (200px)   │      (flexible)       │     (flexible)        │
│             │                       │                       │
│  - Files    │  - Syntax highlight   │  - Sandboxed iframe   │
│  - Folders  │  - IntelliSense       │  - Hot reload         │
│  - Context  │  - Multi-tab          │  - Console output     │
│    menu     │  - Auto-save          │  - Error overlay      │
└─────────────┴───────────────────────┴───────────────────────┘
```

---

## Monaco Editor Setup

### Installation

```bash
pnpm add @monaco-editor/react monaco-editor
```

### Basic Integration

```tsx
// components/editor/code-editor.tsx
'use client';

import Editor, { OnMount, OnChange } from '@monaco-editor/react';
import { useTheme } from 'next-themes';
import { useCallback, useRef } from 'react';
import type { editor } from 'monaco-editor';

interface CodeEditorProps {
  value: string;
  language: string;
  onChange: (value: string) => void;
  readOnly?: boolean;
}

export function CodeEditor({ value, language, onChange, readOnly }: CodeEditorProps) {
  const { theme } = useTheme();
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  const handleMount: OnMount = useCallback((editor) => {
    editorRef.current = editor;
    editor.focus();
  }, []);

  const handleChange: OnChange = useCallback((value) => {
    onChange(value ?? '');
  }, [onChange]);

  return (
    <Editor
      height="100%"
      language={language}
      value={value}
      onChange={handleChange}
      onMount={handleMount}
      theme={theme === 'dark' ? 'vs-dark' : 'light'}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily: 'JetBrains Mono, monospace',
        tabSize: 2,
        wordWrap: 'on',
        automaticLayout: true,
        scrollBeyondLastLine: false,
        readOnly,
        // Performance optimizations
        renderWhitespace: 'none',
        renderLineHighlight: 'line',
        quickSuggestions: true,
        folding: true,
      }}
    />
  );
}
```

### Language Detection

```typescript
// lib/editor/language-detection.ts
const EXTENSION_MAP: Record<string, string> = {
  '.ts': 'typescript',
  '.tsx': 'typescriptreact',
  '.js': 'javascript',
  '.jsx': 'javascriptreact',
  '.json': 'json',
  '.html': 'html',
  '.css': 'css',
  '.scss': 'scss',
  '.md': 'markdown',
  '.yaml': 'yaml',
  '.yml': 'yaml',
};

export function getLanguageFromPath(filePath: string): string {
  const ext = filePath.slice(filePath.lastIndexOf('.'));
  return EXTENSION_MAP[ext] ?? 'plaintext';
}
```

### Multi-Tab Support

```tsx
// components/editor/editor-tabs.tsx
'use client';

import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Tab {
  id: string;
  path: string;
  isDirty: boolean;
}

interface EditorTabsProps {
  tabs: Tab[];
  activeTabId: string;
  onTabSelect: (id: string) => void;
  onTabClose: (id: string) => void;
}

export function EditorTabs({ tabs, activeTabId, onTabSelect, onTabClose }: EditorTabsProps) {
  return (
    <div className="flex border-b border-border bg-muted/50 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabSelect(tab.id)}
          className={cn(
            "flex items-center gap-2 px-4 py-2 text-sm border-r border-border",
            "hover:bg-muted transition-colors",
            activeTabId === tab.id && "bg-background border-b-2 border-b-primary"
          )}
        >
          <span>{tab.path.split('/').pop()}</span>
          {tab.isDirty && <span className="w-2 h-2 rounded-full bg-primary" />}
          <X
            className="w-4 h-4 opacity-50 hover:opacity-100"
            onClick={(e) => {
              e.stopPropagation();
              onTabClose(tab.id);
            }}
          />
        </button>
      ))}
    </div>
  );
}
```

---

## Auto-Save Implementation

```typescript
// hooks/use-auto-save.ts
import { useEffect, useRef, useCallback } from 'react';
import { useDebouncedCallback } from 'use-debounce';

interface UseAutoSaveOptions {
  onSave: (content: string) => Promise<void>;
  delay?: number;
  enabled?: boolean;
}

export function useAutoSave({ onSave, delay = 1000, enabled = true }: UseAutoSaveOptions) {
  const pendingRef = useRef<string | null>(null);
  const savingRef = useRef(false);

  const debouncedSave = useDebouncedCallback(async (content: string) => {
    if (savingRef.current) {
      pendingRef.current = content;
      return;
    }

    savingRef.current = true;
    try {
      await onSave(content);
    } finally {
      savingRef.current = false;
      if (pendingRef.current !== null) {
        const pending = pendingRef.current;
        pendingRef.current = null;
        debouncedSave(pending);
      }
    }
  }, delay);

  const save = useCallback((content: string) => {
    if (enabled) {
      debouncedSave(content);
    }
  }, [debouncedSave, enabled]);

  return { save };
}
```

---

## Preview System

### Sandboxed Preview Frame

```tsx
// components/preview/preview-frame.tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { Loader2, AlertCircle } from 'lucide-react';

interface PreviewFrameProps {
  html: string;
  css?: string;
  js?: string;
  onError?: (error: string) => void;
}

export function PreviewFrame({ html, css, js, onError }: PreviewFrameProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!iframeRef.current) return;

    const doc = `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>${css ?? ''}</style>
          <script>
            window.onerror = function(msg, url, line) {
              window.parent.postMessage({ type: 'error', message: msg, line }, '*');
              return true;
            };
          </script>
        </head>
        <body>
          ${html}
          <script>${js ?? ''}</script>
        </body>
      </html>
    `;

    iframeRef.current.srcdoc = doc;
    setLoading(false);
  }, [html, css, js]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'error') {
        setError(event.data.message);
        onError?.(event.data.message);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [onError]);

  return (
    <div className="relative h-full w-full bg-white">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-muted">
          <Loader2 className="w-6 h-6 animate-spin" />
        </div>
      )}
      {error && (
        <div className="absolute top-0 left-0 right-0 p-2 bg-destructive text-destructive-foreground text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          {error}
        </div>
      )}
      <iframe
        ref={iframeRef}
        className="w-full h-full border-0"
        sandbox="allow-scripts"
        title="Preview"
      />
    </div>
  );
}
```

### WebContainer Integration (Advanced)

For full Node.js runtime in browser:

```typescript
// lib/preview/webcontainer.ts
import { WebContainer } from '@webcontainer/api';

let webcontainerInstance: WebContainer | null = null;

export async function getWebContainer(): Promise<WebContainer> {
  if (!webcontainerInstance) {
    webcontainerInstance = await WebContainer.boot();
  }
  return webcontainerInstance;
}

export async function mountProject(files: Record<string, string>) {
  const container = await getWebContainer();

  // Convert flat files to WebContainer format
  const tree = filesToTree(files);
  await container.mount(tree);

  return container;
}

export async function runDevServer(container: WebContainer) {
  // Install dependencies
  const installProcess = await container.spawn('npm', ['install']);
  await installProcess.exit;

  // Start dev server
  const devProcess = await container.spawn('npm', ['run', 'dev']);

  // Wait for server URL
  return new Promise<string>((resolve) => {
    container.on('server-ready', (port, url) => {
      resolve(url);
    });
  });
}
```

---

## Console Output

```tsx
// components/preview/console.tsx
'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

type LogLevel = 'log' | 'warn' | 'error' | 'info';

interface LogEntry {
  id: string;
  level: LogLevel;
  message: string;
  timestamp: Date;
}

export function Console() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data?.type === 'console') {
        setLogs((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            level: event.data.level,
            message: event.data.message,
            timestamp: new Date(),
          },
        ]);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  return (
    <div className="h-full overflow-auto bg-background font-mono text-xs">
      {logs.map((log) => (
        <div
          key={log.id}
          className={cn(
            "px-2 py-1 border-b border-border",
            log.level === 'error' && "bg-destructive/10 text-destructive",
            log.level === 'warn' && "bg-yellow-500/10 text-yellow-600",
            log.level === 'info' && "text-blue-600"
          )}
        >
          <span className="text-muted-foreground">
            {log.timestamp.toLocaleTimeString()}
          </span>{' '}
          {log.message}
        </div>
      ))}
    </div>
  );
}
```

---

## Performance Considerations

| Concern | Solution |
|---------|----------|
| Large files | Virtualize with `@monaco-editor/react` built-in |
| Frequent saves | Debounce 1000ms minimum |
| Preview updates | Throttle to 500ms |
| Memory leaks | Dispose editor on unmount |
| Initial load | Lazy load Monaco (~2MB) |

### Lazy Loading Monaco

```tsx
// Use dynamic import
import dynamic from 'next/dynamic';

const CodeEditor = dynamic(
  () => import('@/components/editor/code-editor').then(mod => mod.CodeEditor),
  {
    loading: () => <div className="h-full bg-muted animate-pulse" />,
    ssr: false,
  }
);
```
