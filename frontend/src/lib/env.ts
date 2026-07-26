function requireEnv(name: string): string {
  const value = import.meta.env[name];
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}. ` +
        "Set it in your .env file (VITE_ prefix required)."
    );
  }
  return value;
}

export const env = {
  API_BASE_URL: requireEnv("VITE_API_BASE_URL"),
  SUPABASE_URL: requireEnv("VITE_SUPABASE_URL"),
  SUPABASE_ANON_KEY: requireEnv("VITE_SUPABASE_ANON_KEY"),
} as const;
