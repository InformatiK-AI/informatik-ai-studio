/**
 * ABOUTME: Dashboard page showing user projects
 * RESPONSIBILITY: Display project list and dashboard widgets
 * DEPENDENCIES: Supabase (to be integrated)
 */
export default function DashboardPage() {
  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-2xl font-bold">My Projects</h1>
          <button className="rounded-lg bg-primary px-4 py-2 text-primary-foreground font-medium hover:opacity-90 transition-opacity">
            New Project
          </button>
        </div>
        <div className="rounded-lg border border-border bg-card p-8 text-center">
          <p className="text-muted-foreground">
            Dashboard will be implemented in Issue #14
          </p>
        </div>
      </div>
    </main>
  );
}
