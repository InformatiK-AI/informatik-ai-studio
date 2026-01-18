/**
 * ABOUTME: Login page with email/password form
 * RESPONSIBILITY: Handle user authentication
 * DEPENDENCIES: Supabase Auth (to be integrated)
 */
export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md">
        <h1 className="mb-8 text-center text-2xl font-bold">Sign In</h1>
        <div className="rounded-lg border border-border bg-card p-8">
          <p className="text-center text-muted-foreground">
            Login form will be implemented in Issue #8
          </p>
        </div>
      </div>
    </main>
  );
}
