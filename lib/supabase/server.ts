/**
 * ABOUTME: Server-side Supabase clients for Server Components and API Routes
 * RESPONSIBILITY: Provide authenticated and admin Supabase clients for server-side use
 * DEPENDENCIES: @supabase/ssr, next/headers
 * SECURITY: Provides two clients - one respecting RLS (user context) and one for admin operations
 */

import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

/**
 * Creates a Supabase client for Server Components and Route Handlers
 *
 * SECURITY NOTE: This client respects Row Level Security (RLS) policies
 * because it uses the anon key with user session cookies. Use this for
 * operations that should respect user permissions.
 *
 * @returns Supabase server client instance with user context
 */
export async function createClient() {
  const cookieStore = await cookies();
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      'Missing Supabase environment variables. ' +
      'Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are set.'
    );
  }

  return createServerClient(supabaseUrl, supabaseAnonKey, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        } catch {
          // The `setAll` method was called from a Server Component.
          // This can be ignored if you have middleware refreshing
          // user sessions.
        }
      },
    },
  });
}

/**
 * Creates an admin Supabase client that bypasses Row Level Security
 *
 * ⚠️ CRITICAL SECURITY WARNING ⚠️
 * This client has FULL database access and bypasses ALL RLS policies.
 * Use ONLY for:
 * - System-level operations
 * - Admin dashboard functionality
 * - Background jobs
 * - Migration scripts
 *
 * NEVER use this client for user-facing operations or expose it to client code.
 * Always validate user permissions before using this client.
 *
 * @returns Supabase admin client instance (bypasses RLS)
 */
export function createAdminClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (!supabaseUrl || !supabaseServiceRoleKey) {
    throw new Error(
      'Missing Supabase admin environment variables. ' +
      'Ensure NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set.'
    );
  }

  return createServerClient(supabaseUrl, supabaseServiceRoleKey, {
    cookies: {
      getAll() {
        return [];
      },
      setAll() {
        // Admin client doesn't need cookie management
      },
    },
  });
}
