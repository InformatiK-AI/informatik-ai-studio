/**
 * ABOUTME: Next.js middleware for session management and route protection
 * RESPONSIBILITY: Refresh Supabase sessions on every request
 * DEPENDENCIES: lib/supabase/middleware
 */

import { updateSession } from '@/lib/supabase/middleware';

/**
 * Middleware function executed on every request
 *
 * This middleware:
 * - Refreshes user authentication sessions automatically
 * - Updates session cookies with secure settings
 * - Runs before all routes to ensure valid user context
 *
 * @param request - The incoming request
 * @returns Response with updated session cookies
 */
export async function middleware(request: Request) {
  return await updateSession(request);
}

/**
 * Matcher configuration - applies middleware to all routes except static files
 *
 * Excludes:
 * - _next/static (static files)
 * - _next/image (image optimization)
 * - favicon.ico (favicon)
 * - Public files (.svg, .png, .jpg, .jpeg, .gif, .webp)
 */
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
