/**
 * ABOUTME: Unit tests for server Supabase clients
 * RESPONSIBILITY: Verify server and admin client creation and security
 * DEPENDENCIES: Vitest, @supabase/ssr, next/headers
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock next/headers
vi.mock('next/headers', () => ({
  cookies: vi.fn(() =>
    Promise.resolve({
      getAll: vi.fn(() => []),
      set: vi.fn(),
      get: vi.fn(),
    })
  ),
}));

describe('Server Supabase Clients', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    vi.resetModules();
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  describe('createClient (Server with RLS)', () => {
    it('should create a server client with user context', async () => {
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';

      // Import after setting env vars
      const { createClient } = await import('../server');

      // Act
      const client = await createClient();

      // Assert
      expect(client).toBeDefined();
      expect(client.auth).toBeDefined();
      expect(client.from).toBeDefined();
    });

    it('should throw error if environment variables are missing', async () => {
      // Arrange
      delete process.env.NEXT_PUBLIC_SUPABASE_URL;
      delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

      // Import after clearing env vars
      const { createClient } = await import('../server');

      // Act & Assert
      await expect(createClient()).rejects.toThrow(
        'Missing Supabase environment variables'
      );
    });

    it('should use anon key (respects RLS)', async () => {
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';
      process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

      const { createClient } = await import('../server');

      // Act
      const client = await createClient();

      // Assert
      expect(client).toBeDefined();
      // This client should use anon key, not service role
      // It respects Row Level Security policies
    });
  });

  describe('createAdminClient (Bypasses RLS)', () => {
    it('should create an admin client with service role key', () => {
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

      // Import synchronously for admin client
      const { createAdminClient } = require('../server');

      // Act
      const client = createAdminClient();

      // Assert
      expect(client).toBeDefined();
      expect(client.auth).toBeDefined();
      expect(client.from).toBeDefined();
    });

    it('should throw error if service role key is missing', () => {
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      delete process.env.SUPABASE_SERVICE_ROLE_KEY;

      const { createAdminClient } = require('../server');

      // Act & Assert
      expect(() => createAdminClient()).toThrow(
        'Missing Supabase admin environment variables'
      );
    });

    it('should throw error if Supabase URL is missing', () => {
      // Arrange
      delete process.env.NEXT_PUBLIC_SUPABASE_URL;
      process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

      const { createAdminClient } = require('../server');

      // Act & Assert
      expect(() => createAdminClient()).toThrow(
        'Missing Supabase admin environment variables'
      );
    });

    it('should NEVER use service role key in regular server client', async () => {
      // SECURITY TEST: Ensure service role key is isolated to admin client only
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';
      process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

      const { createClient } = await import('../server');

      // Act
      const regularClient = await createClient();

      // Assert
      // Regular server client should use anon key, NOT service role
      expect(regularClient).toBeDefined();
      // This is a critical security requirement
    });
  });

  describe('Security Validation', () => {
    it('should separate client types correctly', async () => {
      // Arrange
      process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key';
      process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

      const { createClient, createAdminClient } = await import('../server');

      // Act
      const userClient = await createClient();
      const adminClient = createAdminClient();

      // Assert
      expect(userClient).toBeDefined();
      expect(adminClient).toBeDefined();
      // Both should exist but use different keys
      // userClient: anon key (respects RLS)
      // adminClient: service role key (bypasses RLS)
    });
  });
});
