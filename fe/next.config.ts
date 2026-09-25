import type { NextConfig } from 'next';

// Importing this validates process.env eagerly (throws listing every
// missing/invalid key) — makes `next build` (and thus `pnpm build`) fail
// fast before compiling, since next.config.ts loads before anything else.
import './src/common/constants/env-config';

const nextConfig: NextConfig = {
  output: 'standalone',
};

export default nextConfig;
