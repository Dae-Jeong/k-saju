// Runs once when a new Next.js server instance starts (`next dev` /
// `next start`), before it accepts requests. Importing env-config here
// re-validates server-only + NEXT_PUBLIC_* vars at server start, not just at
// build time — see docs/architecture/env.md at the repo root.
export async function register(): Promise<void> {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('@/common/constants/env-config');
  }
}
