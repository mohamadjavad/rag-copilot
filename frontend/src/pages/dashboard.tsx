import { useAuth } from "@/lib/auth";

export default function Dashboard() {
  const { user, signOut } = useAuth();

  return (
    <div className="flex min-h-screen flex-col p-6">
      <header className="flex items-center justify-between border-b border-border pb-4">
        <h1 className="text-lg font-semibold text-foreground">
          Document Copilot
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground">{user?.email}</span>
          <button
            onClick={signOut}
            className="inline-flex h-8 items-center rounded-md border border-border px-3 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            Sign out
          </button>
        </div>
      </header>
      <main className="flex flex-1 items-center justify-center">
        <p className="text-muted-foreground">
          Chat will be built in Phase 3.
        </p>
      </main>
    </div>
  );
}
