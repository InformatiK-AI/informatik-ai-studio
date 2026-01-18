/**
 * ABOUTME: Signup page with registration form
 * RESPONSIBILITY: Handle new user registration
 * DEPENDENCIES: Supabase Auth (to be integrated)
 */
export default function SignupPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md">
        <h1 className="mb-8 text-center text-2xl font-bold">Create Account</h1>
        <div className="rounded-lg border border-border bg-card p-8">
          <p className="text-center text-muted-foreground">
            Signup form will be implemented in Issue #7
          </p>
        </div>
      </div>
    </main>
  );
}
