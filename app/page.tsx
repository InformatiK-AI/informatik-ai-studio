/**
 * ABOUTME: Landing page for InformatiK-AI Studio
 * RESPONSIBILITY: Display marketing/intro content and CTA
 */
export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="mb-4 text-4xl font-bold">InformatiK-AI Studio</h1>
        <p className="mb-8 text-lg text-muted-foreground">
          AI-powered software generation platform
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/login"
            className="rounded-lg bg-primary px-6 py-3 text-primary-foreground font-medium hover:opacity-90 transition-opacity"
          >
            Get Started
          </a>
          <a
            href="/dashboard"
            className="rounded-lg border border-border px-6 py-3 font-medium hover:bg-muted transition-colors"
          >
            Dashboard
          </a>
        </div>
      </div>
    </main>
  );
}
