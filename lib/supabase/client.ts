/**
 * ABOUTME: Browser-side Supabase client for client components
 * RESPONSIBILITY: Create and configure Supabase client for browser usage
 * DEPENDENCIES: @supabase/ssr
 * SECURITY: ONLY uses NEXT_PUBLIC_SUPABASE_ANON_KEY (never service role key)
 */

'use client';

import { createBrowserClient } from '@supabase/ssr';

/**
 * Creates a Supabase client for use in Client Components
 *
 * SECURITY NOTE: This client uses the anon key which is safe to expose
 * to the browser. All data access is protected by Row Level Security (RLS)
 * policies on the database tables.
 *
 * @returns Supabase browser client instance
 */
export function createClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      'Missing Supabase environment variables. ' +
      'Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are set.'
    );
  }

  return createBrowserClient(supabaseUrl, supabaseAnonKey);
}
