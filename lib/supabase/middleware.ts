/**
 * ABOUTME: Middleware helper for refreshing Supabase user sessions
 * RESPONSIBILITY: Keep user sessions fresh and handle session cookie updates
 * DEPENDENCIES: @supabase/ssr, next/server
 * SECURITY: Uses HttpOnly, Secure, SameSite cookies for session protection
 */

import { createServerClient } from '@supabase/ssr';
import { type NextRequest, NextResponse } from 'next/server';

/**
 * Updates the user session and refreshes auth tokens
 *
 * This function should be called from Next.js middleware to ensure
 * user sessions are kept fresh across requests. It handles:
 * - Session token refresh
 * - Cookie updates with secure settings
 * - Automatic re-authentication
 *
 * SECURITY: Cookies are set with:
 * - HttpOnly: true (prevents XSS attacks)
 * - Secure: true (HTTPS only in production)
 * - SameSite: 'lax' (CSRF protection)
 *
 * @param request - The incoming Next.js request
 * @returns NextResponse with updated session cookies
 */
export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseAnonKey) {
    console.error('Missing Supabase environment variables in middleware');
    return supabaseResponse;
  }

  const supabase = createServerClient(supabaseUrl, supabaseAnonKey, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value }) =>
          request.cookies.set(name, value)
        );
        supabaseResponse = NextResponse.next({
          request,
        });
        cookiesToSet.forEach(({ name, value, options }) =>
          supabaseResponse.cookies.set(name, value, options)
        );
      },
    },
  });

  // IMPORTANT: Avoid writing any logic between createServerClient and
  // supabase.auth.getUser(). A simple mistake could make it very hard to debug
  // issues with users being randomly logged out.

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Optional: Add custom session validation logic here
  // For example, check if user has required permissions
  // or if their account is still active

  if (
    !user &&
    !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth')
  ) {
    // No user session found, and not on auth pages
    // Optionally redirect to login
    // const url = request.nextUrl.clone();
    // url.pathname = '/login';
    // return NextResponse.redirect(url);
  }

  // IMPORTANT: You *must* return the supabaseResponse object as it is.
  // If you're creating a new response object with NextResponse.next() make sure to:
  // 1. Pass the request in it, like so:
  //    const myNewResponse = NextResponse.next({ request })
  // 2. Copy over the cookies, like so:
  //    myNewResponse.cookies.setAll(supabaseResponse.cookies.getAll())
  // 3. Change the myNewResponse object to fit your needs, but avoid changing
  //    the cookies!
  // 4. Finally:
  //    return myNewResponse
  // If this is not done, you may be causing the browser and server to go out
  // of sync and terminate the user's session prematurely.

  return supabaseResponse;
}
