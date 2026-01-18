/**
 * ABOUTME: TypeScript type definitions
 * RESPONSIBILITY: Centralize type definitions for the application
 */

/**
 * Base entity with common fields
 */
export interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Project entity
 */
export interface Project extends BaseEntity {
  userId: string;
  name: string;
  description?: string;
  template: string;
  settings: Record<string, unknown>;
  deployedUrl?: string;
  vercelProjectId?: string;
}

/**
 * Project file entity
 */
export interface ProjectFile extends BaseEntity {
  projectId: string;
  path: string;
  content: string;
  language?: string;
}

/**
 * AI generation record
 */
export interface Generation extends BaseEntity {
  projectId: string;
  prompt: string;
  response?: string;
  model: string;
  tokensInput: number;
  tokensOutput: number;
  durationMs?: number;
  status: 'pending' | 'completed' | 'failed';
}

/**
 * Deployment record
 */
export interface Deployment extends BaseEntity {
  projectId: string;
  provider: 'vercel';
  status: 'queued' | 'building' | 'ready' | 'failed';
  url?: string;
  errorMessage?: string;
  envVars: Record<string, string>;
}
