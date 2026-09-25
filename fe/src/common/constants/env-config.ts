import { z } from 'zod';

// The app reads only OS environment variables — Next.js is never allowed to
// load them from an fe/.env* file (none exist in this repo; see docs/env.md
// at the repo root). NEXT_PUBLIC_* vars are baked in at build time (passed
// as Docker build args in fe/Dockerfile); this module validates them eagerly
// on import so both `pnpm build` and server start fail fast with every
// missing/invalid key listed, instead of surfacing a runtime crash later.
const envSchema = z.object({
  NEXT_PUBLIC_API_BASE_URL: z.string().url(),
});

function loadEnv(): z.infer<typeof envSchema> {
  const result = envSchema.safeParse({
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  });

  if (!result.success) {
    const keys = [
      ...new Set(result.error.issues.map((issue) => String(issue.path[0]))),
    ];
    throw new Error(
      `Missing or invalid environment variables: ${keys.join(', ')}`,
    );
  }

  return result.data;
}

const env = loadEnv();

export const envConfig = {
  apiBaseUrl: env.NEXT_PUBLIC_API_BASE_URL,
} as const;
