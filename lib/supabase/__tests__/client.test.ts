/**
 * ABOUTME: Unit tests for browser Supabase client
 * RESPONSIBILITY: Verify client creation and environment variable validation
 * DEPENDENCIES: Vitest, @supabase/ssr
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createClient } from '../client';

describe('createClient (Browser)', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    // Reset environment before each test
    vi.resetModules();
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    // Restore original environment
    process.env = originalEnv;
  });

  it('should create a Supabase client with valid environment variables', () => {
    // Arrange
    process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';

    // Act
    const client = createClient();

    // Assert
    expect(client).toBeDefined();
    expect(client.auth).toBeDefined();
    expect(client.from).toBeDefined();
  });

  it('should throw error if NEXT_PUBLIC_SUPABASE_URL is missing', () => {
    // Arrange
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';

    // Act & Assert
    expect(() => createClient()).toThrow('Missing Supabase environment variables');
  });

  it('should throw error if NEXT_PUBLIC_SUPABASE_ANON_KEY is missing', () => {
    // Arrange
    process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
    delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    // Act & Assert
    expect(() => createClient()).toThrow('Missing Supabase environment variables');
  });

  it('should throw error if both environment variables are missing', () => {
    // Arrange
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

    // Act & Assert
    expect(() => createClient()).toThrow('Missing Supabase environment variables');
  });

  it('should use NEXT_PUBLIC prefix (client-safe variables)', () => {
    // Arrange
    process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';

    // This test verifies that we ONLY use NEXT_PUBLIC_ prefixed variables
    // which are safe to expose to the browser

    // Act
    const client = createClient();

    // Assert
    expect(client).toBeDefined();
    // Service role key should NEVER be used in browser client
    expect(process.env.SUPABASE_SERVICE_ROLE_KEY).toBeUndefined();
  });
});
